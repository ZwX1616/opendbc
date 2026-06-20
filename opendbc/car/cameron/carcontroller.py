from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])
    self.last_alert_ctr = -1
    self.last_ldw_ctr = -1

  def update(self, CC, CS, now_nanos):
    can_sends = []

    if CS.cam_disp_values:
      can_sends.append(cam_disp_suppress(self.packer, CS.cam_disp_values))

    if CS.cam_alert_values:
      alert_ctr = int(CS.cam_alert_values["B1"]) & 0x0F
      if alert_ctr != self.last_alert_ctr:
        self.last_alert_ctr = alert_ctr
        can_sends.append(cam_alert_suppress(self.packer, CS.cam_alert_values))

    if CS.cam_ldw_values:
      ldw_ctr = int(CS.cam_ldw_values["B1"])
      if ldw_ctr != self.last_ldw_ctr:
        self.last_ldw_ctr = ldw_ctr
        can_sends.append(cam_ldw_suppress(self.packer, CS.cam_ldw_values))

    self.frame += 1
    return CC.actuators, can_sends


def cam_disp_suppress(packer, cam_disp_values):
  disp_values = {sig: int(val) for sig, val in cam_disp_values.items()}
  disp_values["SPEED_LIMIT"] = 100
  disp_values["B1_LOW"] |= 0x06 # directionless ldw event? unclear
  disp_values["LL_CROSSING_LEFT"] = 0
  disp_values["LL_CROSSING_RIGHT"] = 0
  disp_values["LL_DETECTED_LEFT"] = 0
  disp_values["LL_DETECTED_RIGHT"] = 0
  disp_values["B2"] &= 0xBB # bits 2+6 laneish, unclear
  # disp_values["B3"] &= 0xF7
  # disp_values["B4"] &= 0xF7
  # disp_values["B6"] &= 0xFA
  return packer.make_can_msg("FRONT_CAMERA_DISP", 0, disp_values)

def cam_alert_suppress(packer, cam_alert_values):
  alert_values = {sig: int(val) for sig, val in cam_alert_values.items()}
  alert_values["TSR_VISUAL"] = 0
  alert_values["TSR_AUDIBLE"] = 0
  alert_values["LDW_AUDIBLE"] = 0
  return packer.make_can_msg("FRONT_CAMERA_ALERT", 0, alert_values)

def cam_ldw_suppress(packer, cam_ldw_values):
  ldw_values = {sig: int(val) for sig, val in cam_ldw_values.items()}
  ldw_values["LANE_CROSSING"] = 0
  return packer.make_can_msg("FRONT_CAMERA_LDW", 0, ldw_values)
