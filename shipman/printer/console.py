from shipman.printer.base import BasePrinter
from shipman.shipment import Shipment
from shipman.colorize import *


def maxlen(arg1, arg2, *argv):
    maxl = max(len(arg1), len(arg2))
    for arg in argv:
        maxl = max(maxl, len(arg))
    return maxl


class ConsolePrinter(BasePrinter):

    def print(self, shipment: Shipment):
        n = max(50, maxlen(shipment.code, shipment.date,
                           shipment.departure, shipment.arrival)+14)
        print('='*n)
        print(('| Tracking: {:<'+str(n-5)+'} |').format(colorize(shipment.code, purple)))
        print(('| Data: {:<'+str(n-1)+'} |').format(colorize(shipment.date, orange)))
        print(('| Da: {:<'+str(n+1)+'} |').format(colorize(shipment.departure, cyan)))
        print(('| A: {:<'+str(n+2)+'} |').format(colorize(shipment.arrival, cyan)))
        print('='*n)

        therealmax = 0

        for step in shipment.steps:
            therealmax = max(therealmax, max(50, maxlen(
                step.time, step.location, step.message) + 4))

        for step in shipment.steps:
            n = therealmax
            print('~'*n)
            print(('| {:<' + str(n+5) + '} |').format(colorize(step.time, orange)))
            print(('| {:<' + str(n+5) + '} |').format(colorize(step.location, cyan)))
            print(('| {:<' + str(n+4) + '} |').format(colorize(step.message, underline, bold)))

        print('~'*therealmax)

    @staticmethod
    def get_arg_name() -> str:
        return "pretty"
