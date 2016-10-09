//Play HBD if threshold is crossed and debounce is correct

#define C 60
#define D5 62
#define E 64
#define F1 65
#define F2 77
#define G 67

int note1=8;
int note2=A0;
int val;
int flag=0;

int hbd[12]={C,C,D5,C,F1,E,C,C,D5,C,G,F2};
int i=0;

void setup() {
  // put your setup code here, to run once:
  pinMode(note1,INPUT_PULLUP);
  pinMode(note2,INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  val=analogRead(note2);
  while(val<550)
  {   
    val=analogRead(note2);
    if(flag==0){
      MIDImessage(0x90,hbd[i],0x55);
      flag=1;
      i++;
      if(i==12)
      i=0;
    }
  }
    if(flag==1){
      if(i==0){
        MIDImessage(0x80,hbd[11],0x55);
      }
      MIDImessage(0x80,hbd[i-1],0x55);
      flag=0;
    }
    delay(50);
   }

void MIDImessage(int note, int data1, int data2)
{
  Serial.write(note);
  Serial.write(data1);
  Serial.write(data2);
}



