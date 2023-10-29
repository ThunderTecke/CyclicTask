import threading
import time
from .CycleTimeError import CycleTimeError
import logging

class TimedTask(threading.Thread):
    """
    TimedTask A task performed with delay between each execution.

    Parameters
    ----------
    cycleTime: float
        The delay between each execution.
    
    maximumTime: float | None, default = None
        The maximum cycle time permitted. If the runtime exceed the maximum time an "CycleTimeError" will be raised.
        If None or lower than the cycle time, the maximum time is defined as 150% of the cycle time.
    """
    def __init__(self, cycleTime: float, maximumTime: float | None = None, name: str | None = None) -> None:
        super().__init__(name=name)

        # Attributes
        self.cycleTime = cycleTime

        if maximumTime is None:
            self.maximumTime = self.cycleTime * 1.5
            self.logger.warning(f"The maximum time has been set to {self.maximumTime}, because it undefined.")
        elif maximumTime < self.cycleTime:
            self.maximumTime = self.cycleTime * 1.5
            self.logger.warning(f"The maximum time has been set to {self.maximumTime}, because it was lower than the cycle time.")
        else:
            self.maximumTime = maximumTime


        self.stopThread = False

        self.lastExecutionTime = None
        self.lastRuntime = None

        self.cycleTimeWarning = False

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(name)s - %(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.logger.info(f"Timed task \"{self.name}\" created")

    def run(self) -> None:
        """
        Execute the method "task" every `cycleTime` seconds.

        Raises
        ------
        CycleTimeError
            Indicate that the runtime has exceeded the maximum runtime.
        """
        while not self.stopThread:
            self.lastExecutionTime = time.time()
            self.task()
            self.lastRuntime = time.time() - self.lastExecutionTime

            if self.maximumTime is None:
                self.logger.debug(f"Task executed ({self.lastRuntime}s)")
            else:
                if self.lastRuntime >= self.maximumTime:
                    self.cycleTimeWarning = False
                    self.logger.error(f"Maximum cycle time exceeded ({self.lastRuntime:.3f}s/{self.cycleTime:.3f}s - {(self.lastRuntime/self.cycleTime)*100.0:.3f}%, maximum {(self.maximumTime/self.cycleTime)*100:.3f}%)")
                    raise CycleTimeError(f"Maximum cycle time exceeded ({self.lastRuntime:.3f}s/{self.cycleTime:.3f}s - {(self.lastRuntime/self.cycleTime)*100.0:.3f}%, maximum {(self.maximumTime/self.cycleTime)*100:.3f}%)")
                elif self.lastRuntime >= self.cycleTime:
                    self.cycleTimeWarning = True
                    self.logger.warning(f"The last runtime exceeded the cycle time ({self.lastRuntime:.3f}s/{self.cycleTime:.3f}s - {(self.lastRuntime/self.cycleTime)*100.0:.3f}%, maximum {(self.maximumTime/self.cycleTime)*100:.3f}%)")
                else:
                    self.logger.debug(f"Task executed ({self.lastRuntime}s - {(self.lastRuntime/self.cycleTime)*100.0:.3f}%, maximum {(self.maximumTime/self.cycleTime)*100:.3f}%)")
                    self.cycleTimeWarning = False
            
            while time.time() < (self.lastExecutionTime + self.cycleTime):
                pass

    def start(self) -> None:
        """
        Start the timed task.
        """
        self.stopThread = False
        self.logger.info(f"Timed task \"{self.name}\" started")
        return super().start()
    
    def stop(self) -> None:
        """
        Send a stop request to the timed task
        """
        self.logger.info(f"Timed task \"{self.name}\" stop requested")
        self.stopThread = True

    def task(task) -> None:
        """
        The implementation of the task to execute. This method must be override.

        Raises
        ------
        NotImplementedError
            The method was not overrided.
        """
        raise NotImplementedError("The method \"task\" must be override")