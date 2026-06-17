from opendbc.car import PlatformConfig, Platforms, CarSpecs, Bus

class CAR(Platforms):
  GR_CAMRY = PlatformConfig(
    [],
    CarSpecs(mass=1470., wheelbase=2.57, steerRatio=16.1, centerToFrontRatio=0.61),
    {Bus.pt: 'cameron_gr_camry'},
  )

DBC = CAR.create_dbc_map()
