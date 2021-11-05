from colorama import Fore

EChO = [
    ' __________     _________     |           _________',
    '|              |             |           |       |',
    '__________     |             ______      |       |',
    '|              |             |     |     |       |',
    '__________     _________     |     |     _________'
    ]

red = Fore.RED
white = Fore.WHITE
reset = Fore.RESET
blue = Fore.BLUE
cyan = Fore.CYAN
yellow = Fore.YELLOW
magenta = Fore.MAGENTA
green = Fore.GREEN

if __name__ == "__main__":
    print(red + EChO[0] + '\n',
          white + EChO[1] + '\n',
          blue + EChO[2] + '\n',
          cyan + EChO[3] + '\n',
          yellow + EChO[4] + '\n')
    print(magenta + 'EChO Framework 0.1_PRE | YiLinINIC and MixacPROD')