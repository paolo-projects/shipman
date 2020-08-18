from printer.baseprinter import BasePrinter
from shipment import Shipment


class bcolors:
    PURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    CYAN = '\033[96m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        print(('| Tracking: {}{:<'+str(n-14)+'}{} |').format(bcolors.PURPLE,
                                                             shipment.code, bcolors.ENDC))
        print(('| Data: {}{:<'+str(n-10)+'}{} |').format(bcolors.WARNING,
                                                         shipment.date, bcolors.ENDC))
        print(('| Da: {}{:<'+str(n-8)+'}{} |').format(bcolors.CYAN,
                                                      shipment.departure, bcolors.ENDC))
        print(('| A: {}{:<'+str(n-7)+'}{} |').format(bcolors.CYAN,
                                                     shipment.arrival, bcolors.ENDC))
        print('='*n)

        therealmax = 0

        for step in shipment.steps:
            therealmax = max(therealmax, max(50, maxlen(
                step.time, step.location, step.message) + 4))

        for step in shipment.steps:
            n = therealmax
            print('~'*n)
            print(('| {}{:<' + str(n-4) + '}{} |').format(bcolors.WARNING,
                                                          step.time, bcolors.ENDC))
            print(('| {}{:<' + str(n-4) + '}{} |').format(bcolors.CYAN,
                                                          step.location, bcolors.ENDC))
            print(('| {}{}{:<' + str(n-4) + '}{} |').format(bcolors.UNDERLINE,
                                                            bcolors.BOLD, step.message, bcolors.ENDC))

        print('~'*therealmax)

    @staticmethod
    def get_arg_name() -> str:
        return "pretty"
