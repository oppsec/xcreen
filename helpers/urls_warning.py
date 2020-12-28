from rich.console import Console
console = Console()

def warning_message():
    with open("helpers/files/warning_message.txt", "r") as warn_file:
        get_message = warn_file.read()
        console.input(f"\n[bold red]{get_message}[/]")