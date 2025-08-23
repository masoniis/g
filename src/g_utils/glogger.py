from functools import lru_cache

from rich.console import Console


class _GMasterLogger:
    len_last_name: int = 0

    _console: Console = Console(log_time=True)
    _econsole: Console = Console(log_time=True, stderr=True)

    def _smart_gutter_prefix(self, name: str) -> tuple[str, ...]:
        len_diff = len(name) - self.len_last_name

        cname = "[cyan b]" + name + " │ [/]"

        if len_diff > 0:
            return (
                "[cyan b]"
                + " " * (self.len_last_name + 1)
                + "└"
                + ("─" * (len_diff - 1))
                + "┐"
                + "[/]\n",
                cname,
            )
        elif len_diff < 0:
            return (
                "[cyan b]"
                + " " * (len(name) + 1)
                + "┌"
                + ("─" * (-len_diff - 1))
                + "┘"
                + "[/]\n",
                cname,
            )
        else:
            return (cname,)

    def e(
        self,
        *values: object,
        sep: str = " ",
        end: str = "",
        name: str = "default",
        style: str = "red",
    ) -> None:
        self._econsole.log(
            *self._smart_gutter_prefix(name),
            *values,
            sep=sep,
            end=end,
            style=style,
            log_locals=True,
            _stack_offset=3,
        )

        self.len_last_name = len(name)

    def i(
        self,
        *values: object,
        sep: str = " ",
        end: str = "",
        name: str = "default",
        style: str = "blue",
    ) -> None:
        prefix = "".join(self._smart_gutter_prefix(name))
        self._console.log(
            prefix,
            *values,
            sep=sep,
            end=end,
            style=style,
            _stack_offset=3,
        )

        self.len_last_name = len(name)


_gLogger = _GMasterLogger()


@lru_cache
class GLogger:
    # Logger state
    name: str
    err_color: str
    log_color: str

    # Internal consoles
    _console: Console = Console(log_time=True)
    _econsole: Console = Console(log_time=True, stderr=True)

    def __init__(
        self, err_color: str = "red", log_color: str = "blue", name: str = "default"
    ) -> None:
        self.err_color = err_color
        self.log_color = log_color
        self.name = name
        pass

    def e(
        self,
        *values: object,
        sep: str = " ",
        end: str = "",
    ) -> None:
        _gLogger.e(
            *values,
            sep=sep,
            end=end,
            name=self.name,
            style=self.err_color,
        )

    def i(
        self,
        *values: object,
        sep: str = " ",
        end: str = "",
    ) -> None:
        _gLogger.i(
            *values,
            sep=sep,
            end=end,
            name=self.name,
            style=self.log_color,
        )


glog = GLogger()
