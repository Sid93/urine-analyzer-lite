#pragma once
#include <Arduino.h>

// ── I2C ──────────────────────────────────────────────────────────────────────
#define PIN_SDA   21
#define PIN_SCL   22

// ── Motor & encoder (N20 + MX1508) ───────────────────────────────────────────
#define PIN_MOTOR_IN1  18
#define PIN_MOTOR_IN2   8
#define PIN_ENC_A      15
#define PIN_ENC_B       7

// ── Limit switches (INPUT_PULLUP, active LOW) ────────────────────────────────
#define PIN_LIMIT_HOME 10
#define PIN_LIMIT_END  11

// ── LED illumination (PWM) ────────────────────────────────────────────────────
#define PIN_LED_PWM     2
#define LED_PWM_CHAN    0
#define LED_PWM_FREQ    5000
#define LED_PWM_RES     8    // 8-bit: 0–255

// ── UV-C enable (active HIGH) ─────────────────────────────────────────────────
#define PIN_UVC_EN      3
#define UVC_STERILIZE_MS  10000   // 10 s exposure

// ── HX711 load cell ──────────────────────────────────────────────────────────
#define PIN_HX711_DT    4
#define PIN_HX711_SCK   5

// ── UART: thermal printer (CSN-A2) ──────────────────────────────────────────
#define PIN_PRINTER_TX  6
#define PIN_PRINTER_RX 19
#define PRINTER_BAUD    9600

// ── UART: debug / log ────────────────────────────────────────────────────────
#define SERIAL_BAUD     115200

// ── UI button ────────────────────────────────────────────────────────────────
#define PIN_SCAN_BTN    9    // INPUT_PULLUP, active LOW

// ── ADS1115 ──────────────────────────────────────────────────────────────────
#define ADS_ADDR        0x48
#define ADS_GAIN        1    // ±4.096 V

// ── TCS34725 I2C addresses ────────────────────────────────────────────────────
// Both default to 0x29; use TCA9548A mux or address pin if needed.
// Firmware multiplexes by enabling the LED on only one sensor at a time.
#define TCS_ADDR        0x29

// ── SHT31 ────────────────────────────────────────────────────────────────────
#define SHT31_ADDR      0x44

// ── BH1750 ───────────────────────────────────────────────────────────────────
#define BH1750_ADDR     0x23  // ADDR pin = GND

// ── Motor positioning ─────────────────────────────────────────────────────────
#define MOTOR_SPEED_HOME   150   // PWM duty for homing (0–255)
#define MOTOR_SPEED_SCAN   100   // PWM duty during scan
#define TICKS_PER_PAD       80   // encoder ticks per reagent pad (~2 mm)
#define NUM_PADS            10   // standard 10-pad dipstick

// ── Calibration ───────────────────────────────────────────────────────────────
#define CAL_R_WHITE    255
#define CAL_G_WHITE    255
#define CAL_B_WHITE    255

// ── Diagnostics ───────────────────────────────────────────────────────────────
struct PadResult {
    uint8_t  pad;
    uint16_t r, g, b, c;
    float    hue, sat, val;
    char     analyte[24];
    char     result[16];
};
