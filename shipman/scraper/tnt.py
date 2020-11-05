from shipman.scraper.base import BaseScraper
from shipman.shipment import Shipment, ShipmentStep
import requests
import xml.etree.ElementTree as ET


class TntScraper(BaseScraper):
    url: str = "https://www.tnt.it/tracking/getTrackXML.html"

    def scrape(self, tracking: str) -> None:
        r = requests.post(self.url,
                          data={'wt':1, 'consigNos': tracking, 'autoSearch': '', 'searchMethod': '', 'pageNo': '',
                                'numberText': tracking, 'numberTextArea': '', 'codCli': '', 'tpCod': 'N'})
        if not (200 <= r.status_code <= 399):
            raise ConnectionError('Bad response status code: %d' % r.status_code)

        response = r.text

        xml_doc = ET.fromstring(response)
        consignment = xml_doc.find('Consignment')
        sender_details = consignment.find('SenderDetails')

        send_code = consignment.find('ConNo').text
        departure = f"{sender_details.find('SendZIP').text} - {sender_details.find('SendTown').text} " \
                    f"({sender_details.find('SendProvince').text})"
        send_date = consignment.find('ConsignmentDate').text

        receiver_details = consignment.find('ReceiverDetails')
        destination = f"{receiver_details.find('RcvZIP').text} - {receiver_details.find('RcvTown').text} " \
                      f"({receiver_details.find('RcvProvince').text})"

        self.shipment = Shipment()
        self.shipment.code = send_code
        self.shipment.date = send_date
        self.shipment.departure = departure
        self.shipment.arrival = destination
        self.shipment.steps = []

        for ship_step in consignment.findall('StatusDetails'):
            step = ShipmentStep()
            step.time = ship_step.find('StatusDate').text
            step.location = ship_step.find('Depot').text
            step.message = ship_step.find('StatusDescription').text
            self.shipment.steps.append(step)

        # Status updates are ordered bottom (oldest) to top (latest)
        # We reverse it so you can have a quicker look at the latest status
        self.shipment.steps.reverse()

    @staticmethod
    def get_arg_name() -> str:
        return "tnt"
