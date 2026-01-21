#!/usr/bin/env python3
from opendbc.car import structs
from opendbc.car.interfaces import CarInterfaceBase
from opendbc.car.mock.carcontroller import CarController
from opendbc.car.porsche.carstate import CarState


class CarInterface(CarInterfaceBase):
  CarState = CarState
  CarController = CarController

  @staticmethod
  def _get_params(ret: structs.CarParams, candidate, fingerprint, car_fw, alpha_long, is_release, docs) -> structs.CarParams:
    ret.brand = "porsche"
    return ret
