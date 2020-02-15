#define pinOfPin(P)\
  (((P)>=0&&(P)<8)?&PIND:(((P)>7&&(P)<14)?&PINB:&PINC))
#define pinIndex(P)((uint8_t)(P>13?P-14:P&7))
#define pinMask(P)((uint8_t)(1<<pinIndex(P)))
#define isHigh(P)((*(pinOfPin(P))& pinMask(P))>0)

const int inPin = 8;
//int pulldownpin = 7;
float kiloh;
float freq =10000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  DDRB = B00000000;
  kiloh = 1000000 / freq;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
//    while (!isHigh(inPin)){
//      delay(1);
//    }
//    
//    for (int i= 0; i < 800; i++){
//      Serial.println(isHigh(inPin));
//      delayMicroseconds(kiloh);
//  }
  Serial.println(analogRead(A0) > 205);
  
   
}
