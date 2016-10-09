void setup() {
Serial.begin(9600); // set the baud rate
}

void loop() {
  if(Serial.available()) {
    char inByte = Serial.read();
  
    if(inByte=='t'){
      for(int i=-11;i<11;i++)
        Serial.println(i);
   
    }
    
  }
}
