from typing import Callable, Optional

from ..func import Func
from ..vm import VM


def jit(
    fn: Optional[Callable],
    func: str,
    vm: str,
    **kwargs,
) -> Func:
    """
    Create a Func class
    :param fn: the wrapped function
    :param func: the register wrapperd function class
    :param vm: the virtual machine for execution
    :param kwargs: pass the argument to the virtual machine and func
    """

    def decorator(fn: Callable) -> Func:
        assert callable(fn)
        return Func[func](
            fn,
            runtime=VM[vm](**kwargs),
            **kwargs,
        )

    if fn is not None:
        return decorator(fn)

    return decorator


def code(
    fn: Optional[Callable] = None,
    func: str = "CodeFunc",
    vm: str = "CodeVM",
    **kwargs,
) -> Func:
    """
    Create a CodeFunc class
    :param fn: the wrapped function
    :param func: the register wrapperd function class
    :param vm: the virtual machine for execution
    :param kwargs: pass the argument to the virtual machine and func
    """
    return jit(fn, func=func, vm=vm, **kwargs)


def text(
    fn: Optional[Callable] = None,
    func: str = "TextFunc",
    vm: str = "TextVM",
    **kwargs,
) -> Func:
    """
    Create a TextFunc class
    :param fn: the wrapped function
    :param func: the register wrapperd function class
    :param vm: the virtual machine for execution
    :param kwargs: pass the argument to the virtual machine and func
    """
    return jit(fn, func=func, vm=vm, **kwargs)
