import abc
from typing import Dict

from ..func import Func


class VM(type):
    registry_: Dict[str, "BaseVM"] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name not in mcs.registry_:
            mcs.registry_[name] = cls
        return cls

    def __class_getitem__(cls, name):
        if name not in cls.registry_:
            raise NotImplementedError
        return cls.registry_[name]


class BaseVM(metaclass=VM):
    @abc.abstractmethod
    def __call__(self, func: Func, **kwargs): ...
