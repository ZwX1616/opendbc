#pragma once

#include "opendbc/safety/declarations.h"
#include "opendbc/safety/modes/defaults.h"

static bool cameron_tx_hook(const CANPacket_t *msg) {
  SAFETY_UNUSED(msg);
  return true;
}

static bool cameron_fwd_hook(int bus_num, int addr) {
  // Don't echo our injected camera-replacement frames (sent on bus 0) back onto
  // the camera's bus (bus 2). The camera would see its own message type with our
  // edits and a mismatched counter and fault. Static blocking already drops the
  // camera's originals in the bus2->bus0 direction; this blocks the bus0->bus2
  // direction for the same addresses.
  bool block_msg = false;
  if (bus_num == 0 && ((addr == 0x45) || (addr == 0xB5))) {
    block_msg = true;
  }
  return block_msg;
}

static safety_config cameron_init(uint16_t param) {
  static const CanMsg CAMERON_TX_MSGS[] = {
    {0x45, 0, 8, .check_relay = true},
    {0xB5, 0, 8, .check_relay = true},
  };

  SAFETY_UNUSED(param);
  return (safety_config){NULL, 0, CAMERON_TX_MSGS,
                         sizeof(CAMERON_TX_MSGS) / sizeof(CAMERON_TX_MSGS[0]), false}; // NOLINT(readability/braces)
}

const safety_hooks cameron_hooks = {
  .init = cameron_init,
  .rx = default_rx_hook,
  .tx = cameron_tx_hook,
  .fwd = cameron_fwd_hook,
};
