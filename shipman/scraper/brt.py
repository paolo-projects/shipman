from shipman.scraper.base import BaseScraper
from shipman.shipment import Shipment, ShipmentStep
from shipman.utils.unquote import unquote
import re
import requests


class BrtScraper(BaseScraper):
    url: str = "https://as777.brt.it/vas/sped_det_show.htm"
    detailsPattern = re.compile(
        r'<tr>.*?<td class="bold">.*?<label id="diz_232" title="Mittente">Mittente</label>.*?</td>.*?<td>(.+?)</td>.*?'
        r'</tr>.*?<tr>.*?<td class="bold">.*?<label id="diz_115" title="Destinatario">Destinatario</label>.*?</td>.*?'
        r'<td>(.+?)</td>.*?</tr>', re.DOTALL)
    recursivePattern = re.compile(
        r'<tr >.*?<td style="white-space: nowrap; width: 1%">(.+?)</td>.*?<td style="white-space: nowrap; width: 1%">'
        r'(.+?)</td>.*?<td style="text-align: left; width: 35%">(.+?)</td>.*?<td style="text-align: left;">(.+?)</td>'
        r'.*?</tr>', re.DOTALL)

    def scrape(self, tracking: str) -> None:
        params = {}
        if len(tracking) == 19:
            params["brtCode"] = tracking
        elif len(tracking) == 12:
            params["Nspediz"] = tracking
        else:
            raise ValueError("Tracking number unsupported. BRT supports 12 digits and 16 digits tracking numbers")

        r = requests.get(self.url, params=params)
        if not (200 <= r.status_code <= 399):
            raise ConnectionError('Bad response status code: %d' % r.status_code)

        response = r.text
        m = self.detailsPattern.search(response)

        if not m:
            raise LookupError('No data available')

        self.shipment = Shipment()
        self.shipment.code = "/"
        self.shipment.date = "/"
        self.shipment.departure = unquote(m.group(1)).strip()
        self.shipment.arrival = unquote(m.group(2)).strip()
        self.shipment.steps = []

        for m2 in self.recursivePattern.finditer(response[m.end():]):
            step = ShipmentStep()
            step.time = unquote(m2.group(1)).strip() + ", " + unquote(m2.group(2)).strip()
            step.location = unquote(m2.group(3)).strip()
            step.message = unquote(m2.group(4)).strip()
            self.shipment.steps.append(step)

        # Status updates are ordered bottom (oldest) to top (latest)
        # We reverse it so you can have a quicker look at the latest status
        self.shipment.steps.reverse()

    @staticmethod
    def get_arg_name() -> str:
        return "brt"
