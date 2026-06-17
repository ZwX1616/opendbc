from opendbc.can import CANPacker
from opendbc.car import Bus
from opendbc.car.interfaces import CarControllerBase


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP):
    super().__init__(dbc_names, CP)
    self.packer = CANPacker(dbc_names[Bus.pt])

  def update(self, CC, CS, now_nanos):
    can_sends = []

    if CS.tsr_stock_values:
      can_sends.append(create_tsr_suppress(self.packer, CS.tsr_stock_values))

    self.frame += 1
    return CC.actuators, can_sends


def create_tsr_suppress(packer, stock_values):
  values = {sig: int(val) for sig, val in stock_values.items()}
  values["TSR_B3"] &= 0xF7
  return packer.make_can_msg("TSR", 0, values)
