from abc import ABC, abstractmethod
from pylogger import projectLogger

class WeatherUtilityAbstract(ABC):

    def __init__(self, apikey):
        self.log = projectLogger()
        self._apikey = apikey
        super().__init__()
