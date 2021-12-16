import random
import time
from threading import Thread, Condition


class JobsAndUsers:
    def __init__(self, number_of_users, number_of_resources, job_size):
        self.n = number_of_users
        self.r = number_of_resources
        self.m = job_size
        self.resources = [Condition() for _ in range(number_of_resources)]
        self.jobs = [job_size for _ in range(number_of_users)]

    def user(self, i):
        print("Hi, I am user #%d" % i)
        while self.jobs[i] > 0:
            time.sleep(3 + random.random())
            print("User #%d wants to start now" % i)
            r = random.randint(0, self.r - 1)
            print("User #%d is trying to get the resource #%d" % (i, r))
            if self.resources[r].acquire():
                print("User #%d has the resource #%d" % (i, r))
                time.sleep(5 + random.random())
                self.jobs[i] -= 1
                self.resources[r].notify()
                self.resources[r].release()
                print("User #%d has completed the job" % i)
            else:
                print("User #%d could not get the resource #%d" % (i, r))


def main():
    n = 10
    r = 3
    m = 100
    jobs_and_users = JobsAndUsers(n, r, m)
    users = [Thread(target=jobs_and_users.user, args=(i,)) for i in range(n)]
    for user in users:
        user.start()
    '''
    while sum(jobs_and_users.jobs):
        print(jobs_and_users.jobs)
        time.sleep(0.1)'''
    for user in users:
        user.join()


if __name__ == "__main__":
    main()