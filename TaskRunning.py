from locust import  HttpLocust,TaskSet,task

count = 0;

class Task(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        global count
        count += 1
        self.tmp = count
        print("Print locust number:" + str(self.tmp))

    @task
    def run_task_1(self):
        self.client.get("/")
        print("Locust "+str(self.tmp)+" is running")


class Run(HttpLocust):
    task_set = Task