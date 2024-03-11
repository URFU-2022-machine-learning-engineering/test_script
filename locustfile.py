from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    host = "https://api.dzailz.su"

    @task
    def hello_world(self):
        self.client.get("/status")
        # self.client.get("/upload")
