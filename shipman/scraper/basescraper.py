from shipman.shipment import Shipment
from typing import Optional


class BaseScraper:
    shipment: Optional[Shipment] = None

    def scrape(self, tracking: str) -> None:
        pass

    def get_shipment(self) -> Optional[Shipment]:
        return self.shipment

    @staticmethod
    def get_arg_name() -> str:
        pass
