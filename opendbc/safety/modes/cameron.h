#pragma once

#include "opendbc/safety/declarations.h"
#include "opendbc/safety/modes/defaults.h"

static bool cameron_tx_hook(const CANPacket_t *msg) {
  SAFETY_UNUSED(msg);
  return true;
}

static safety_config cameron_init(uint16_t param) {
  static const CanMsg CAMERON_TX_MSGS[] = {
    {0x45, 0, 8, .check_relay = true},
    {0xB5, 0, 8, .check_relay = true},
    {0x210, 0, 8, .check_relay = true},
  };

  SAFETY_UNUSED(param);
  return (safety_config){NULL, 0, CAMERON_TX_MSGS,
                         sizeof(CAMERON_TX_MSGS) / sizeof(CAMERON_TX_MSGS[0]), false}; // NOLINT(readability/braces)
}

const safety_hooks cameron_hooks = {
  .init = cameron_init,
  .rx = default_rx_hook,
  .tx = cameron_tx_hook,
};
