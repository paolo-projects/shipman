from shipman.scraper import BaseScraper
from shipman.shipment import Shipment, ShipmentStep
import requests


class DhlScraper(BaseScraper):
    url: str = "https://www.dhl.com/shipmentTracking"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'host': 'www.dhl.com'
    }

    def scrape(self, tracking: str) -> None:
        r = requests.get(self.url,
                          params={'AWB': tracking, 'countryCode':'g0', 'languageCode':'en'},
                         headers=self.headers)
        if not (200 <= r.status_code <= 399):
            raise ConnectionError('Bad response status code: %d' % r.status_code)

        try:
            response = r.json()

            if not response or not response['results'] or len(response['results']) == 0:
                raise LookupError('No data available')

            response = response['results'][0]

            self.shipment = Shipment()
            self.shipment.code = response['id']
            self.shipment.date = response['signature']['description']
            self.shipment.departure = response['origin']['value']
            self.shipment.arrival = response['destination']['value']
            self.shipment.steps = []

            for checkpoint in response['checkpoints']:
                step = ShipmentStep()
                step.time = checkpoint['date'] + checkpoint['time']
                step.location = checkpoint['location']
                step.message = checkpoint['description']
                self.shipment.steps.append(step)

            # Status updates are ordered bottom (oldest) to top (latest)
            # We reverse it so you can have a quicker look at the latest status
            self.shipment.steps.reverse()
        except:
            raise LookupError('Bad response data')

    @staticmethod
    def get_arg_name() -> str:
        return "dhl"
