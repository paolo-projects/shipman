from shipman.scraper.base import BaseScraper
from shipman.shipment import Shipment, ShipmentStep
import requests
import datetime


class PosteScraper(BaseScraper):
    url: str = "https://www.poste.it/online/dovequando/DQ-REST/ricercasemplice"
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'host': 'www.poste.it',
        'referer': 'https://www.poste.it/cerca/index.html',
        'content-type': 'application/json;charset=utf-8'
    }

    def scrape(self, tracking: str) -> None:
        req = {
            'codiceSpedizione': tracking,
            'periodoRicerca': 1,
            'tipoRichiedente': 'WEB'
        }
        r = requests.post(self.url,
                         json=req,
                         headers=self.headers)

        # PosteItaliane could randomly request a recaptcha verification
        # In that case, the request will fail with a 400 status code
        # There's nothing you can do about it, just hope you are lucky
        #
        # And don't send too many requests one after the other...

        if not (200 <= r.status_code <= 399):
            raise ConnectionError('Bad response status code: %d' % r.status_code)

        try:
            response = r.json()

            if not response:
                raise LookupError('No data available')

            self.shipment = Shipment()
            self.shipment.code = response['idTracciatura']
            self.shipment.date = response['tipoProdotto']
            self.shipment.departure = response['sintesiStato']
            self.shipment.arrival = "/"
            self.shipment.steps = []

            for movement in response['listaMovimenti']:
                step = ShipmentStep()
                unix_time_ms = movement['dataOra']
                dt_time = datetime.datetime.fromtimestamp(unix_time_ms / 1000)
                step.time = dt_time.strftime('%d-%m-%Y %H:%M:%S')
                step.location = movement['luogo']
                step.message = movement['statoLavorazione']
                self.shipment.steps.append(step)

            # Status updates are ordered bottom (oldest) to top (latest)
            # We reverse it so you can have a quicker look at the latest status
            self.shipment.steps.reverse()
        except Exception as e:
            raise LookupError('Bad response data')

    @staticmethod
    def get_arg_name() -> str:
        return "posteit"
