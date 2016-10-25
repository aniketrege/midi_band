#define master 11
#define select 12
#define led0 A0
#define led1 A1
#define led2 A2
#define led3 A3
static int i=0;
int k=0;
static int mode,prevmode,sel,prevsel;
char inByte='c';

void setup() {
  pinMode(master,INPUT);
  pinMode(select,INPUT);
  pinMode(2,INPUT);
  pinMode(3,INPUT);
  pinMode(4,INPUT);
  pinMode(5,INPUT);
  pinMode(6,INPUT);
  pinMode(7,INPUT);
  pinMode(8,INPUT);
  pinMode(9,INPUT);
  pinMode(10,INPUT);
  pinMode(led0,OUTPUT);
  pinMode(led1,OUTPUT);
  pinMode(led2,OUTPUT);
  pinMode(led3,OUTPUT);
  Serial.begin(9600);
}
static int count[9];


void loop() {
   if(Serial.available()) {
    char inByte = Serial.read();
   }
  


  if(digitalRead(select)==HIGH)
    sel=sel+1;
  if(digitalRead(master)==HIGH)
    mode=mode+1;
  if(mode%5==1)
    digitalWrite(led0,HIGH);
  if(mode%5==2)
    digitalWrite(led1,HIGH);
  if(mode%5==3)
    digitalWrite(led2,HIGH);
  if(mode%5==4)
    digitalWrite(led3,HIGH);
    if(mode==5)
    mode=0;
    if(sel==2)
    sel=0;
Serial.print(mode);
Serial.print(" " );
Serial.print(sel);
Serial.print(" " );
for(i=0;i<9;i++)
{ if(digitalRead(i+2)==HIGH&&sel%2!=0)
{
  count[i]++;
  if(count[i]==2)
  count[i]=0;
}
  if(sel%2==0)
  count[i]=0;
  Serial.print(count[i]);
  Serial.print(" " );
}

Serial.print("\n");
   delay(10);
}

void midi(int cmd, int data1, int data2)
{
Serial.write(cmd);
Serial.write(data1);
Serial.write(data2);
}

