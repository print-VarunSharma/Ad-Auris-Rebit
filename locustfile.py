from locust import HttpLocust, TaskSet, task, HttpUser, between
import random
import json


sampleIds = ["Logan1","Tina5","Nick8", "Keith7", "Jayden99"]

def on_start(self):
    		self.client.post("/login", json={"username":"varun08", "password":"fortheear"})


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def index(self):
        self.client.get("/")
        self.client.get("/static/images")
        
    @task
    def rebit_nov(self):
        self.client.get("/rebit_cyberpulse_nov")
    
    @task
    def rebit_dec(self):
        self.client.get("/rebit/cyberpulse-dec")
	

class stressTest(HttpUser):
	task_set = WebsiteUser
	min_wait = 5000
	max_wait = 10000