from printer.baseprinter import BasePrinter
from shipment import Shipment


class TabPrinter(BasePrinter):

    def print(self, shipment: Shipment):
        print('{}\t{}\t{}\t{}'.format(
            shipment.code, shipment.date, shipment.departure, shipment.arrival))
        for step in shipment.steps:
            print('{}\t{}\t{}'.format(step.time,
                                      step.location, step.message))

    @staticmethod
    def get_arg_name() -> str:
        return "tab"
