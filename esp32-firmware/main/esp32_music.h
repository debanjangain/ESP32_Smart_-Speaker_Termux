#pragma once

// =======================
// Wi-Fi + Backend Config
// =======================
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASS "YOUR_WIFI_PASSWORD"
#define SERVER_URI "ws://192.168.1.100:8765"

// =======================
// 🎤 INMP441 I2S Microphone
// =======================
// Hardware wiring:
// VDD → 3.3V
// GND → GND
// L/R → GND
#define MIC_SD   GPIO_NUM_8    // Serial Data
#define MIC_WS   GPIO_NUM_46   // Word Select (LRCLK)
#define MIC_SCK  GPIO_NUM_9    // Serial Clock

// =======================
// 🔊 MAX98357A I2S Amplifier
// =======================
// Hardware wiring:
// VIN → 5V
// GND → GND
// GAIN → GND
#define AMP_LRC  GPIO_NUM_10   // LRCLK
#define AMP_DIN  GPIO_NUM_3    // Data In
#define AMP_BCLK GPIO_NUM_11   // Bit Clock
