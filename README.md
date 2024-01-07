[![GitHub](https://img.shields.io/github/license/ThunderTecke/CyclicTask)](https://github.com/ThunderTecke/CyclicTask/blob/develop/LICENSE)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/ThunderTecke/CyclicTask)](https://github.com/ThunderTecke/CyclicTask/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/ThunderTecke/CyclicTask)](https://github.com/ThunderTecke/CyclicTask/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/ThunderTecke/CyclicTask)](https://github.com/ThunderTecke/CyclicTask/commits)
[![GitHub issues](https://img.shields.io/github/issues/ThunderTecke/CyclicTask)](https://github.com/ThunderTecke/CyclicTask/issues)
![Python version](https://img.shields.io/badge/Python-v3.11-blue)

# CyclicTask <!-- omit in toc -->
Allow a task to be executed regulary

## Table of content <!-- omit in toc -->
- [Installation](#installation)
- [`ContinuousTask` class usage](#continuoustask-class-usage)
  - [Minimum usage](#minimum-usage)
  - [Maximum execution time](#maximum-execution-time)
- [`TimedTask` class](#timedtask-class)
  - [Minimum usage](#minimum-usage-1)
  - [Maximum execution time](#maximum-execution-time-1)

## Installation

```bash
python3 -m pip install CyclicTask
```

## `ContinuousTask` class usage
### Minimum usage

The `ContinuousTask` class allow to execute a task as fast as possible, until the stop request.

```Python
from CyclicTask.ContinuousTask import ContinuousTask

# Sub-classing `ContinuousTask` class
class Task(ContinuousTask):
    # override `task` function
    def task(self) -> None:
        # --- Task definition ---
        pass

# Task creation
task = Task()

# Task start
task.start()

# Task stop
task.stop()

# Waiting for the end of the current cycle
task.join()
```

### Maximum execution time
`maximumTime` parameter allow to monitor the execution duration of one cycle. 

If this one exceed 80% of `maximumTime` the attribut `cycleTimeWarning` is set for one cycle, and a message in the logger is written.

If the duration exceed `maximumTime` the exception `CycleTimeError` is raised, and a message is written in the logger.

```Python
from CyclicTask.ContinuousTask import ContinuousTask

# Sub-classing `ContinuousTask` class
class Task(ContinuousTask):
    # override `task` function
    def task(self) -> None:
        # --- Task definition ---
        pass

# Task creation with `maximumTime` set to 1 second
task = Task(maximumTime = 1.0)

# Task start
task.start()

# Task stop
task.stop()

# Waiting for the end of the current cycle
task.join()
```

## `TimedTask` class
### Minimum usage
The `TimedTask` class allow to execute a task every x seconds, until the stop request.

```Python
from CyclicTask.TimedTask import TimedTask

# Sub-classing `TimedTask` class
class Task(TimedTask):
    # override `task` function
    def task(task) -> None:
        # --- Task definition ---
        pass

# Task creation with `cycleTime` set to 1 second
task = Task(cycleTime = 1.0)

# Task start
task.start()

# Task stop
task.stop()

# Waiting for the end of the current cycle
task.join()
```

### Maximum execution time
`maximumTime` parameter allow to monitor the execution duration of one cycle.
If `maximumTime` is left to None, the maximum execution time is set to 150% of the cycle time.

If this one exceed 80% of `maximumTime` the attribut `cycleTimeWarning` is set for one cycle, and a message in the logger is written.

If the duration exceed `maximumTime` the exception `CycleTimeError` is raised, and a message is written in the logger.

```Python
from CyclicTask.TimedTask import TimedTask

# Sub-classing `TimedTask` class
class Task(TimedTask):
    # override `task` function
    def task(task) -> None:
        # --- Task definition ---
        pass

# Task creation with `cycleTime` set to 1 second, and `maximumTime` set to 1.0 second
task = Task(cycleTime = 1.0, maximumTime = 1.0)

# Task start
task.start()

# Task stop
task.stop()

# Waiting for the end of the current cycle
task.join()
```