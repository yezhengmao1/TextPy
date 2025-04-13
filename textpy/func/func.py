import inspect
from typing import TYPE_CHECKING, Callable, Dict, Optional

if TYPE_CHECKING:
    from vm import VM


class Func(type):
    registry_: Dict[str, "BaseFunc"] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name not in mcs.registry_:
            mcs.registry_[name] = cls
        return cls

    def __class_getitem__(cls, name):
        if name not in cls.registry_:
            raise NotImplementedError
        return cls.registry_[name]


class BaseFunc(metaclass=Func):
    fn_: Callable

    fn_name_: str
    fn_file_: str
    fn_source_: str

    override_arg_: Optional[Callable]
    override_ret_: Optional[Callable]

    # The function will run in the Text Virtual Machine(TVM).
    runtime_: "VM"

    cache_: Optional[str]

    constant_: bool

    def __init__(
        self,
        fn: Callable,
        *,
        override_arg: Optional[Callable] = None,
        override_ret: Optional[Callable] = None,
        runtime: "VM" = None,
        cache: Optional[str] = ".cache",
        constant: bool = False,
        **kwargs,
    ):
        """
        Func class
        :param fn: the wrapped function
        :param desc: the functions' description
        :param override_arg: the function to override the input, if None use the default
        :param override_ret: the function to override the output, if None use the default
        :param runtime: the runtime for run the function
        :param cache: the directory for compiler cache the compile result
        :param constant: whether the function can be optimized
        """
        assert callable(fn)

        self.fn_ = fn

        self.fn_name_ = fn.__name__
        self.fn_file_ = inspect.getfile(self.fn_)
        self.fn_source_ = inspect.getsource(self.fn_)

        self.override_arg_ = override_arg
        self.override_ret_ = override_ret

        self.runtime_ = runtime

        self.cache_ = cache

        self.constant_ = constant

        # check the signature, we only support the keyworld only parameters
        for _, param in inspect.signature(self.fn_).parameters.items():
            if param.kind != inspect.Parameter.KEYWORD_ONLY:
                raise ValueError(
                    "We only support the keyword only parameters for llm better understand your code."
                    + " The function signature should like func(*, arg1: str) -> str"
                )

        del kwargs

    def __call__(self, **kwargs):
        assert self.runtime_ is not None

        return self.runtime_(self, **kwargs)

    def set_runtime(self, runtime: "VM"):
        self.runtime_ = runtime

    def copy_runtime(self, func: "BaseFunc"):
        self.runtime_.copy(func.runtime_)

    def set_override_ret(self, func: Callable):
        self.override_ret_ = func

    def set_override_arg(self, func: Callable):
        self.override_arg_ = func
