from scraper.basescraper import BaseScraper
from shipment import Shipment, ShipmentStep
from utils.unquote import unquote
import re
import requests


class GlsScraper(BaseScraper):
    url: str = "https://www.gls-italy.com/it/servizi-per-destinatari/dettaglio-spedizione"
    detailsPattern = re.compile(
        r'<h3>DETTAGLIO SPEDIZIONE</h3>.+<td><b>N. Spedizione:</b>.+?<span>(.+?)</span>.+?<b>Data Partenza:</b>.+?'
        r'<span>(.+?)</span>.+<td><b>Sede Mittente:</b></td>.+?<span>(.+?)</span>.+<td><b>Destinatario:</b></td>.+?'
        r'<span>\s+(.+?)</span>.+<h3>ESITO SPEDIZIONE</h3>.+?<tr>.+?</tr>', re.DOTALL)
    recursivePattern = re.compile(
        r'<tr>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?<td>(.+?)</td>.*?</tr>', re.DOTALL)

    def scrape(self, tracking: str) -> None:
        r = requests.post(self.url,
                          data={'numero_spedizione': tracking, 'tipo_codice': 'nazionale', 'mode': 'search',
                                'tabelle_memorizzate': 1, 'filtro_codice': 0, 'pagina': 1, 'reclast': ''})
        if not (200 <= r.status_code <= 399):
            raise ConnectionError('Bad response status code: %d' % r.status_code)

        response = r.text
        m = self.detailsPattern.search(response)

        if not m:
            raise LookupError('No data available')

        self.shipment = Shipment()
        self.shipment.code = unquote(m.group(1)).strip()
        self.shipment.date = unquote(m.group(2)).strip()
        self.shipment.departure = unquote(m.group(3)).strip()
        self.shipment.arrival = unquote(m.group(4)).strip()
        self.shipment.steps = []

        for m2 in self.recursivePattern.finditer(response[m.end():]):
            step = ShipmentStep()
            step.time = unquote(m2.group(1)).strip()
            step.location = unquote(m2.group(2)).strip()
            step.message = unquote(m2.group(3)).strip()
            self.shipment.steps.append(step)

        # Status updates are ordered bottom (oldest) to top (latest)
        # We reverse it so you can have a quicker look at the latest status
        self.shipment.steps.reverse()

    @staticmethod
    def get_arg_name() -> str:
        return "gls"
