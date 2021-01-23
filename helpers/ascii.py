from rich import print

def print_ascii():
    with open("helpers/files/ascii.txt", "r") as ascii_file:
        get_ascii = ascii_file.read()
        print(f"[bold white]{get_ascii}[/]")