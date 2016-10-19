#define master 11
#define select 12
#define led0 A0
#define led1 A1
#define led2 A2
#define led3 A3
static int i=0;
int k=0;
int notpressed=LOW;
static int mode,prevmode,sel,prevsel;
bool flag[]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};


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



void loop() {
  
  
  
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
 if(sel%2==0){
    Serial.print("0 ");
    for(i=0;i<9;i++)
    Serial.print("0 ");
    Serial.print("\n");
  }
    
  if(sel%2==1)
  { 
    static int count[9];
    Serial.print(mode);
    Serial.print(" ");
    for(i=0;i<9;i++)
    {
      if(digitalRead(i+2)==HIGH && flag[i+2]==LOW){
        count[i]=count[i]+1;
        flag[i+2]=HIGH;
      }
      if(digitalRead(i+2)==LOW)
        flag[i+2]=LOW;
      Serial.print(count[i]);
      Serial.print(" ");
    }
    Serial.print("\n");
 }
 prevmode=mode;
 delay(300);
}
