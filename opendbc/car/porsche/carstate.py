import copy
from opendbc.can import CANDefine, CANParser
from opendbc.car import Bus, structs
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.interfaces import CarStateBase
from opendbc.car.porsche.values import DBC, CANBUS

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

  def update(self, can_parsers) -> structs.CarState:
    ret = structs.CarState()
    return ret

  @staticmethod
  def get_can_parsers(CP):
    return {
      CANBUS: CANParser(DBC[CP.carFingerprint][CANBUS], [], CANBUS),
    }
