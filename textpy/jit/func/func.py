import abc
import inspect
from typing import Callable, Optional

from textpy.tvm import TVM


class Func:
    fn_: Callable

    fn_name_: str
    fn_file_: str
    fn_source_: str

    """
        TextPy call llm to generate the understanding of the function
    """
    fn_desc_: str

    override_arg_: Optional[Callable]
    override_ret_: Optional[Callable]

    runtime_: TVM

    def __init__(self, fn: Callable, **kwargs):
        assert callable(fn)

        self.fn_ = fn

        self.fn_name_ = fn.__name__
        self.fn_source_ = inspect.getsource(self.fn_)
        self.fn_file_ = inspect.getfile(self.fn_)

        self.override_arg_ = None
        self.override_ret_ = None

        self.fn_desc_ = None

        del kwargs

    def set_runtime(self, tvm: TVM):
        self.runtime_ = tvm

    def override_ret(self, fn: Callable = None):
        self.override_ret_ = fn

    def override_arg(self, fn: Callable = None):
        self.override_arg_ = fn

    @abc.abstractmethod
    def __call__(self, *args, **kwargs): ...
