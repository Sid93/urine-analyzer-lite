/*
 * Urine Analyzer Lite — Main Firmware
 * Target: ESP32-S3-DevKitC-1 (Arduino ESP32 core ≥ 2.0.14)
 *
 * Required libraries (install via Arduino Library Manager):
 *   Adafruit TCS34725      >= 1.4.2
 *   Adafruit ADS1X15       >= 2.5.0
 *   Adafruit SHT31         >= 2.2.2
 *   BH1750                 >= 1.3.0
 *   HX711 by bogde         >= 0.7.5
 *
 * Board settings:
 *   Board     : ESP32S3 Dev Module
 *   Flash     : 8MB
 *   PSRAM     : OPI PSRAM
 *   USB Mode  : Hardware CDC and JTAG
 */

#include <Wire.h>
#include "config.h"
#include "sensors.h"
#include "motor.h"
#include "analysis.h"
#include "printer.h"

// ── State machine ─────────────────────────────────────────────────────────────
enum State { IDLE, HOMING, SCANNING, PRINTING, STERILIZING, ERROR_STATE };
static State state = IDLE;

// ── Scan results ──────────────────────────────────────────────────────────────
static PadResult results[NUM_PADS];
static uint8_t   pad_count = 0;

// ── LED PWM ───────────────────────────────────────────────────────────────────
void led_init() {
    ledcSetup(LED_PWM_CHAN, LED_PWM_FREQ, LED_PWM_RES);
    ledcAttachPin(PIN_LED_PWM, LED_PWM_CHAN);
    ledcWrite(LED_PWM_CHAN, 0);
}

void led_set(uint8_t duty) { ledcWrite(LED_PWM_CHAN, duty); }

// ── UV-C control ──────────────────────────────────────────────────────────────
void uvc_init()   { pinMode(PIN_UVC_EN, OUTPUT); digitalWrite(PIN_UVC_EN, LOW); }
void uvc_on()     { digitalWrite(PIN_UVC_EN, HIGH); }
void uvc_off()    { digitalWrite(PIN_UVC_EN, LOW); }

// ── Scan button ───────────────────────────────────────────────────────────────
void btn_init()   { pinMode(PIN_SCAN_BTN, INPUT_PULLUP); }
bool btn_pressed() { return digitalRead(PIN_SCAN_BTN) == LOW; }

// ── Single-pad scan ───────────────────────────────────────────────────────────
void scan_pad(uint8_t pad_idx) {
    led_set(200);
    delay(50);  // settle

    uint16_t r, g, b, c;
    read_rgb(r, g, b, c);
    led_set(0);

    float rn, gn, bn;
    normalise_rgb(r, g, b, c, rn, gn, bn);

    float h, s, v;
    rgb_to_hsv(rn, gn, bn, h, s, v);

    PadResult &res = results[pad_idx];
    res.pad = pad_idx + 1;
    res.r = r; res.g = g; res.b = b; res.c = c;
    res.hue = h; res.sat = s; res.val = v;

    classify_pad(res, h);

    Serial.printf("[PAD %2d] %s → %s  (H=%.1f S=%.2f V=%.2f)\n",
                  res.pad, res.analyte, res.result, h, s, v);
}

// ── Full scan sequence ────────────────────────────────────────────────────────
bool run_scan() {
    Serial.println("[SCAN] Homing...");
    if (!motor_home()) {
        Serial.println("[ERR] Homing failed");
        return false;
    }
    delay(200);

    pad_count = 0;
    for (uint8_t i = 0; i < NUM_PADS; i++) {
        Serial.printf("[SCAN] Moving to pad %d\n", i + 1);
        if (!motor_move_ticks(TICKS_PER_PAD)) {
            Serial.printf("[WARN] Motor end-stop at pad %d\n", i + 1);
            break;
        }
        delay(100);
        scan_pad(i);
        pad_count++;
    }

    motor_home();
    return pad_count > 0;
}

// ── Print report ──────────────────────────────────────────────────────────────
void print_report() {
    float temp    = read_temperature();
    float humidity= read_humidity();
    float weight  = read_weight_grams();
    printer_report(results, pad_count, temp, humidity, weight);
}

// ── UV-C sterilization cycle ──────────────────────────────────────────────────
void sterilize() {
    Serial.println("[UVC] Sterilization start");
    uvc_on();
    delay(UVC_STERILIZE_MS);
    uvc_off();
    Serial.println("[UVC] Sterilization done");
}

// ── Setup ─────────────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(SERIAL_BAUD);
    delay(500);
    Serial.println("\n=== Urine Analyzer Lite ===");

    Wire.begin(PIN_SDA, PIN_SCL);
    Wire.setClock(400000);

    led_init();
    uvc_init();
    btn_init();
    motor_init();
    printer_init();

    if (!sensors_init()) {
        Serial.println("[WARN] Some sensors missing — check wiring");
    }

    Serial.println("[OK] Ready. Press scan button to begin.");
    state = IDLE;
}

// ── Loop ──────────────────────────────────────────────────────────────────────
void loop() {
    switch (state) {
        case IDLE:
            if (btn_pressed()) {
                delay(50);  // debounce
                if (btn_pressed()) {
                    float w = read_weight_grams();
                    if (w < 1.0f) {
                        Serial.println("[WARN] No sample detected. Place cup on scale.");
                        delay(2000);
                        break;
                    }
                    Serial.printf("[INFO] Sample %.1f g detected. Starting scan.\n", w);
                    state = HOMING;
                }
            }
            break;

        case HOMING:
            state = SCANNING;
            break;

        case SCANNING:
            if (run_scan()) {
                state = PRINTING;
            } else {
                Serial.println("[ERR] Scan failed");
                state = ERROR_STATE;
            }
            break;

        case PRINTING:
            print_report();
            state = STERILIZING;
            break;

        case STERILIZING:
            sterilize();
            Serial.println("[OK] Cycle complete. Remove strip. Ready.");
            state = IDLE;
            break;

        case ERROR_STATE:
            led_set(128);
            delay(500);
            led_set(0);
            delay(500);
            if (btn_pressed()) { state = IDLE; }
            break;
    }
}
