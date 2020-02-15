const int outPin = 8;
float kiloh;
float freq = 1000;
long now;
String bitstring;
String rawstring;
String asciistring;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  DDRB = B00000001;
  kiloh = 1000000/freq;
  rawstring = "hello";
  asciistring = "104 101 108 108 111";
//  bitstring = "0110100001100101011011000110110001101111";
  bitstring = "1111000011110000110011001010";
}

void loop() {
  // put your main code here, to run repeatedly:
    PORTB = B00000001;
    delay(10);
    for (int i = 0; i < 26; i++) {
      now = micros();
      if (bitstring[i] == '1'){
        PORTB = B00000001;
      }
      else {
        PORTB = B00000000;
      }
      
      delayMicroseconds(kiloh-(micros()-now));
    }
    PORTB = B00000000;
    delay(500);
}
