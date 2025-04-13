from typing import Callable, Optional

from ..func import Func, TextFunc
from ..vm import TextVM


def text(
    fn: Optional[Callable] = None,
    func: str = "TextFunc",
    runtime: TextVM = TextVM(),
    **kwargs,
):
    """
    Create a Func class
    :param fn: the wrapped function
    :param func: the register wrapperd function class
    """

    def decorator(fn: Callable) -> TextFunc:
        assert callable(fn)
        return Func[func](fn, runtime=runtime, **kwargs)

    if fn is not None:
        return decorator(fn)

    return decorator
