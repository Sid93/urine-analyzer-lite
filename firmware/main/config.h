#pragma once
#include <Arduino.h>

// Pin map = hardware/ENGINEERING_REVIEW.md §3 (master, ESP32-S3, USB-CDC enabled).
// Avoids strapping pins (0/3/45/46), USB pins (19/20), and non-existent S3 pins (22–25).
// PENDING ELECTRONICS-ENGINEER VERIFICATION before PCB layout.

// ── I2C (shared bus: TCA9548A mux, SHT31, BH1750, ADS1115) ───────────────────
#define PIN_SDA    1
#define PIN_SCL    2

// ── Motor & encoder (N20 + MX1508) ───────────────────────────────────────────
#define PIN_MOTOR_IN1   4   // PWM
#define PIN_MOTOR_IN2   5   // PWM
#define PIN_ENC_A       6
#define PIN_ENC_B       7

// ── Limit switches (INPUT_PULLUP, active LOW) ────────────────────────────────
#define PIN_LIMIT_HOME 10
#define PIN_LIMIT_END  11

// ── LED illumination (PWM via 2N7000) ─────────────────────────────────────────
#define PIN_LED_PWM    12
#define LED_PWM_CHAN    0
#define LED_PWM_FREQ    5000
#define LED_PWM_RES     8    // 8-bit: 0–255

// ── UV-C enable (active HIGH; external 10k pull-DOWN → OFF at boot, safety) ───
#define PIN_UVC_EN     13
#define UVC_STERILIZE_MS  10000   // 10 s exposure

// ── HX711 load cell ──────────────────────────────────────────────────────────
#define PIN_HX711_DT   14
#define PIN_HX711_SCK  15

// ── UART1: thermal printer (CSN-A2) ──────────────────────────────────────────
#define PIN_PRINTER_TX 17   // MCU TX → printer RXD
#define PIN_PRINTER_RX 18   // printer TXD → MCU RX
#define PRINTER_BAUD    9600

// ── UART: debug / log ────────────────────────────────────────────────────────
#define SERIAL_BAUD     115200

// ── UI button ────────────────────────────────────────────────────────────────
#define PIN_SCAN_BTN   16    // INPUT_PULLUP, active LOW

// ── Display: SPI TFT 3.5–4.0" (ILI9488/ST7796) + XPT2046 touch (polled) ──────
// Touch shares the SPI bus (SCLK/MOSI/MISO); touch IRQ polled to save a pin.
#define PIN_TFT_SCLK   38
#define PIN_TFT_MOSI   39
#define PIN_TFT_MISO   40   // shared with touch read
#define PIN_TFT_CS     41
#define PIN_TFT_DC     42
#define PIN_TFT_BL     47   // backlight enable / PWM
#define PIN_TOUCH_CS   48
#define PIN_TFT_RST    21

// ── ADS1115 ──────────────────────────────────────────────────────────────────
#define ADS_ADDR        0x48
#define ADS_GAIN        1    // ±4.096 V

// ── I2C mux + TCS34725 ────────────────────────────────────────────────────────
// Two TCS34725 share fixed address 0x29 → each sits behind its own TCA9548A channel.
#define TCA9548A_ADDR   0x70
#define TCS_MUX_CH0     0    // primary RGB sensor
#define TCS_MUX_CH1     1    // secondary / differential RGB sensor
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
