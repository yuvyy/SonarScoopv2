from colorama import Style, Fore


def info(msg): print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")
def success(msg): print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")
def warning(msg): print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}")
def error(msg): print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")
def prompt(msg): return input(f"{Fore.BLUE}[INPUT]{Style.RESET_ALL} {msg} ").strip()