#pragma once
#include <Arduino.h>
#include "config.h"

/*
 * Pad classification via HSV hue comparison against reference colour
 * tables for standard 10-pad dipstick reagent chemistry.
 *
 * Reference hue ranges are illustrative; actual calibration required
 * on physical device using known positive/negative standards.
 */

struct PadSpec {
    uint8_t  pad;
    const char *analyte;
    // Expected hue ranges: [neg_lo, neg_hi] = negative, [pos_lo, pos_hi] = positive
    float neg_lo, neg_hi;
    float pos_lo, pos_hi;
    const char *neg_label;
    const char *pos_label;
};

static const PadSpec PAD_TABLE[10] = {
    {1,  "Leukocytes",    50,80,  90,140, "Negative",  "Positive"},
    {2,  "Nitrites",      55,85,  0,30,   "Negative",  "Positive"},
    {3,  "Urobilinogen",  55,85,  20,50,  "Normal",    "Abnormal"},
    {4,  "Protein",       55,85,  10,40,  "Negative",  "Positive"},
    {5,  "pH",            30,70,  70,130, "5.0-6.0",   "7.0-9.0"},
    {6,  "Blood",         55,85,  90,150, "Negative",  "Positive"},
    {7,  "SpGravity",     55,85,  45,80,  "1.005",     "1.030"},
    {8,  "Ketones",       55,85,  20,55,  "Negative",  "Positive"},
    {9,  "Bilirubin",     55,85,  20,50,  "Negative",  "Positive"},
    {10, "Glucose",       55,85,  100,160,"Negative",  "Positive"},
};

void classify_pad(PadResult &res, float hue) {
    const PadSpec &spec = PAD_TABLE[res.pad - 1];
    snprintf(res.analyte, sizeof(res.analyte), "%s", spec.analyte);

    bool neg = (hue >= spec.neg_lo && hue <= spec.neg_hi);
    bool pos = (hue >= spec.pos_lo && hue <= spec.pos_hi);

    if (pos)       snprintf(res.result, sizeof(res.result), "%s", spec.pos_label);
    else if (neg)  snprintf(res.result, sizeof(res.result), "%s", spec.neg_label);
    else           snprintf(res.result, sizeof(res.result), "Indeterminate");
}
