#define DIR_PIN 2
#define STEP_PIN 3
#define POT_PIN 26

void setup() {
  Serial.begin(115200);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(POT_PIN, INPUT);
  digitalWrite(STEP_PIN, LOW);
}

void loop() {
  int value = analogRead(POT_PIN);
  Serial.println(value);
  int delayValue = map(value, 0, 1023, 1, 10);
  if (value == 0) {
    Serial.print("Stopped");
  } else {
    digitalWrite(DIR_PIN, HIGH);
    for (int i = 0; i < 200; i++) {
      digitalWrite(STEP_PIN, HIGH);
      delayMicroseconds(500);
      digitalWrite(STEP_PIN, LOW);
      delay(delayValue);
    }
  } 
  delay(10);
}
