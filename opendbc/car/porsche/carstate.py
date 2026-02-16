import copy
from opendbc.can import CANDefine, CANParser
from opendbc.car import Bus, structs
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.interfaces import CarStateBase
from opendbc.car.porsche.values import DBC

class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

  def update(self, can_parsers) -> structs.CarState:
    cp = can_parsers[Bus.cam]
    ret = structs.CarState()

    ret.brake = cp.vl['PSM4']['PSM_BrakePressure'] # Bars
    ret.brakePressed = cp.vl['PSM1']['PSM_FootBrake2'] > 0.5
    return ret

  @staticmethod
  def get_can_parsers(CP):
    return {
      Bus.cam: CANParser(DBC[CP.carFingerprint][Bus.cam], [], 1),
    }
