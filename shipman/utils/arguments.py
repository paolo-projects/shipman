from typing import Tuple, List
from shipman.scraper import scrapers
from shipman.printer import printers
import argparse
from argparse import Namespace
import argcomplete


def build_options() -> Tuple[List[str], List[str]]:
    scrapers_args = []
    for s in scrapers:
        scrapers_args.append(s)

    printers_args = []
    for p in printers:
        printers_args.append(p)
    return scrapers_args, printers_args


def require_arguments() -> Namespace:
    scraper_args, printer_args = build_options()

    ap = argparse.ArgumentParser(description="Get the tracking info from one of the supported services")

    argcomplete.autocomplete(ap)

    ap.add_argument("-p", "--printer", type=str, choices=printer_args, default=printer_args[0], required=False,
                    help="The printer to use. Defaults to pretty")
    ap.add_argument("-s", "--service", type=str, choices=scraper_args, required=True,
                    help="The service to search the status on")
    ap.add_argument("tracking_number", type=str)

    return ap.parse_args()