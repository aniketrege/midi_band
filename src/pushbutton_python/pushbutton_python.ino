void setup() {
  // put your setup code here, to run once:
pinMode(8,INPUT);
Serial.begin(9600);
}
void loop() {
  // put your main code here, to run repeatedly:
Serial.println(digitalRead(8));
//Serial.println(analogRead(A4));
//Serial.println(analogRead(A5));

}
