#pragma once
#include <Arduino.h>
#include "config.h"

HardwareSerial PrinterSerial(1);

void printer_init() {
    PrinterSerial.begin(PRINTER_BAUD, SERIAL_8N1, PIN_PRINTER_RX, PIN_PRINTER_TX);
    delay(200);
}

void printer_raw(const uint8_t *buf, size_t len) {
    PrinterSerial.write(buf, len);
}

void printer_println(const char *s) {
    PrinterSerial.println(s);
}

void printer_feed(uint8_t lines = 3) {
    for (uint8_t i = 0; i < lines; i++) PrinterSerial.write('\n');
}

void printer_align_center() {
    const uint8_t cmd[] = {0x1B, 0x61, 0x01};
    printer_raw(cmd, sizeof(cmd));
}

void printer_align_left() {
    const uint8_t cmd[] = {0x1B, 0x61, 0x00};
    printer_raw(cmd, sizeof(cmd));
}

void printer_bold(bool on) {
    const uint8_t cmd[] = {0x1B, 0x45, (uint8_t)(on ? 1 : 0)};
    printer_raw(cmd, sizeof(cmd));
}

void printer_report(PadResult *pads, uint8_t n_pads,
                    float temp, float humidity, float weight_g) {
    printer_align_center();
    printer_bold(true);
    printer_println("LEVRAM URINE ANALYZER LITE");
    printer_bold(false);
    printer_println("---------------------------");

    char buf[48];
    snprintf(buf, sizeof(buf), "Temp: %.1f C   RH: %.0f%%", temp, humidity);
    printer_println(buf);
    snprintf(buf, sizeof(buf), "Sample: %.1f g", weight_g);
    printer_println(buf);
    printer_println("---------------------------");

    printer_align_left();
    printer_bold(true);
    printer_println("Analyte       Result");
    printer_bold(false);
    printer_println("---------------------------");

    for (uint8_t i = 0; i < n_pads; i++) {
        snprintf(buf, sizeof(buf), "%-14s%s", pads[i].analyte, pads[i].result);
        printer_println(buf);
    }

    printer_println("---------------------------");
    printer_align_center();
    printer_println("For clinical use by");
    printer_println("qualified personnel only.");
    printer_feed(4);
}
