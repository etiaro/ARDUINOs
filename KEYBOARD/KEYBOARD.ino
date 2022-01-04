#include "MIDIUSB.h"

int outPins[] = {1, 0, 2, 3, 4, 5, 6, 7};
int inPins[] = {21, 20, 19, 18, 15, 14, 16, 10};
int potPin = 8;
int btnPin = 9;


int state[64];
int potState = 0;
int btnState = 0;//0 - none, 1 - pressed DOWN, 2 - pressed UP

int firstKey = 36;


void noteOn(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOn);
}
void noteOff(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOff);
}
void sendPitchBend(byte channel, byte control, byte value){
  midiEventPacket_t event = {0x0B, 0xE0 | channel, control, value};
  MidiUSB.sendMIDI(event);
}

int calculateBend(int potVal){//0-127
  //min - ~160
  //max - ~640
  //avg - ~420
  if(potVal > 400 && potVal < 440) return 64;
  if(potVal < 420){
    int val = -0.2423076923076923*potVal+165.76923076923077;
    if(val >= 122) return 127;
    return val;
  }else{
    int val = -0.2909090909090909*potVal+186.1818181818182;
    if(val <= 5) return 0;
    return val;
  }
}


void setup() {
  for(int i = 0; i < 8; i++)
      pinMode(outPins[i], OUTPUT);
  for(int i = 0; i < 8; i++)
      pinMode(inPins[i], INPUT);

  for(int i = 0; i < 61; i++)
    state[i] = false;
}

void loop() {
  //Handling keyboard
  for(int i = 0; i < 8; i++){
    digitalWrite(outPins[i], HIGH);
    delay(1); //TODO check if its nessesary
    for(int j = 0; j < 8; j++){
      bool pressed = digitalRead(inPins[j]) == HIGH;
      if(pressed != state[8*i+j]){
        state[8*i+j] = pressed;
        if(pressed){
          noteOn(0, 8*i+j + firstKey, 64);//channel 0(TODO make to all?)
        }else{
          noteOff(0, 8*i+j + firstKey, 64);//channel 0(TODO make to all?)
        }
      }
    }
    digitalWrite(outPins[i], LOW);
  }

  //handling PitchBend
  int bend=calculateBend(analogRead(potPin));
  if(potState != bend){
    sendPitchBend(0, 0, bend);
  }
  potState = bend;

  //handling buttons
  int btnVal = analogRead(9);
  if(btnVal < 900){
    btnState = 0;
  }else if(btnVal < 980){
    if(btnState != 1){
      firstKey -= 12;
      if(firstKey < 0) firstKey = 0;
      else{
        //MOVING pressed keys down by 12 steps
        for(int i = 0; i < 64; i++)
          if(state[i]){
            noteOff(0, i + firstKey + 12, 64);//channel 0(TODO make to all?)
            noteOn(0, i + firstKey, 64);//channel 0(TODO make to all?)
          }
      }
    }
    btnState = 1;
  }else{
    if(btnState != 2){
      firstKey += 12;
      if(firstKey > 60) firstKey = 60;
      else{
        //MOVING pressed keys up by 12 steps
        for(int i = 0; i < 64; i++)
          if(state[i]){
            noteOff(0, i + firstKey - 12, 64);//channel 0(TODO make to all?)
            noteOn(0, i + firstKey, 64);//channel 0(TODO make to all?)
          }
      }
    }
    btnState = 2;
  }
  MidiUSB.flush();
}
