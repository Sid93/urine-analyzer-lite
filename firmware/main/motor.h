#pragma once
#include <Arduino.h>
#include "config.h"

volatile long enc_ticks = 0;

void IRAM_ATTR enc_isr() {
    enc_ticks += (digitalRead(PIN_ENC_B) == HIGH) ? 1 : -1;
}

void motor_init() {
    pinMode(PIN_MOTOR_IN1, OUTPUT);
    pinMode(PIN_MOTOR_IN2, OUTPUT);
    ledcSetup(1, 20000, 8);          // channel 1 for motor PWM
    ledcAttachPin(PIN_MOTOR_IN1, 1);

    pinMode(PIN_ENC_A, INPUT_PULLUP);
    pinMode(PIN_ENC_B, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(PIN_ENC_A), enc_isr, RISING);

    pinMode(PIN_LIMIT_HOME, INPUT_PULLUP);
    pinMode(PIN_LIMIT_END,  INPUT_PULLUP);
}

void motor_stop() {
    ledcWrite(1, 0);
    digitalWrite(PIN_MOTOR_IN2, LOW);
}

// Forward = away from home; duty 0–255
void motor_forward(uint8_t duty) {
    digitalWrite(PIN_MOTOR_IN2, LOW);
    ledcWrite(1, duty);
}

// Reverse = toward home
void motor_reverse(uint8_t duty) {
    digitalWrite(PIN_MOTOR_IN2, HIGH);
    ledcWrite(1, 255 - duty);
}

// Drive to home position; returns false if limit not hit within timeout_ms
bool motor_home(uint32_t timeout_ms = 10000) {
    enc_ticks = 0;
    uint32_t t0 = millis();
    motor_reverse(MOTOR_SPEED_HOME);
    while (digitalRead(PIN_LIMIT_HOME) == HIGH) {
        if (millis() - t0 > timeout_ms) { motor_stop(); return false; }
        delay(5);
    }
    motor_stop();
    enc_ticks = 0;
    delay(100);
    return true;
}

// Move forward by n_ticks encoder counts; returns false on end-limit hit
bool motor_move_ticks(long n_ticks, uint32_t timeout_ms = 15000) {
    long target = enc_ticks + n_ticks;
    uint32_t t0 = millis();
    motor_forward(MOTOR_SPEED_SCAN);
    while (enc_ticks < target) {
        if (digitalRead(PIN_LIMIT_END) == LOW) { motor_stop(); return false; }
        if (millis() - t0 > timeout_ms)        { motor_stop(); return false; }
        delay(2);
    }
    motor_stop();
    return true;
}
