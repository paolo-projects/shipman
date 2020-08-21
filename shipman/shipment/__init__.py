from typing import List
import json


class ShipmentStep:
    time: str
    location: str
    message: str

    def json(self) -> str:
        return json.dumps({
            'time': self.time,
            'location': self.location,
            'message': self.message
        })

    def dict(self) -> dict:
        return {
            'time': self.time,
            'location': self.location,
            'message': self.message
        }


class Shipment:
    code: str
    date: str
    departure: str
    arrival: str
    steps: List[ShipmentStep]

    def dict(self) -> dict:
        return {
            'code': self.code,
            'date': self.date,
            'departure': self.departure,
            'arrival': self.arrival,
            'steps': list(map(lambda x: x.dict(), self.steps))
        }

    def json(self) -> str:
        return json.dumps(self.dict())
