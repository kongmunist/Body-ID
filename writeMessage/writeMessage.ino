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
//  bitstring = "0110100001100101011011000110110001101111"; // Hello
  bitstring = "01100001011011100110010001111001"; // Andy
  bitstring = "0110010001100001011101100110100101100100"; // David
//    bitstring = "01110110011010010110011101101110011001010111001101101000";
//  bitstring = "0110010101110011011101000110010101100101011011010110010101100100001000000110011101110101011001010111001101110100"; // Esteemed guest
//  bitstring = "1100100110000111010011000111000101100011110010111001101100110111001110111110001011000111000111100110111001110110110000110111111000110011011001101100010110010110100111001110001011001111001001101101101101100101";
  
//  bitstring = "1111000011110000110011001010";
}

void loop() {
//  // put your main code here, to run repeatedly:
    PORTB = B00000001;
    delay(10);
    for (int i = 0; i < bitstring.length(); i++) {
      now = micros();
      if (bitstring[i] == '1'){
        PORTB = B00000001;
      }
      else {
        PORTB = B00000000;
      }
      
      delayMicroseconds(kiloh);
    }
    PORTB = B00000000;
    delay(500);

    
//  delayMicroseconds(kiloh);
  
}
