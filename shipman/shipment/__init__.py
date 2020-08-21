from typing import List, Dict
import json


class ShipmentStep:
    time: str
    location: str
    message: str

    def dict(self) -> Dict:
        return {
            'time': self.time,
            'location': self.location,
            'message': self.message
        }

    def json(self) -> str:
        return json.dumps(self.dict())


class Shipment:
    code: str
    date: str
    departure: str
    arrival: str
    steps: List[ShipmentStep]

    def dict(self) -> Dict:
        return {
            'code': self.code,
            'date': self.date,
            'departure': self.departure,
            'arrival': self.arrival,
            'steps': list(map(lambda x: x.dict(), self.steps))
        }

    def json(self) -> str:
        return json.dumps(self.dict())
