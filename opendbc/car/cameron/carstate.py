from opendbc.can import CANParser
from opendbc.car import Bus, structs
from opendbc.car.interfaces import CarStateBase
from opendbc.car.cameron.values import DBC


class CarState(CarStateBase):
  def __init__(self, CP):
    super().__init__(CP)

    self.cam_disp_values: dict = {}
    self.cam_tsr_values: dict = {}
    self.cam_ldw_values: dict = {}

  def update(self, can_parsers) -> structs.CarState:
    cp_cam = can_parsers[Bus.cam]
    ret = structs.CarState()

    self.cam_disp_values = cp_cam.vl["FRONT_CAMERA_DISP"]
    self.cam_tsr_values = cp_cam.vl["FRONT_CAMERA_TSR"]
    self.cam_ldw_values = cp_cam.vl["FRONT_CAMERA_LDW"]   # 0x210; parsed for observation only - NOT blocked/edited (B5-only test)

    return ret

  @staticmethod
  def get_can_parsers(CP):
    return {
      Bus.pt: CANParser(DBC[CP.carFingerprint][Bus.pt], [], 0),
      Bus.cam: CANParser(DBC[CP.carFingerprint][Bus.pt], [], 2),
    }
