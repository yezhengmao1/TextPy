from .vm import BaseVM


class TVM(BaseVM):
    def __init__(self):
        super().__init__()

    def __call__(self, func):
        print(func)
