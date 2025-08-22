from rich.console import Console

console = Console()


def eprint(*args, **kwargs):
    console.print(*args, **kwargs, style="red")
