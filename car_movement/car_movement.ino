// Motor Pins
const int ENA = 5;   // Left motor speed
const int IN1 = 2;   // Left motor forward
const int IN2 = 3;   // Left motor backward
const int ENB = 6;   // Right motor speed
const int IN3 = 4;   // Right motor forward
const int IN4 = 7;   // Right motor backward

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.begin(9600);  // Start serial communication
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == '1') {
      moveForward();
    } else if (command == '0') {
      stopCar();
    }
  }
}

void moveForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150); // Adjust speed
  analogWrite(ENB, 150);
}

void stopCar() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
