from typing import Dict


class Engine(type):
    registry_: Dict[str, "BaseEngine"] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name not in mcs.registry_:
            mcs.registry_[name] = cls
        return cls

    def __class_getitem__(cls, name):
        if name not in cls.registry_:
            raise NotImplementedError
        return cls.registry_[name]


class BaseEngine(metaclass=Engine): ...
