import abc
import inspect
from typing import TYPE_CHECKING, Callable, Dict, Optional

if TYPE_CHECKING:
    from tvm import TVM


class FuncRegister(type):
    registry_: Dict[str, "Func"] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name not in mcs.registry_:
            mcs.registry_[name] = cls
        return cls


class Func(metaclass=FuncRegister):
    fn_: Callable

    fn_name_: str
    fn_file_: str
    fn_source_: str

    # TextPy call llm to generate the understanding of the function
    fn_desc_: str

    override_arg_: Optional[Callable]
    override_ret_: Optional[Callable]

    # The function will run in the Text Virtual Machine(TVM).
    runtime_: "TVM"

    def __init__(
        self,
        fn: Callable,
        *,
        desc: Optional[Callable] = None,
        override_arg: Optional[Callable] = None,
        override_ret: Optional[Callable] = None,
        runtime: "TVM" = None,
        **kwargs,
    ):
        """
        Func class
        :param fn: the wrapped function
        :param desc: the functions' description
        :param override_arg: the function to override the input
        :param override_ret: the function to override the output
        :param runtime: the runtime for run the function
        """
        assert callable(fn)

        self.fn_ = fn

        self.fn_name_ = fn.__name__
        self.fn_file_ = inspect.getfile(self.fn_)
        self.fn_source_ = inspect.getsource(self.fn_)

        self.fn_desc_ = desc

        self.override_arg_ = override_arg
        self.override_ret_ = override_ret

        self.runtime_ = runtime

        del kwargs

    @abc.abstractmethod
    def __call__(self, *args, **kwargs): ...
