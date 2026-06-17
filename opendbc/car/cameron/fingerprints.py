from opendbc.car.cameron.values import CAR

FINGERPRINTS = {
  CAR.GR_CAMRY: [{
    16: 8, 32: 8, 35: 8, 48: 8, 53: 8, 64: 8, 67: 8, 69: 8, 80: 8, 83: 8, 85: 8,
    112: 8, 117: 8, 128: 8, 138: 8, 144: 8, 146: 8, 149: 8, 154: 8, 160: 8, 165: 8,
    168: 8, 170: 8, 181: 8, 240: 8, 464: 8, 480: 8, 528: 8, 608: 8, 1337: 8, 1407: 4,
  },],
}

FW_VERSIONS: dict[str, dict[tuple, list[bytes]]] = {
}
