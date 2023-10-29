from CyclicTask.TimedTask import TimedTask
import time

class Task(TimedTask):
    def task(task) -> None:
        print("Execution")
        time.sleep(1.1)

t = Task(1.0, 1.2, "TimedTask")
t.start()

time.sleep(5.0)

t.stop()
t.join()