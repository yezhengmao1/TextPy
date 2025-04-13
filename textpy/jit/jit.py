from typing import Callable, Optional

from ..compiler import Compiler
from ..func import TextFunc


class JIT:
    compiler_: Compiler

    def __init__(self, fn: Callable, **kwargs):
        pass

    def __call__(self, *args, **kwds):
        pass


def jit(fn: Optional[Callable] = None, **kwargs):
    def decorator(fn: Callable) -> JIT:
        assert callable(fn)
        return JIT(fn, **kwargs)

    if fn is not None:
        return decorator(fn)

    return decorator


def text(fn: Optional[Callable] = None, **kwargs):
    def decorator(fn: Callable) -> TextFunc:
        assert callable(fn)
        return TextFunc(fn, **kwargs)

    if fn is not None:
        return decorator(fn)

    return decorator
