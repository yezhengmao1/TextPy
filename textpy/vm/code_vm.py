from ..engine import Engine
from ..func import CodeFunc
from .vm import BaseVM


class CodeVM(BaseVM):
    engine_: Engine

    def __init__(
        self,
        *,
        engine: str = "PyEngine",
        **kwargs,
    ):
        super().__init__()
        self.engine_ = Engine[engine](**kwargs)

    def __call__(self, func: CodeFunc, **kwargs):
        """
        Call PyEngine to execute the func
        :param func: the wrapped function
        :param args: the functions' input
        :param kwargs: the functions' input
        """
        if not isinstance(func, CodeFunc):
            raise TypeError("CodeVM only supported the CodeFunc")

        # the code should be only a function
        code = func.code()

        try:
            response = self.engine_.run(code, **kwargs)
        except Exception as e:
            raise

        # TODO: check the response
        # TODO: the response must same with the func's return value
        return response
