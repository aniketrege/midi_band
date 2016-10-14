int count;

void setup() {
  pinMode(8,INPUT);
  Serial.begin(9600);
}

void loop() {
  if(digitalRead(8)==HIGH)
    count++;
    
  Serial.println(count);

}

