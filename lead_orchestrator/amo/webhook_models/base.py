from pydantic import BaseModel
from typing import Any

from abc import ABC, abstractmethod
class CustomField(BaseModel):
    id: int
    name: str
    values: list[Any]


class BodyPattern(BaseModel, ABC):
    
    @classmethod
    def get_subclasses(cls):
        r = tuple(cls.__subclasses__())
        return r

    @property
    @abstractmethod
    def data(self) -> dict:
        raise NotImplementedError()