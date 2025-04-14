from typing import Callable, Optional

from ..func import Func, TextFunc
from ..vm import TextVM


def text(
    fn: Optional[Callable] = None,
    func: str = "TextFunc",
    cache: Optional[str] = ".cache",
    engine: str = "LMEngine",
    model: str = "deepseek/deepseek-chat",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs,
):
    """
    Create a Func class
    :param fn: the wrapped function
    :param func: the register wrapperd function class
    :param cache: the cache dir for compiler
    :param engine: the execution engine
    :param model: the engine's model
    :param base_url: the model;s base url
    :param api_key: the model's api_key
    """

    def decorator(fn: Callable) -> TextFunc:
        assert callable(fn)
        runtime: TextVM = TextVM(
            engine=engine,
            model=model,
            base_url=base_url,
            api_key=api_key,
            **kwargs,
        )
        return Func[func](
            fn,
            runtime=runtime,
            cache=cache,
            **kwargs,
        )

    if fn is not None:
        return decorator(fn)

    return decorator
