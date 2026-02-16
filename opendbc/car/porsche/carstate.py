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

    ret.gas = cp.vl['DME3']['Accel_PDL_Angle']
    ret.engineRpm = cp.vl['DME1']['DME_RPM']

    sa_sign = cp.vl['SCCM1']['SCCM_SteeringAngleSign']
    sa_mag = cp.vl['SCCM1']['SCCM_SteeringAngleMagnitude']
    ret.steeringAngleDeg = 2.0 * (sa_sign - 0.5) * sa_mag

    return ret

  @staticmethod
  def get_can_parsers(CP):
    return {
      Bus.cam: CANParser(DBC[CP.carFingerprint][Bus.cam], [], 1),
    }
