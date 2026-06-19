from opendbc.can import CANParser
from opendbc.car import Bus, structs
from opendbc.car.interfaces import CarStateBase
from opendbc.car.cameron.values import DBC


class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

    self.cam_disp_values: dict = {}
    self.cam_alert_values: dict = {}

  def update(self, can_parsers) -> structs.CarState:
    cp_pt = can_parsers[Bus.pt]
    cp_cam = can_parsers[Bus.cam]
    ret = structs.CarState()

    ret.vEgo = cp_pt.vl["VEHICLE_SPEED"]["SPEED"] / 3.6
    ret.standstill = ret.vEgo < 0.1

    ret.gas = cp_pt.vl["DRIVER_INPUTS"]["THROTTLE_POSITION"]
    ret.gasPressed = ret.gas > 0.25 # %

    ret.steeringAngleDeg = cp_pt.vl["DRIVER_INPUTS"]["STEERING_ANGLE"]

    self.cam_disp_values = cp_cam.vl["FRONT_CAMERA_DISP"]
    self.cam_alert_values = cp_cam.vl["FRONT_CAMERA_ALERT"]

    return ret

  @staticmethod
  def get_can_parsers(CP):
    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], [], 0),
      Bus.cam: CANParser(DBC[CP.carFingerprint][Bus.pt], [], 2),
    }
