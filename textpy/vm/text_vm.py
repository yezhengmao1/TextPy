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

    def __call__(self, func: TextFunc, **kwargs):
        """
        Call LLM to generate output just like function
            func(**kwargs)
        :param func: the wrapped function
        :param args: the functions' input
        :param kwargs: the functions' input
        """
        if not isinstance(func, TextFunc):
            raise TypeError("TextVM only supported the TextFunc")
        # the args is none

        prompt = func.prompt(**kwargs)

        response = self.engine_.run(prompt)

        return response

    def copy(self, runtime: "TextVM"):
        self.engine_.copy(runtime.engine_)
