from typing import List, Optional
import random
import json


def get_scheduler():
    return [
        ("First Come Scheduling", FirstComeScheduler),
        ("Shortest Task Scheduling", ShortestTaskScheduler),
        ("Round Robin Scheduling", RoundRobinScheduler),
    ]


class Task:
    def __init__(self, _name: str, _time: int, _cost: int, _priority: Optional[int] = None):
        self.name: str = _name
        self.arrive_time: int = _time
        self.cost: int = _cost
        self.finish_time: int = 0
        self.priority: int = _priority
        print(f"Created {str(self)}")

    def process(self) -> bool:
        # returns is task finished
        self.cost -= 1
        if self.cost == 0:
            return True
        return False

    def __str__(self):
        if self.priority == None:
            return f"Task {self.name}(arrive={self.arrive_time}, cost={self.cost})"
        else:
            return f"Task {self.name}(arrive={self.arrive_time}, cost={self.cost}, priority={self.priority})"


class Scheduler:
    def __init__(self):
        self.time: int = 0
        self.finished: List[Task] = []
        self.tasks: List[Task] = []
        self.queue: List[Task] = []
        self.start_menu()
        self.get_task()
        self.printer()

    def start_menu(self) -> None:
        flag = True
        print("Select Task Type(0: Add tasks by random, 1:Add tasks by manual, 2:Import from JSON File)")
        i = int(input())

        if i == 0:
            print("Input tasks number")
            task_num = int(input())
            for j in range(task_num):
                self.add_task(
                    Task(chr(65+j), random.randint(0, j), random.randint(1, 10)))
        elif i == 1:
            print("Input tasks number")
            task_num = int(input())
            print("Input tasks")
            print("ex.)[A 0 2] to make  a task A (arrive time:0, cost:2)")
            for j in range(task_num):
                name, time, cost = input().split()
                self.add_task(Task(name, int(time), int(cost)))
        elif i == 2:
            tasks = []
            with open("tasks.json", mode="r") as f:
                tasks = json.load(f)["tasks"]
            for t in tasks:
                self.add_task(Task(t["name"], t["time"], t["cost"]))

        else:
            raise ValueError

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task_finished(self) -> None:
        for t in self.queue:
            if t.cost == 0:
                self.finished.append(t)
        for t in self.finished:
            if t in self.queue:
                self.queue.remove(t)

    def get_task(self) -> None:
        for t in self.tasks:
            if t.arrive_time == self.time:
                self.queue.append(t)

        for t in self.queue:
            if t in self.tasks:
                self.tasks.remove(t)

    def process(self) -> bool:
        r = False
        if (self.time == 0):
            self.get_task()
        if (len(self.queue) != 0):
            r = self.queue[0].process()
            if r:
                self.queue[0].finish_time = self.time + 1

            self.get_task()
            self.remove_task_finished()

        self.time += 1
        return r

    def is_finish(self) -> bool:
        if len(self.tasks) != 0:
            return False
        if len(self.queue) != 0:
            return False

        print("Finished")
        # Turn Around
        for t in self.finished:
            print(
                f"{t.name}:({t.finish_time}-{t.arrive_time}=){t.finish_time - t.arrive_time}")
        print("Average turnaround time: {}\n".format(
            sum([t.finish_time - t.arrive_time for t in self.finished])/len(self.finished)))
        return True

    def printer(self) -> None:
        max_string = max([len(t.name) for t in self.queue] +
                         [len(t.name) for t in self.finished] +
                         [len(t.name) for t in self.tasks])
        print(f"TIME = {self.time}")

        if (len(self.tasks) != 0):
            print("In Task List(not arrived)")
            for t in self.tasks:
                print(" "*(max_string-len(t.name)), end="")
                print(f"{t.name}: Cost={t.cost}")
        print()
        if (len(self.queue) != 0):
            print("In Queue(arrived)")
            for t in self.queue:
                print(" "*(max_string-len(t.name)), end="")
                print(f"{t.name}: Cost={t.cost}")
        print()
        if (len(self.finished) != 0):
            print("In Finished List")
            for t in self.finished:
                print(" "*(max_string-len(t.name)), end="")
                print(f"{t.name}: Cost={t.cost}")
        print("---Enter to proceed---")
        input()


class FirstComeScheduler(Scheduler):
    def __init__(self):
        super().__init__()

    def start(self):
        while True:
            if self.is_finish():
                return

            self.process()
            self.printer()


class ShortestTaskScheduler(Scheduler):
    def __init__(self):
        super().__init__()

    def start(self):
        while True:
            if self.is_finish():
                return

            if not self.process():
                self.printer()
                continue
            if len(self.queue) == 0:
                continue
            queue_cost = [t.cost for t in self.queue]
            shortest = queue_cost.index(min(queue_cost))
            self.queue = (
                self.queue[shortest:shortest+1] +
                self.queue[:shortest] +
                self.queue[shortest+1:])
            self.printer()


class RoundRobinScheduler(Scheduler):
    def __init__(self):
        print("Input interval time")
        self.interval: int = int(input())
        super().__init__()

    def start(self):
        while(True):
            if self.is_finish():
                return

            r = self.process()
            if not r and self.time % self.interval == 0:
                self.queue = self.queue[1:] + self.queue[:1]
            self.printer()
