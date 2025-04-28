import logging

from .engine import BaseEngine

logger = logging.getLogger("PyEngine")


class PyEngine(BaseEngine):

    def __init__(self, **kwargs):
        super().__init__()
        del kwargs

    def install_package(self, error_str: str):
        import re
        import subprocess

        match = re.search(r"No module named '(.*)'\s*$", error_str)

        if not match:
            logger.warning(f"No module name in error str : {error_str}")
            return

        missing_module = match.group(1)

        result = subprocess.run(["pip", "install", missing_module])
        logger.info(f"install module result : {result}")

        return

    def run(self, code: str, **kwargs):
        """
        the code is python code, and we use the PyEngine
        to run this code and get the output
        :param code: the function, use the str to define
        :param kwargs: the function's input argument
        """
        namespace = {}

        exec(code, globals(), namespace)

        # must ensure the code only have one function
        if len(namespace.keys()) != 1:
            raise ValueError

        _, func = namespace.popitem()

        try_execute_cnt = 0

        while True:
            try:
                result = func(**kwargs)
                break
            except ModuleNotFoundError as e:
                # install the module
                self.install_package(error_str=str(e))
                try_execute_cnt += 1
            except TypeError:
                # got an unexpected keyword argument
                raise TypeError
            except Exception as e:
                raise

            if try_execute_cnt >= 5:
                raise RuntimeError

        return result
