from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])
    self.last_tsr_ctr = -1

  def update(self, CC, CS, now_nanos):
    can_sends = []

    if CS.cam_disp_values and CS.cam_tsr_values:
      can_sends.append(disp_suppress(self.packer, CS.cam_disp_values))

      # FRONT_CAMERA_TSR (0xB5) carries a rolling code: byte1 low nibble is a
      # counter (+8 mod 15) and b0/b6/b7 are a counter-keyed table. Re-emitting
      # at our loop rate stalls the counter and faults the car, so forward only
      # one edited copy per new camera frame (i.e. on counter change).
      tsr_ctr = int(CS.cam_tsr_values["B1"]) & 0x0F
      if tsr_ctr != self.last_tsr_ctr:
        self.last_tsr_ctr = tsr_ctr
        can_sends.append(tsr_suppress(self.packer, CS.cam_tsr_values))

    self.frame += 1
    return CC.actuators, can_sends


def disp_suppress(packer, cam_disp_values):
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
  return packer.make_can_msg("FRONT_CAMERA_DISP", 0, disp_values)


def tsr_suppress(packer, cam_tsr_values):
  # mirror the camera frame (preserves the rolling code b0/b1/b6/b7), overwrite
  # only the displayed limit. emitted once per counter change by the caller.
  tsr_values = {sig: int(val) for sig, val in cam_tsr_values.items()}
  tsr_values["SPEED_LIMIT"] = 145 # kph
  return packer.make_can_msg("FRONT_CAMERA_TSR", 0, tsr_values)
