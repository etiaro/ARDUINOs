#include <SoftwareSerial.h>

enum MessageKind{
  lift,
  lower,
  move,
  set
};

struct Message{
  MessageKind kind;
  long len1, len2;
};


class Communicator{
private:
  SoftwareSerial BT;
  int r, t;
public:
  Communicator(int RX, int TX) : BT(RX, TX), r(RX), t(TX){}
  void init(){
    BT.begin(9600);
  }
  void sendDone(){
    byte b = 1;
    BT.print(b);
  }
  byte forceRead(){
    while(!BT.available());
    return BT.read();
  }
  long forceReadLong(){//Unsigned!!
    long res = 0;
    res = forceRead();
    res <<=8;
    res |= forceRead();
    res <<=8;
    res |= forceRead();
    res <<=8;
    res |= forceRead();
    return res;
  }
  Message forceReadMessage(){
    while(!BT.available());
    Message m;
    m.kind = static_cast<MessageKind>(BT.read());
    switch(m.kind){
      case MessageKind::lift:
        Serial.println("LIFT");
        break;
      case MessageKind::lower:
        Serial.println("LOWER");
        break;
      case MessageKind::move:
        Serial.println("MOVE");
        m.len1 = forceReadLong();
        m.len2 = forceReadLong();
        break;
      case MessageKind::set:
        Serial.println("SET");
        m.len1 = forceReadLong();
        m.len2 = forceReadLong();
        break;
      default:
        Serial.println("unknown message:");
        Serial.println(m.kind);
        break;
    }
    return m;
  }
};
