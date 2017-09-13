from locust.runners import LocalLocustRunner
import PrintStatsExtra
import TaskRunning
import LoginStory
from gevent import Greenlet

#StubOptions replace for options attribute in the legacy runner class
class StubOptions:
    def __init__(self,hatch_rate=10,host = None):
        self.hatch_rate = hatch_rate
        self.num_clients = 0
        self.num_requests = None
        self.host = host
        self.no_reset_stats = True

#Ramp Up Runner extended from Local Locust Runner
class RampUpRunner(LocalLocustRunner):
    def __init__(self, locust_classes, options):
        print([locust_classes])
        super(RampUpRunner, self).__init__([locust_classes], options)

    def ramp_up(self,locust_count_first_step,
                number_of_steps,
                duration_of_each_step,
                locust_count_each_step):
        self.hatching_greenlet = Greenlet.spawn(self.return_runner_to_spawn(locust_count_first_step))
        self.greenlet = self.hatching_greenlet
        self.greenlet.join(timeout=duration_of_each_step)
        allHatched = False
        stepCount = 0
        maxUser = locust_count_first_step + locust_count_each_step
        while True:
            if not allHatched:
                self.hatching_greenlet = Greenlet.spawn(self.return_runner_to_spawn(maxUser))
                self.greenlet.join(timeout=duration_of_each_step)
                maxUser+=locust_count_each_step
                stepCount += 1
                if stepCount==number_of_steps:
                    allHatched = True
            else:
                self.greenlet.join(50)
                PrintStatsExtra.print_stats_extra(self.request_stats)
                PrintStatsExtra.print_percentile_stats_extra(self.request_stats)
                break

    def return_runner_to_spawn(self,number_of_locust):
        return lambda: super(LocalLocustRunner, self).start_hatching(locust_count=number_of_locust, hatch_rate=None, wait=True)

if __name__ == '__main__':
    #Running with hatch rate 10, first step start with 20, then next 3 steps with 10 locusts each step, the duration between each step is 5 seconds.
    #Note that the hatch rate should be lower than the duration between each step.
    RampUpRunner(LoginStory.LoginLocust, StubOptions(hatch_rate=10,host = "http://192.168.74.204")).ramp_up(20,3,5,10)

