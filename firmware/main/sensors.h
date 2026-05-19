#pragma once
#include <Wire.h>
#include <Adafruit_TCS34725.h>
#include <Adafruit_ADS1X15.h>
#include <Adafruit_SHT31.h>
#include <BH1750.h>
#include <HX711.h>
#include "config.h"

// ── Globals ───────────────────────────────────────────────────────────────────
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_50MS, TCS34725_GAIN_4X);
Adafruit_ADS1115  ads;
Adafruit_SHT31    sht31;
BH1750            bh1750;
HX711             scale;

// ── Init ──────────────────────────────────────────────────────────────────────
bool sensors_init() {
    bool ok = true;

    if (!tcs.begin(TCS_ADDR, &Wire)) {
        Serial.println("[WARN] TCS34725 not found");
        ok = false;
    }

    ads.setGain(GAIN_ONE);
    if (!ads.begin(ADS_ADDR, &Wire)) {
        Serial.println("[WARN] ADS1115 not found");
        ok = false;
    }

    if (!sht31.begin(SHT31_ADDR, &Wire)) {
        Serial.println("[WARN] SHT31 not found");
        ok = false;
    }

    bh1750.begin(BH1750::CONTINUOUS_HIGH_RES_MODE, BH1750_ADDR, &Wire);

    scale.begin(PIN_HX711_DT, PIN_HX711_SCK);
    scale.set_scale(420.0f);  // calibration factor — adjust per unit
    scale.tare();

    return ok;
}

// ── RGB reading (averaged over 4 samples) ────────────────────────────────────
void read_rgb(uint16_t &r, uint16_t &g, uint16_t &b, uint16_t &c) {
    uint32_t sr=0, sg=0, sb=0, sc=0;
    for (int i = 0; i < 4; i++) {
        uint16_t tr, tg, tb, tc;
        tcs.getRawData(&tr, &tg, &tb, &tc);
        sr+=tr; sg+=tg; sb+=tb; sc+=tc;
        delay(10);
    }
    r = sr/4; g = sg/4; b = sb/4; c = sc/4;
}

// ── Normalise raw RGB against white calibration ───────────────────────────────
void normalise_rgb(uint16_t r, uint16_t g, uint16_t b, uint16_t c,
                   float &rn, float &gn, float &bn) {
    if (c == 0) { rn=gn=bn=0; return; }
    rn = (float)r / c;
    gn = (float)g / c;
    bn = (float)b / c;
}

// ── RGB → HSV (hue 0–360) ────────────────────────────────────────────────────
void rgb_to_hsv(float r, float g, float b, float &h, float &s, float &v) {
    float mx = max(r, max(g, b));
    float mn = min(r, min(g, b));
    float d  = mx - mn;
    v = mx;
    s = (mx == 0) ? 0 : d / mx;
    if (d == 0) { h = 0; return; }
    if (mx == r) h = 60.0f * fmodf((g - b) / d, 6.0f);
    else if (mx == g) h = 60.0f * ((b - r) / d + 2.0f);
    else              h = 60.0f * ((r - g) / d + 4.0f);
    if (h < 0) h += 360.0f;
}

// ── Environment ───────────────────────────────────────────────────────────────
float read_temperature()  { return sht31.readTemperature(); }
float read_humidity()     { return sht31.readHumidity(); }
float read_lux()          { return bh1750.readLightLevel(); }

float read_weight_grams() {
    if (!scale.is_ready()) return -1.0f;
    return scale.get_units(5);
}

float read_ntc_celsius() {
    int16_t raw = ads.readADC_SingleEnded(0);
    float v = ads.computeVolts(raw);
    // Steinhart–Hart simplified for 10kΩ NTC, β=3950, Vcc=3.3V
    float r = 10000.0f * v / (3.3f - v);
    float lnR = log(r / 10000.0f);
    float T = 1.0f / (1.0f/298.15f + lnR / 3950.0f);
    return T - 273.15f;
}
