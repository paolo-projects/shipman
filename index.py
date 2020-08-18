#!/usr/bin/python3
import sys

from scraper import basescraper, scrapers
from printer import baseprinter, printers
from arguments import require_arguments


def main():
    args = require_arguments()
    tracking = args.tracking_number

    shipment_scraper: basescraper.BaseScraper = scrapers[args.service]()

    try:
        shipment_scraper.scrape(tracking)
        shipment = shipment_scraper.get_shipment()
        shipment_printer: baseprinter.BasePrinter = printers[args.printer]()
        shipment_printer.print(shipment)
    except Exception as err:
        print("%s: %s" % (err.__class__.__name__, err.args[0]), file=sys.stderr)


if __name__ == "__main__":
    main()
