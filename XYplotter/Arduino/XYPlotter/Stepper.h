const int PHASES[] = {1, 3, 2, 6, 4, 12, 8, 9};

class Stepper{
private:
  int IN1, IN2, IN3, IN4;
  int actPhase;
  int setPhase(int phase){
    actPhase = phase;
    digitalWrite(IN1, (PHASES[actPhase]&1)==1);
    digitalWrite(IN2, (PHASES[actPhase]&2)==2);
    digitalWrite(IN3, (PHASES[actPhase]&4)==4);
    digitalWrite(IN4, (PHASES[actPhase]&8)==8);
  }
public:
  Stepper(int I1, int I2, int I3, int I4){
    IN1 = I1;
    IN2 = I2;
    IN3 = I3;
    IN4 = I4;
    
    actPhase = 0;
  }
  void init(){
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
  }
  void step(bool backwards = false){
    if(backwards){
      setPhase((actPhase - 1 + 8)%8);
    }else{
      setPhase((actPhase + 1 + 8)%8);
    }
  }
};
