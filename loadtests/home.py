from __future__ import annotations

from locust import HttpUser
from locust import task


class Home(HttpUser):
    @task
    def home_endpoint(self):
        self.client.get("/api/home/")
