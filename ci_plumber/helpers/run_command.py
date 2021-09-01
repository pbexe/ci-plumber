import subprocess
from time import sleep

from rich.console import Console
from rich.traceback import install

install(show_locals=True)


def run_command(command: str) -> str:
    """Runs a command and returns the output.

    Args:
        command (str): The command to run.

    Returns:
        str: STDOUT of the command.
    """
    sleep(2)  # Most commands seem to benefit from this delay
    console = Console()
    output = subprocess.run(command.split(), capture_output=True, text=True)

    try:
        output.check_returncode()
    except subprocess.CalledProcessError:
        console.log("[bold red]Command failed:[/bold red]")
        console.log(output.stderr)
        # console.print_exception(show_locals=True)
    return output.stdout + output.stderr
