import sys
from datetime import datetime
from functools import lru_cache
from typing import TextIO

from rich.console import Console


class _GMasterLogger:
    # Consoles
    _console: Console = Console(log_time=True)
    _econsole: Console = Console(log_time=True, stderr=True)

    # Logger state
    len_last_name: int = 0
    last_message: str = ""
    last_message_count: int = 1
    last_name: str = ""
    repeat_line_printed: bool = False

    def _smart_gutter_prefix(
        self, name: str, gutter_str: str = " │ "
    ) -> tuple[str, ...]:
        """Creates a dynamic, correctly aligned gutter prefix for logging."""
        len_diff = len(name) - self.len_last_name
        cname = f"[cyan b]{name}{gutter_str}[/]"

        if len_diff > 0:
            padding = " " * (self.len_last_name + 1)
            dashes = "─" * (len_diff - 1)
            return (f"[cyan b]{padding} └{dashes}┐[/]\n", cname)
        elif len_diff < 0:
            padding = " " * (len(name) + 1)
            dashes = "─" * (-len_diff - 1)
            return (f"[cyan b]{padding} ┌{dashes}┘[/]\n", cname)
        else:
            return (f" {cname}",)

    def _log(
        self,
        console: Console,
        stream: TextIO,
        values: tuple[object, ...],
        sep: str,
        end: str,
        name: str,
        style: str,
        log_locals: bool = False,
    ) -> None:
        """Core logging logic to handle new and repeated messages."""
        current_message = sep.join(str(v) for v in values)

        if current_message == self.last_message and name == self.last_name:
            # Logic for repeated messages
            self.last_message_count += 1

            if self.last_message_count > 2 and self.repeat_line_printed:
                stream.write("\033[1A\033[2K")
                stream.flush()

            timestamp = datetime.now().strftime("%H:%M:%S")
            prefix = "".join(self._smart_gutter_prefix(name, gutter_str=" ├"))

            # The repeat message is always printed to the standard console
            self._console.print(
                f"[cyan dim]\\[{timestamp}][/] [cyan]{prefix}─────▶[/] [b yellow]🔁 {self.last_message_count}x[/]"
            )
            self.repeat_line_printed = True
        else:
            # Logic for new messages
            console.log(
                *self._smart_gutter_prefix(name),
                *values,
                sep=sep,
                end=end,
                style=style,
                log_locals=log_locals,
                _stack_offset=4,
            )

            self.last_message = current_message
            self.last_name = name
            self.last_message_count = 1
            self.repeat_line_printed = False

        self.len_last_name = len(name)

    def e(
        self,
        *values: object,
        sep: str = " ",
        end: str = "",
        name: str = "default",
        style: str = "red",
    ) -> None:
        """Logs an error message to stderr."""
        self._log(
            console=self._econsole,
            stream=sys.stderr,
            values=values,
            sep=sep,
            end=end,
            name=name,
            style=style,
            log_locals=True,
        )

    def i(
        self,
        *values: object,
        sep: str = " ",
        end: str = "",
        name: str = "default",
        style: str = "blue",
    ) -> None:
        """Logs an informational message to stdout."""
        self._log(
            console=self._console,
            stream=sys.stdout,
            values=values,
            sep=sep,
            end=end,
            name=name,
            style=style,
            log_locals=False,
        )


_gLogger = _GMasterLogger()


@lru_cache
class GLogger:
    # Logger state
    name: str
    err_color: str
    log_color: str

    def __init__(
        self, err_color: str = "red", log_color: str = "blue", name: str = "default"
    ) -> None:
        self.err_color = err_color
        self.log_color = log_color
        self.name = name

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
