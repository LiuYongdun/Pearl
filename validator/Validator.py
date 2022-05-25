from abc import ABCMeta, abstractmethod
from typing import List


class Validator(metaclass=ABCMeta):

    def __init__(self, sql_elements):
        self.sql_elements: List = sql_elements

    @abstractmethod
    def validate(self):
        pass


