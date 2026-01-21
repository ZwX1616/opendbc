from opendbc.car import PlatformConfig, Platforms, CarSpecs

CANBUS = 1

class CAR(Platforms):
  PORSCHE_911_997_2_CARRERA_S_COUPE_RWD = PlatformConfig(
    [],
    CarSpecs(mass=1455., wheelbase=2.35, steerRatio=13.7, centerToFrontRatio=0.62),
    {CANBUS: 'porsche_997_DRIVE_CAN_R8'},
  )

DBC = CAR.create_dbc_map()
