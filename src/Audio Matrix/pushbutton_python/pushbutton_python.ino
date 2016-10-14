void setup() {
  // put your setup code here, to run once:
pinMode(12,INPUT_PULLUP);
Serial.begin(9600);
}
int count=0;
void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(12)==LOW)
  count++;
Serial.println(count);
delay(300);
}
