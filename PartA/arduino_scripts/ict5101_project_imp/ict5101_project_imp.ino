// Imports ---
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Definitions ---
#define RGB_RED_PIN 2       // PWM Pin
#define RGB_GREEN_PIN 3     // PWM Pin
#define RGB_BLUE_PIN 4      // PWM Pin
#define MOISTURE_SENSOR A3

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Calibration values ---
int dryValue = 0;   // sensor threshold in dry air/soil
int wetValue = 600;   // sensor threshold in water/wet soil

// Helper Functions ---
void drawCenteredText(String text, int y, int size) {

  int16_t x1, y1;
  uint16_t w, h;

  display.setTextSize(size);
  display.getTextBounds(text, 0, 0, &x1, &y1, &w, &h);

  int x = (SCREEN_WIDTH - w) / 2;

  display.setCursor(x, y);
  display.print(text);
}

void displayMC(String text) {
  display.clearDisplay();

  // Title in yellow section (top 16px)
  drawCenteredText("Moisture Content (MC)", 2, 1);
  // Divider line
  display.drawLine(0, 16, 128, 16, WHITE);

  // Meter text in middle
  drawCenteredText(text+"%", 35, 2);
  display.display();
}

void setColourRGB(int red, int green, int blue) {
  analogWrite(RGB_RED_PIN, red);
  analogWrite(RGB_GREEN_PIN, green);
  analogWrite(RGB_BLUE_PIN, blue);
}

void setMoistureColour(int percent) {
  if (percent <= 33) {
    setColourRGB(128, 0, 0);  // Red
  }
  else if (percent <= 66) {
    setColourRGB(128, 50, 0); // Yellow
  }
  else {
    setColourRGB(0, 50, 0);   // Green
  }
}

// Setup & Loop ---
void setup() {
  Serial.begin(9600);
  
  // RGB LED
  pinMode(RGB_RED_PIN, OUTPUT);
  pinMode(RGB_GREEN_PIN, OUTPUT);
  pinMode(RGB_BLUE_PIN, OUTPUT);
  
  // MOISTURE SENSOR
  pinMode(MOISTURE_SENSOR, INPUT);

  // SCREEN
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(">> !!! OLED Not Found !!!");
  }

  // display.setCursor(0, 0);
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);

  delay(1000);
} // setup()

void loop() {
  // setColourRGB(0, 50, 0);  // R_MIN = 128 | G_MIN = 50 | B_MIN = 128
  // displayMC("100");

  // delay(5000);

  // setColourRGB(128, 50, 0);  // R_MIN = 128 | G_MIN = 50 | B_MIN = 128
  // displayMC("50");

  // delay(5000);

  // setColourRGB(128, 0, 0);  // R_MIN = 128 | G_MIN = 50 | B_MIN = 128
  // displayMC("0");

  // delay(5000);
  int sensorValue = analogRead(MOISTURE_SENSOR);

  // convert raw sensor value to percentage & keep between 0 to 100
  int percent  = map(sensorValue, dryValue, wetValue, 0, 100);
  int moisturePercentage = constrain(percent, 0, 100);

  Serial.print("Raw sensor value: ");
  Serial.print(sensorValue);
  Serial.print(" | Moisture: ");
  Serial.print(percent);
  Serial.println("%");

  displayMC(String(moisturePercentage));
  setMoistureColour(moisturePercentage);

  delay(500);

} // loop()