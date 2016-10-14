void setup() {
  // put your setup code here, to run once:
pinMode(8,INPUT);
Serial.begin(9600);
}
int count=0;
void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(8)==HIGH)
  count++;
Serial.println(count);
delay(300);
}
