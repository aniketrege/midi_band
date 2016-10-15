void setup() {
  // put your setup code here, to run once:
pinMode(10,INPUT);
pinMode(2,INPUT);
pinMode(3,INPUT);
pinMode(4,INPUT);
pinMode(5,INPUT);
pinMode(6,INPUT);
pinMode(7,INPUT);
pinMode(8,INPUT);
pinMode(9,INPUT);
Serial.begin(9600);
}
static int i=0,count[9];
void loop() {
  // put your main code here, to run repeatedly:
  for(i=0;i<9;i++)
  {
    if(digitalRead(i+2)==HIGH)
    count[i]=count[i]+1;
   Serial.print(count[i]);
   Serial.print(" ");
  }
  Serial.print("\n");
delay(200);
}
