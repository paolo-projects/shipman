from shipman.printer.base import BasePrinter
from shipman.printer.console import ConsolePrinter
from shipman.printer.json import JsonPrinter
from shipman.printer.tab import TabPrinter
from typing import Dict, Type


printers: Dict[str, Type[BasePrinter]] = {
    ConsolePrinter.get_arg_name(): ConsolePrinter,
    JsonPrinter.get_arg_name(): JsonPrinter,
    TabPrinter.get_arg_name(): TabPrinter
}