from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])

  def update(self, CC, CS, now_nanos):
    can_sends = []

    if CS.cam_disp_values and CS.cam_tsr_values and CS.cam_ldw_values:
      can_sends += ldw_tsr_suppress(self.packer, CS.cam_disp_values, CS.cam_tsr_values, CS.cam_ldw_values)

    self.frame += 1
    return CC.actuators, can_sends


def ldw_tsr_suppress(packer, cam_disp_values, cam_tsr_values, cam_ldw_values):
  disp_values = {sig: int(val) for sig, val in cam_disp_values.items()}
  disp_values["SPEED_LIMIT"] = 145 # kph
  disp_values["B1_LOW"] |= 0x06 # directionless ldw event? unclear
  disp_values["LL_CROSSING_LEFT"] = 0
  disp_values["LL_CROSSING_RIGHT"] = 0
  disp_values["LL_DETECTED_LEFT"] = 0
  disp_values["LL_DETECTED_RIGHT"] = 0
  disp_values["B2"] &= 0xBB # bits 2+6 laneish, unclear
  # disp_values["B3"] &= 0xF7
  # disp_values["B4"] &= 0xF7
  # disp_values["B6"] &= 0xFA

  tsr_values = {sig: int(val) for sig, val in cam_tsr_values.items()}
  tsr_values["SPEED_LIMIT"] = disp_values["SPEED_LIMIT"]

  ldw_values = {sig: int(val) for sig, val in cam_ldw_values.items()}
  ldw_values["LANE_CROSSING"] = 0

  return [packer.make_can_msg("FRONT_CAMERA_DISP", 0, disp_values),
          packer.make_can_msg("FRONT_CAMERA_TSR", 0, tsr_values),
          packer.make_can_msg("FRONT_CAMERA_LDW", 0, ldw_values)]
