#include <Stepper.h>
#define STEPS 2038 // the number of steps in one revolution of motor (28BYJ-48)

Stepper stepper(STEPS, 8, 10, 9, 11);
int input;

void setup() {
  Serial.begin(9600);
}

void loop() {
  stepper.setSpeed(10); // rpm
  while(Serial.available()){
    input = Serial.read();
  }

  if(input == '1'){
    stepper.step(2038);
  }  
  if(input == '2') {
    stepper.step(-2038);
  }
  input = 0;
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
}
