from shipman.scraper.base import BaseScraper
from shipman.shipment import Shipment, ShipmentStep
import re
import requests
import json


class AmazonScraper(BaseScraper):
    url: str = "https://www.amazon.it/progress-tracker/package/ref=ppx_yo_dt_b_track_package"
    detailsPattern = re.compile(
        r'<script type="a-state" data-a-state="{&quot;key&quot;:&quot;page-state&quot;}">(.+?)</script>', re.DOTALL)

    def scrape(self, tracking: str) -> None:
        try:
            item_id, order_id = tracking.split(',')
            if not item_id or len(item_id) == 0 or not order_id or len(order_id) == 0: raise ValueError()
        except ValueError:
            raise ValueError('Invalid arguments provided. '
                             'You need to provide tracking as [item id],[order id]')
        r = requests.get(self.url, params={'_encoding': 'UTF8', 'itemId': item_id, 'orderId': order_id})
        if not (200 <= r.status_code <= 399):
            raise ConnectionError('Bad response status code: %d' % r.status_code)

        response = r.text
        m = self.detailsPattern.search(response)

        if not m:
            raise LookupError('No data available')

        try:
            json_val = json.loads(m.group(1))

            self.shipment = Shipment()
            self.shipment.code = ','.join([item_id, order_id])
            self.shipment.date = '/'
            self.shipment.departure = '/'
            self.shipment.arrival = '/'
            self.shipment.steps = []

            step = ShipmentStep()
            step.time = '/'
            step.location = "%d %%" % json_val['progressTracker']['lastTransitionPercentComplete']
            step.message = "%s: %s" % (json_val['progressTracker']['lastReachedMilestone'],
                                       json_val['promise']['promiseMessage'])
            self.shipment.steps.append(step)
        except:
            raise LookupError('Error while trying to make sense of return data')

    @staticmethod
    def get_arg_name() -> str:
        return "amazon"
