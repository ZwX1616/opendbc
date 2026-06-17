from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])

  def update(self, CC, CS, now_nanos):
    can_sends = []

    if CS.cam_stock_values:
      can_sends.append(ldw_tsr_suppress(self.packer, CS.cam_stock_values))

    self.frame += 1
    return CC.actuators, can_sends


def ldw_tsr_suppress(packer, stock_values):
  values = {sig: int(val) for sig, val in stock_values.items()}
  values["B3"] &= 0xF7
  values["B5"] &= 0x3F
  return packer.make_can_msg("FRONT_CAMERA", 0, values)
