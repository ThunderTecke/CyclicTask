import importlib.metadata

__version__ = importlib.metadata.version("CyclicTask")
__author__ = "ThunderTecke <thunder.tecke@gmail.com>"
__all__=["ContinuousTask", "TimedTask", "CycleTimeError"]