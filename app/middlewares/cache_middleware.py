from typing import List

from fastapi import Request
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response
from app.config.base import settings

from app.wrappers.cache_wrappers import create_cache, retrieve_cache

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            cached_endpoints: List[str],
    ):
        super().__init__(app)
        self.cached_endpoints = cached_endpoints
    def matches_any_path(self, path_url):
        for pattern in self.cached_endpoints:
            if pattern in path_url:
                return True
        return False

    async def dispatch(self, request: Request, call_next) -> Response:
        path_url = request.url.path
        request_type = request.method
        cache_control = request.headers.get('Cache-Control', None)
        auth = request.headers.get('Authorization', "token public")
        token = auth.split(" ")[1]
        max_age=settings.CACHE_MAX_AGE
        key = f"{path_url}_{token}"
        #checking if end point has been added into cached endpoint
        matches = self.matches_any_path(path_url)
        
        #check if endpoint method is get if not call next function or middleware in chain
        if request_type != 'GET':
            return await call_next(request)

        #getting stored cache for endpoint
        stored_cache = await retrieve_cache(key)
        res = stored_cache and cache_control != 'no-cache'

        if not res:
            response: Response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
        #checking if response is success
            if response.status_code == 200:
        #check if cache header is no-strore if true it return (Applicable for cached endpoint as well as cache control header in request)
                if cache_control == 'no-store':
                    return response
        #check if cache control has max has param if true create a cache for endpoint
                elif cache_control and "max-age" in cache_control:
                    max_age = int(cache_control.split("=")[1])
                    await create_cache(response_body[0].decode(), key, max_age)
        # no cache-control header is present but endpoint is in cached endpoint so by default it is caching response for 60 second
                elif matches:
                    await create_cache(response_body[0].decode(), key, max_age)
            return response

        else:
            # If the response is cached, return it directly
            headers = {
                'Cache-Control': f"max-age:{stored_cache[1]}"
            }
            return StreamingResponse(iter([stored_cache[0]]), media_type="application/json", headers=headers)