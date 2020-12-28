import os

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')