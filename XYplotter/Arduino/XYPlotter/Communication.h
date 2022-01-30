#include <AltSoftSerial.h>

enum MessageKind{
  lift,
  lower,
  move,
  set,
  rest
};

struct Message{
  MessageKind kind;
  long len1, len2;
};
struct ReadResult{
  bool success;
  byte value;
};
struct LongReadResult{
  bool success;
  long value;
  byte ctrl;
};

class Communicator{
private:
  AltSoftSerial BT;
  int queueSize;
public:
  Communicator() : queueSize(0) {}
  void init(){
    BT.begin(9600);
  }
  void sendDone(){
    queueSize++;
    if(queueSize==10){ // sending only 11th confirmations for performace(11 fit in buffer)
      queueSize = 0;
      byte b = 255;
      BT.write(b);
    }
  }
  void sendFail(){
    delay(100);//Time to receive rest of data(until queue limit is reached)
    BT.flushInput();
    BT.write(queueSize);
    queueSize = 0;
  }
  ReadResult forceRead(int time=100){ //TODO tweak time to smallest value without errors
    unsigned long started = millis();
    while(!BT.available()){
      if(millis()-started > time)
        return {false, 0};
    }
    return {true, BT.read()};
  }
  LongReadResult forceReadLong(){
    byte ctrl = 0;
    ReadResult tmp = forceRead();
    if(!tmp.success) return {false, 0};
    ctrl ^= tmp.value;
    long res = tmp.value;
    res <<=8;
    tmp = forceRead();
    if(!tmp.success) return {false, 0};
    ctrl ^= tmp.value;
    res |= tmp.value;
    res <<=8;
    tmp = forceRead();
    if(!tmp.success) return {false, 0};
    ctrl ^= tmp.value;
    res |= tmp.value;
    if(res&8388608)//handle sign bit 
      res -= 16777216;
    return {true, res, ctrl};
  }
  Message forceReadMessage(){
    while(!BT.available());
    Message m;
    m.kind = static_cast<MessageKind>(BT.read());
    byte ctrl = m.kind;
    LongReadResult tmp;
    switch(m.kind){
      case MessageKind::move:
        tmp = forceReadLong();
        if(!tmp.success) return forceReadMessage();
        ctrl^=tmp.ctrl;
        m.len1 = tmp.value;
        tmp = forceReadLong();
        if(!tmp.success) return forceReadMessage();
        ctrl^=tmp.ctrl;
        m.len2 = tmp.value;
        break;
      case MessageKind::set:
        tmp = forceReadLong();
        if(!tmp.success) return forceReadMessage();
        ctrl^=tmp.ctrl;
        m.len1 = tmp.value;
        tmp = forceReadLong();
        if(!tmp.success) return forceReadMessage();
        ctrl^=tmp.ctrl;
        m.len2 = tmp.value;
        break;
      default:
        break;
    }
    ReadResult tmp2 = forceRead();
    if(!tmp2.success) return forceReadMessage();
    byte rXOR = tmp2.value;
    if(rXOR != ctrl){
      sendFail();
      return forceReadMessage();
    }
    if(m.kind == MessageKind::set)
      queueSize = 0; 
    return m;
  }
};
