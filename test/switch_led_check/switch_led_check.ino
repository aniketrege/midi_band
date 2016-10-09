int switchPin=8;
int led=13;
//Check whether a switch works by glowing a LED

void setup() {
  pinMode(switchPin,INPUT);
  pinMode(led,OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(switchPin)==HIGH)
  digitalWrite(led, HIGH);
  else if(digitalRead(switchPin==LOW));
  digitalWrite(led,LOW);
}
