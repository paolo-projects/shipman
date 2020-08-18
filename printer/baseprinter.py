from shipment import Shipment


class BasePrinter:
    def print(self, shipment: Shipment) -> None:
        pass

    @staticmethod
    def get_arg_name() -> str:
        pass
