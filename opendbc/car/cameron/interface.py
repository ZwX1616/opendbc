from opendbc.car import get_safety_config, structs
from opendbc.car.cameron.carcontroller import CarController
from opendbc.car.cameron.carstate import CarState
from opendbc.car.interfaces import CarInterfaceBase


class CarInterface(CarInterfaceBase):
  CarState = CarState
  CarController = CarController

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, alpha_long, is_release, docs) -> structs.CarParams:
    ret.brand = "cameron"
    ret.safetyConfigs = [get_safety_config(structs.CarParams.SafetyModel.cameron)]

    ret.dashcamOnly = False
    ret.radarUnavailable = True
    ret.openpilotLongitudinalControl = False

    return ret
