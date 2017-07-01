#include "thermistor.h"
#include <Wire.h>

#define SLAVE_ADDRESS (0x04)
#define DEBUG (1) // Set to 1 to print Serial messages

int heatPin = 0; // temperature pin
int lightPin = 1;  // LDR pin
float R1 = 9800; // reference resistor in ohms
float R_therm; // thermal resistor in ohms
float R_ldr; // LDR in ohms
float V1; // voltage divider voltage in mV
float V0 = 5000; // input voltage in mV
union {
    float flt;
    byte byts[4];
} T; //temperature in celsius
int i = 0; // iterator variable
int N = 300; // number of loops between serial uploads
int delayMs = 1000; // delay time in ms between arduino actions

void setup()
{
    // Setup serial for debugging
    Serial.begin(9600);
    // Setup arduino as I2C slave
    Wire.begin(SLAVE_ADDRESS);
    // Callback for data request
    Wire.onRequest(requestCallback);
}

void loop()
{
    delay(delayMs);
    R_therm = measSenseR(heatPin, R1);
    R_ldr = measSenseR(lightPin, R1);
    T.flt = calculate_temperature(R_therm);
    if (DEBUG && (i % N == 0)){
        Serial.println(T.flt);
    }
    i += 1;
}

float measSenseR(int pin, float R0)
{
    float V1 = analogRead(pin);
    V1 = map(V1, 0, 1023, 0, V0);
    float R = R0 * (V0 / V1 - 1);
    return R;
}

void requestCallback()
{
    Wire.write(T.byts, 4);
}

