 #include <Servo.h>

Servo servos[6];
const int servoPins[6] = {1, 2, 3, 4, 5, 6}; // Base, Thumb, Index, Middle, Ring, Pinky

String inputString = "";
float fingerPositions[6] = {0, 0, 0, 0, 0, 0};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 6; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(90); // Center position
  }
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      parseAndMove(inputString);
      inputString = "";
    } else {
      inputString += inChar;
    }
  }
}

void parseAndMove(String data) {
  int idx = 0;
  int lastIndex = 0;
  for (int i = 0; i < 6; i++) {
    idx = data.indexOf(',', lastIndex);
    String valueStr;
    if (idx == -1 && i == 5) {
      valueStr = data.substring(lastIndex);
    } else {
      valueStr = data.substring(lastIndex, idx);
      lastIndex = idx + 1;
    }
    fingerPositions[i] = valueStr.toFloat();
    // Map 0.0-1.0 to servo angle (e.g., 0-180)
    int angle = map(fingerPositions[i] * 100, 0, 100, 0, 180);
    servos[i].write(angle);
  }
}
