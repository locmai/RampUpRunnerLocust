from locust import HttpLocust,TaskSet,task
import re
import csv

#Import Account CSV Data Set
with open('saleor_accounts.csv','rb') as f:
            reader = csv.reader(f)
            account_list = list(reader)

count=0

#Two mandatory classes to run Locust test: a TaskSet class and a Locust class (HttpLocust means Locust for Http)
class LoginTask(TaskSet):
    user_account =[]
    #When a locust spawned,it will first use the method 
    def on_start(self):
        global count,account_list
        count+=1
        #Get account info from the list of accounts.
        self.user_account = account_list[count]
        print "Launch User:" + self.user_account[0] + "/" + self.user_account[1]
        
    @task
    def UserLogin(self):
        #Load Homepage and Extract csrf token
        r = self.client.get("/account/login/",name="1. Login Page")
        csrf_token = re.search("<input type='hidden' name='csrfmiddlewaretoken' value='(.+?)' />", r.content,re.IGNORECASE).group(1)
        
        self._sleep(10)
        
        #Login request
        r = self.client.post("/account/login/",{
                            "csrfmiddlewaretoken":csrf_token,
                            "username":self.user_account[0],
                            "password":self.user_account[1]},
                            name="2. Submit Login")
        #Redirecting to front page
        
        self._sleep(10)
        
        self.client.get("/cart/summary/",name="3. Redirecting")
        
        self._sleep(10)
        
        #Logout
        self.client.get("/account/logout/",name="4. Logout")

class LoginLocust(HttpLocust):
    host = "http://192.168.74.204"
    task_set = LoginTask
    min_wait = 10000
    max_wait = 10000

