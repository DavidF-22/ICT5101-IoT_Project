// Definitions ---
#define MOISTURE_SENSOR A3

int max = 0;
int min = 1023;

// Setup & Loop ---
void setup() {
  Serial.begin(9600);

  pinMode(MOISTURE_SENSOR, INPUT);

  delay(1000);
} // setup()

void loop() {
  int sensorValue = analogRead(MOISTURE_SENSOR);

  if (sensorValue > max) {
    max = sensorValue;  // in damp soil
  }

  if (sensorValue < min) {
    min = sensorValue;
  }

  Serial.print(">> Raw: ");
  Serial.print(sensorValue);
  Serial.print(" | Max: ");
  Serial.print(max);
  Serial.print(" | Min: ");
  Serial.print(min);
  Serial.println();

  delay(500);
} // loop()