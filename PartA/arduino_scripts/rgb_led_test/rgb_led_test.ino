// Definitions ---
#define RGB_RED_PIN 2       // PWM Pin
#define RGB_GREEN_PIN 3     // PWM Pin
#define RGB_BLUE_PIN 4      // PWM Pin
#define MOISTURE_SENSOR A3

void setColourRGB(int red, int green, int blue) {
  analogWrite(RGB_RED_PIN, red);
  analogWrite(RGB_GREEN_PIN, green);
  analogWrite(RGB_BLUE_PIN, blue);
}

void setColourLED() {
  setColourRGB(0, 50, 0);  // R_MIN = 128 | G_MIN = 50 | B_MIN = 128
  delay(2000);

  setColourRGB(128, 50, 0);  // R_MIN = 128 | G_MIN = 50 | B_MIN = 128
  delay(2000);

  setColourRGB(128, 0, 0);  // R_MIN = 128 | G_MIN = 50 | B_MIN = 128
  delay(2000);

  setColourRGB(255, 255, 255);
  delay(2000);
}

void setup() {
  // RGB LED
  pinMode(RGB_RED_PIN, OUTPUT);
  pinMode(RGB_GREEN_PIN, OUTPUT);
  pinMode(RGB_BLUE_PIN, OUTPUT);

  setColourRGB(0, 0, 0);
}

void loop() {
  // put your main code here, to run repeatedly:
  setColourLED();
}
