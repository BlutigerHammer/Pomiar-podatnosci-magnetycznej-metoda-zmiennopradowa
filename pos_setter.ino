/*
 * Program gets 2 numbers, first-direction (1-clockwise, 0-counter clockwise), second-number of stepper turns
 * Return 1 number-made distance
 */
#include <Stepper.h> 
#define bottomSensorPin 3 
#define topSensorPin 4
#define stepPin 12 
#define dirPin 13
#define STEPS 200
Stepper stepper(STEPS, 12, 13);
int dir; 
int dis;

void setup() {
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  stepper.setSpeed(1000);
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    processData(input);
    int disMade = turn(dir, dis);
    Serial.println(disMade);
    Serial.flush();
  }
}

void processData(String input){
  dir = int(input[0]-'0');
  input.remove(0,1);
  dis = input.toInt();
}

int turn(int dir, int dis){
  /*
   * returns the number of turns stepper has made
   */
  //digitalWrite(dirPin, dir);
  for (int i = 0; i < dis; i++) {
    if (dir==1 && digitalRead(topSensorPin)) return(i);
    if (dir==0 && digitalRead(bottomSensorPin)) return(i);
    stepper.step(4*STEPS);
  }
  return(dis);
}