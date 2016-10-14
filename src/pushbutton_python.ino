void setup() {
  // put your setup code here, to run once:
pinMode(8,INPUT);
Serial.begin(9600);
}
void loop() {
  // put your main code here, to run repeatedl
  if(digitalRead(8)==HIGH)
  count++;
Serial.println(count);

}
