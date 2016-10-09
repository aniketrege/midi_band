//Play simple note stream to test MIDI 


void setup() {
  Serial.begin(9600);
  //pinMode(4,INPUT_PULLUP);
  
}

void loop() {
 
  //if(digitalRead(4)== LOW)
  //{
  Serial.write(0x90);
  Serial.write(0x43);
  Serial.write(0x55);
  delay(600);

  Serial.write(0x90);
  Serial.write(0x43);
  Serial.write(0x55);
  delay(200);

  Serial.write(0x90);
  Serial.write(0x45);
  Serial.write(0x55);
  delay(800);

  Serial.write(0x90);
  Serial.write(0x43);
  Serial.write(0x55);
  delay(800);

  Serial.write(0x90);
  Serial.write(0x48);
  Serial.write(0x55);
  delay(800);

  Serial.write(0x90);
  Serial.write(0x47);
  Serial.write(0x55);
  delay(1600);
  //}
  //Serial.println(digitalRead(4));
}
