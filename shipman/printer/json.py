from shipman.printer.base import BasePrinter
from shipman.shipment import Shipment


class JsonPrinter(BasePrinter):

    def print(self, shipment: Shipment):
        print(shipment.json())

    @staticmethod
    def get_arg_name() -> str:
        return "json"
