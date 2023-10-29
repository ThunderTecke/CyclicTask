from CyclicTask.ContinuousTask import ContinuousTask
import time

class Task(ContinuousTask):
    def task(self) -> None:
        print("Execution")
        time.sleep(2.1)

t = Task(2.0, "ContinuousTask")
t.start()

time.sleep(5.0)
t.stop()
t.join()