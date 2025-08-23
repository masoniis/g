from functools import lru_cache

from rich.console import Console


@lru_cache
class GLogger:
    console: Console = Console(log_time=True)
    econsole: Console = Console(log_time=True, stderr=True)

    def e(
        self,
        *values: object,
        sep: str = " ",
        end: str = "\n",
    ) -> None:
        self.econsole.log(
            *values,
            sep=sep,
            end=end,
            style="red",
            log_locals=True,
            _stack_offset=2,
        )

    def i(
        self,
        *values: object,
        sep: str = " ",
        end: str = "\n",
    ) -> None:
        self.console.log(
            *values,
            sep=sep,
            end=end,
            style="blue",
            _stack_offset=2,
        )


glog = GLogger()
