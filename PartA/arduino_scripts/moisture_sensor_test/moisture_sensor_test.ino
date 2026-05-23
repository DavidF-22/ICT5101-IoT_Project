// Definitions ---
#define MOISTURE_SENSOR A3

int maxValue = 0;
int minValue = 1023;

// Setup & Loop ---
void setup() {
  Serial.begin(9600);

  pinMode(MOISTURE_SENSOR, INPUT);

  Serial.println("Soil moisture calibration test");
  Serial.println("Type r in Serial Monitor to reset min/max.");

  delay(1000);
} // setup()

void loop() {
  int sensorValue = analogRead(MOISTURE_SENSOR);

  // Read user input is serial monitor is available
  if (Serial.available()) {
    char command = Serial.read();

    if (command == 'r' || command == 'R') {
      maxValue = 0;
      minValue = 1023;
      Serial.println(">> Min/Max reset");
    }
  }

  if (sensorValue > maxValue) {
    maxValue = sensorValue;  // in damp soil
  }

  if (sensorValue < minValue) {
    minValue = sensorValue;
  }

  Serial.print(">> Raw: ");
  Serial.print(sensorValue);
  Serial.print(" | Max: ");
  Serial.print(maxValue);
  Serial.print(" | Min: ");
  Serial.print(minValue);
  Serial.println();

  delay(500);
} // loop()