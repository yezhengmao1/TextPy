from ..engine import Engine, LMEngine
from ..func import TextFunc
from .vm import BaseVM


class TextVM(BaseVM):
    engine_: LMEngine

    def __init__(
        self,
        *,
        engine: str = "LMEngine",
        **kwargs,
    ):
        super().__init__()
        self.engine_ = Engine[engine](**kwargs)

        del kwargs

    def __call__(self, func: TextFunc, *args, **kwargs):
        """
        Call LLM to generate output just like function
            func(*args, **kwargs)
        :param func: the wrapped function
        :param args: the functions' input
        :param kwargs: the functions' input
        """
        if not isinstance(func, TextFunc):
            raise TypeError("TVM only supported the TextFunc")
        # the args is none
        assert len(args) == 0

        prompt = func.prompt(*args, **kwargs)

        response = self.engine_.run(prompt)

        # TODO: the response must same
        return response
