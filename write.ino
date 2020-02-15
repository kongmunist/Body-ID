const int outPin = 8;
float kiloh;
float freq = 100000;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  DDRB = B00000001;
  kiloh = 1000000/freq;
}

void loop() {
  // put your main code here, to run repeatedly:
  while (true) {
    PORTB = B00000001;
    delayMicroseconds(kiloh);
    PORTB = B00000000;
    delayMicroseconds(kiloh);
}
}
