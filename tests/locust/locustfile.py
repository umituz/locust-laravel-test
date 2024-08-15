from locust import HttpUser, task, between
import random

class LaravelUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def view_home(self):
        self.client.get("/")

    @task(2)
    def view_api(self):
        self.client.get("/api")

    @task(1)
    def post_api_data(self):
        payload = {
            "name": f"User {random.randint(1, 1000)}",
            "email": f"user_{random.randint(1, 1000)}@example.com"
        }
        self.client.post("/api/data", json=payload)

    @task(1)
    def check_up(self):
        self.client.get("/up")
