from locust import HttpLocust, TaskSet, task, HttpUser, between
import random
import json
"""
Locustfile.py utilize Locust for stress testing the applcation under simulated environment with server requests. 
Mainly used to test performance, load handling, failure rate, code bottlenecks, and DDOS handling. 

@Class WebsiteUser: Simulates client side user requests within the application.
"""

sampleIds = ["Logan1","Tina5","Nick8", "Keith7", "Jayden99"]

def on_start(self):
    		self.client.post("/login", json={"username":"varun08", "password":"fortheear"})


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task(1)
    def index(self):
        self.client.get("http://localhost:33507/")
        self.client.get("http://localhost:33507/static/images")

    @task(2)
    def rebit_nov(self):
        self.client.get("http://localhost:33507/rebit_cyberpulse_nov")
    
    @task(3)
    def rebit_dec(self):
        self.client.get("http://localhost:33507/rebit/cyberpulse-dec")

    def abiltiy_Test(self):
        self.client.get("http://localhost:33507/abiltiy_test")


class stressTest(HttpUser):
	task_set = WebsiteUser
	min_wait = 5000
	max_wait = 10000
