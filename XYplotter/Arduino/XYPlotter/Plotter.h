#include <EEPROM.h>

class Plotter{
private:
  Stepper s1, s2;
  long len1, len2; 
  void moveTogether(long steps1, long steps2, bool backwards1, bool backwards2){
    if(steps1 == 0 && steps2 == 0){
      // nothing to move
    }else if(steps1 == 0){
      for(long step = 0; step < steps2; step++){
        s2.step(backwards2);
        delay(1);
      }
    }else if(steps2 == 0){
      for(long step = 0; step < steps1; step++){
        s1.step(backwards1);
        delay(1);
      }
    }else{
      long totalTime = 1000L*max(steps1, steps2);
      long delayTime = totalTime/steps1/steps2;
      
      for(long step = 0; step < steps1*steps2; step++){
        if(step%steps2 == 0){
          s1.step(backwards1);
        }
        if(step%steps1 == 0){
          s2.step(backwards2);
        }
        
        long skipTo = max(step + 1, min((step/steps1+1)*steps1, (step/steps2+1)*steps2));
        delayMicroseconds(delayTime*(skipTo - step));
        step = skipTo-1;
      }
    }
  }
public:
  Plotter(Stepper &s1, Stepper &s2): s1(s1), s2(s2){}
  void init(){
    len1 = EEPROM.read(0);
    len1 <<=8;
    len1 |= EEPROM.read(1);
    len1 <<=8;
    len1 |= EEPROM.read(2);
    len1 <<=8;
    len1 |= EEPROM.read(3);
    
    len2 = EEPROM.read(4);
    len2 <<=8;
    len2 |= EEPROM.read(5);
    len2 <<=8;
    len2 |= EEPROM.read(6);
    len2 <<=8;
    len2 |= EEPROM.read(7);
  }
  void savePosition(){
    EEPROM.write(0, (len1>>24) % (1<<8));
    EEPROM.write(1, (len1>>16) % (1<<8));
    EEPROM.write(2, (len1>>8) % (1<<8));
    EEPROM.write(3, (len1) % (1<<8));

    EEPROM.write(4, (len2>>24) % (1<<8));
    EEPROM.write(5, (len2>>16) % (1<<8));
    EEPROM.write(6, (len2>>8) % (1<<8));
    EEPROM.write(7, (len2) % (1<<8));
  }
  void setPos(long l1, long l2){
    len1 = l1; len2 = l2;
    savePosition();
  }
  void moveTo(long to1, long to2){ //TODO move from "lenX" to "toX" instead of toX steps
    long steps1 = to1 - len1;
    long steps2 = to2 - len2;

    
    bool backwards1 = steps1 < 0L;
    bool backwards2 = steps2 > 0L;
    if(steps1 < 0) steps1 *= -1;
    if(steps2 < 0) steps2 *= -1;
    
    if(steps1 > 1000 || steps2 > 1000){
      if(steps1 > steps2){
        for(long i = 0; i < steps1/1000; i++){
          moveTogether(1000, steps2*1000/steps1, backwards1, backwards2);
        }
        moveTogether(steps1%1000, steps2%(steps2*1000/steps1), backwards1, backwards2);
      }else{
        for(long i = 0; i < steps2/1000; i++){
          moveTogether(steps1*1000/steps2, 1000, backwards1, backwards2);
        }
        moveTogether(steps1%(steps1*1000/steps2), steps2%1000, backwards1, backwards2);
      }
    }else{
      moveTogether(steps1, steps2, backwards1, backwards2);
    }
    
    len1 = to1;
    len2 = to2;
    savePosition();
  }
};
