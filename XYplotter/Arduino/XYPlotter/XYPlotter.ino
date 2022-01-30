#include "Stepper.h"
#include "Communication.h"
#include "Plotter.h"

Stepper s(2,3,4,5);
Stepper s2(A0,A1,A2,A3);
Plotter p(s, s2);
Communicator c;//pins 8(RX),9(TX), locks PWM on 10

void setup() {
  s.init();
  s2.init();

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
