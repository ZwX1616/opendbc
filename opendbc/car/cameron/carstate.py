from opendbc.can import CANParser
from opendbc.car import Bus, structs
from opendbc.car.interfaces import CarStateBase
from opendbc.car.cameron.values import DBC


class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

    self.tsr_stock_values: dict = {}

  def update(self, can_parsers) -> structs.CarState:
    cp_cam = can_parsers[Bus.cam]
    ret = structs.CarState()

    self.tsr_stock_values = cp_cam.vl["TSR"]

    return ret

  @staticmethod
  def get_can_parsers(CP):
    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], [], 0),
      Bus.cam: CANParser(DBC[CP.carFingerprint][Bus.pt], [], 2),
    }
