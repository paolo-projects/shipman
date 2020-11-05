from typing import Callable


console_colors = {
    'PURPLE': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'CYAN': '\033[96m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}


def purple(text: str) -> str:
    return "%s%s" % (console_colors['PURPLE'], text)


def blue(text: str) -> str:
    return "%s%s" % (console_colors['OKBLUE'], text)


def green(text: str) -> str:
    return "%s%s" % (console_colors['OKGREEN'], text)


def orange(text: str) -> str:
    return "%s%s" % (console_colors['WARNING'], text)


def cyan(text: str) -> str:
    return "%s%s" % (console_colors['CYAN'], text)


def red(text: str) -> str:
    return "%s%s" % (console_colors['FAIL'], text)


def bold(text: str) -> str:
    return "%s%s" % (console_colors['BOLD'], text)


def underline(text: str) -> str:
    return "%s%s" % (console_colors['UNDERLINE'], text)


def colorize(text: str, *colors: Callable[[str], str]) -> str:
    text_col = text
    for color in colors:
        text_col = color(text)
    return text_col + console_colors['ENDC']

