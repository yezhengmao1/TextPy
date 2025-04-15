from .engine import BaseEngine


class PyEngine(BaseEngine):

    def __init__(self, **kwargs):
        super().__init__()
        del kwargs

    def run(self, code: str, **kwargs):
        """
        the code is python code, and we use the PyEngine
        to run this code and get the output
        """
        namespace = {}

        exec(code, globals(), namespace)

        # must ensure the code only have one function
        if len(namespace.keys()) != 1:
            raise ValueError

        _, func = namespace.popitem()

        try:
            result = func(**kwargs)
        except TypeError:
            # got an unexpected keyword argument
            raise TypeError

        return result
