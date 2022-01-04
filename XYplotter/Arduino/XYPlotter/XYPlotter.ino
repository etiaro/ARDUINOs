#include "Stepper.h"
#include "Communication.h"
#include "Plotter.h"

Stepper s(A0,A1,A2,A3);
Stepper s2(9,10,11,12);
Plotter p(s, s2);
Communicator c(2, 3);

void setup() {
  s.init();
  s2.init();
  
  Serial.begin(9600);
  Serial.println("WAITING"); 
  c.init();
  p.init();
}

void loop() {
  Message msg = c.forceReadMessage();
  switch(msg.kind){
    case MessageKind::move:
      p.moveTo(msg.len1, msg.len2);
      break;
    case MessageKind::set:
      p.setPos(msg.len1, msg.len2);
      break;
  }
  c.sendDone();
}
