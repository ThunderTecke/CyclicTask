import threading
import time
from .CycleTimeError import CycleTimeError
import logging

class ContinuousTask(threading.Thread):
    """
    A task exectued continuously with a runtime monitoring. If this runtime exceed the maximum an exception will raise.

    Parameters
    ----------
    maximumTime : float | None, default = None
        The maximum runtime, if exceed an "CycleTimeError" exception will raise.
        If None the monitoring will be disabled
    name : str | None, default = None
        Thread name, if None a default name will be choose.
    """
    def __init__(self, maximumTime: float | None = None, name: str | None = None) -> None:
        super().__init__(name=name)

        # Attributes
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

        self.logger.info(f"Continuous task \"{self.name}\" created")
    
    def run(self) -> None:
        """
        Execute continuously the method "task" and monitor the runtime.

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
                self.logger.debug(f"Task executed ({self.lastRuntime}s")
                self.cycleTimeWarning = False
            else:
                if self.lastRuntime >= self.maximumTime: # The cycle time has exceeded the maximum cycle time
                    self.cycleTimeWarning = False
                    self.logger.error(f"Maximum cycle time exceeded ({self.lastRuntime:.3f}s/{self.maximumTime:.3f}s - {(self.lastRuntime/self.maximumTime)*100.0:.3f}%)")
                    raise CycleTimeError(f"Maximum cycle time exceeded ({self.lastRuntime:.3f}s/{self.maximumTime:.3f}s - {(self.lastRuntime/self.maximumTime)*100.0:.3f}%)")
                elif self.lastRuntime >= (self.maximumTime * 0.8): # The cycle time has exceed 80% of the maximum cycle time
                    self.cycleTimeWarning = True
                    self.logger.debug(f"Task executed ({self.lastRuntime}s - {(self.lastRuntime/self.maximumTime)*100.0:.3f}%)")
                    self.logger.warning(f"80% of the maximum cycle time exceeded ({self.lastRuntime:.3f}s/{self.maximumTime:.3f}s - {(self.lastRuntime/self.maximumTime)*100.0:.3f}%)")
                else:
                    self.logger.debug(f"Task executed ({self.lastRuntime}s - {(self.lastRuntime/self.maximumTime)*100.0:.3f}%)")
                    self.cycleTimeWarning = False
        
        self.logger.info(f"Continuous task \"{self.name}\" stopped")

    def start(self) -> None:
        """
        Start the continuous task.
        """
        self.stopThread = False
        self.logger.info(f"Continuous task \"{self.name}\" started")
        return super().start()

    def stop(self):
        """
        Send a stop request to the continuous task
        """
        self.logger.info("Continuous task \"{self.name}\" stop requested")
        self.stopThread = True

    def task(self) -> None:
        """
        The implementation of the task to execute. This method must be override.

        Raises
        ------
        NotImplementedError
            The method was not overrided.
        """
        raise NotImplementedError("The method \"task\" must be override")