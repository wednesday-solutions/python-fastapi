from __future__ import annotations

import re

from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.responses import StreamingResponse

from app.config.base import settings
from app.wrappers.cache_wrappers import CacheUtils


class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        cached_endpoints: list[str],
    ):
        super().__init__(app)
        self.cached_endpoints = cached_endpoints

    def matches_any_path(self, path_url):
        for end_point in self.cached_endpoints:
            if end_point in path_url:
                return True
        return False

    async def handle_max_age(self, max_age, response_body, key):
        if max_age:
            await CacheUtils.create_cache(response_body[0].decode(), key, max_age)

    async def dispatch(self, request: Request, call_next) -> Response:
        path_url = request.url.path
        request_type = request.method
        cache_control = request.headers.get("Cache-Control", None)
        auth = request.headers.get("Authorization", "token public")
        token = auth.split(" ")[1]
        max_age = settings.CACHE_MAX_AGE
        key = f"{path_url}_{token}"
        matches = self.matches_any_path(path_url)

        if request_type != "GET":
            return await call_next(request)

        stored_cache, expire = await CacheUtils.retrieve_cache(key)
        res = stored_cache and cache_control != "no-cache"

        if res:
            headers = {"Cache-Control": f"max-age:{expire}"}
            return StreamingResponse(iter([stored_cache]), media_type="application/json", headers=headers)

        response: Response = await call_next(request)
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        if response.status_code == 200:
            if cache_control == "no-store":
                return response
            if cache_control:
                max_age_match = re.search(r"max-age=(\d+)", cache_control)
                if max_age_match:
                    max_age = int(max_age_match.group(1))
                    await self.handle_max_age(max_age, response_body, key)
            elif matches:
                await CacheUtils.create_cache(response_body[0].decode(), key, max_age)
        return response
