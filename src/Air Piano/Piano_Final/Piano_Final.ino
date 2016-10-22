#define C4 0x30
#define Cs4 0x31
#define D4 0x32
#define E4 0x34
#define F4 0x35
#define G4 0x37
#define A4a 0x39
#define B4 0x3B

#define C5 0x3C
#define D5 0x3E
#define E5 0x40
#define F5 0x41
#define G5 0x43
#define A5a 0x45
#define As5 0x46
#define B5 0x47
#define C6 0x48
#define Cs6 0x49

#define n1 A5
#define n2 A4
#define n3 A3
#define n4 A2
#define n5 A1
#define n6 A0

#define led1 3 //bottom to up
#define led2 5
#define led3 6
#define led4 9
#define led5 10
#define led6 11

#define THRESHOLD 500

int drum=12;
int c;
int x,y;
const int d=10; //delay
int ctr=0x10; // controller number 16
int ch=0;
int chmax=14;
int flag_channel=0; //flag for channel switch
int flag_drum=0;
int arr[6]={0,0,0,0,0,0};
int led[6]={0,0,0,0,0,0};
const int size_of_i=6;
int i=0;
int note[size_of_i][6]= { {0x4C,D5,E5,F5,G5,A5a} , {C5,C5,G5,G5,A5a,A5a} , {F5,F5,E5,E5,D5,D5} , {C5,G5,C6,C5,As5,A5a} , {C5,G5,C6,C5,As5,A5a} , {C4,Cs4,D4,E4,C6,Cs6} }    ;
void midi(int cmd, int data1, int data2)
{
Serial.write(cmd);
Serial.write(data1);
Serial.write(data2);
}

void setup() {
   Serial.begin(9600);
  
   
   pinMode(8,INPUT); //channel switch
   
   pinMode(n1,INPUT);  //note array
   pinMode(n2,INPUT);
   pinMode(n3,INPUT);
   pinMode(n4,INPUT);
   pinMode(n5,INPUT);
   pinMode(n6,INPUT);  //note array
   pinMode(drum,INPUT_PULLUP);
   
   pinMode(led1,OUTPUT);
   pinMode(led2,OUTPUT);
   pinMode(led3,OUTPUT);     //might be pwm
   pinMode(led4,OUTPUT);     //might be pwm
   pinMode(led5,OUTPUT);
   pinMode(led6,OUTPUT);
   
   
   
  // midi(0xE0,0x00,0x40);
   
}

void loop() {


/*---------------------------------------------------------      
      if ((digitalRead(8)==LOW) && (flag_channel==0))
      {
          flag_channel=1;
          ch=ch+1;
          i=i+1;
          if (ch>chmax)
             ch=0;
          if (i>size_of_i)
             i=0;   
      } 
      else if  ((digitalRead(8)==HIGH) && (flag_channel==1))    
      {
          flag_channel=0;
      }  
//----------------------------------------------------------
//__________________________________________________________*/


if ((analogRead(n1)>THRESHOLD)&&(arr[0]==0))
  {
      midi((0x90 | ch),C5,0x55);
      arr[0]=1;
      while(1)
      {   led[0]=map(analogRead(n1),0,1023,255,0);
          analogWrite(led1,led[0]);
          if (analogRead(n1)<THRESHOLD)
              {
                  arr[0]=0;
                  midi((0x80 | ch),C5,0x55);
                  digitalWrite(led1,0);
                  break;
              }
          
          delay(d);
          
          //midi((0xE0 | ch) ,0,);
          //midi((0xB0 | ch),ctr,);
          
      }
  }
//--------------------------------

//__________________________________________________________

if ((analogRead(n2)>THRESHOLD)&&(arr[1]==0))
  {
      midi(0x90,D5,0x55);
      arr[1]=1;
      while(1)
      {
        led[1]=map(analogRead(n2),0,1023,255,0);
          analogWrite(led2,led[1]);
          if (analogRead(n2)<THRESHOLD)
              {
                  arr[1]=0;
                  midi(0x80,D5,0x55);
                  digitalWrite(led2,0);
                  break;
              }
          
          delay(d);
          
          //midi((0xE0 | ch) ,0,);
          //midi((0xB0 | ch),ctr,);
          
      }
  }
//--------------------------------
//__________________________________________________________

if ((analogRead(n3)>THRESHOLD)&&(arr[2]==0))
  {
      midi((0x90 | ch),E5,0x55);
      arr[2]=1;
      while(1)
      { 
        led[2]=map(analogRead(n3),0,1023,255,0);
          analogWrite(led3,led[2]);
          if (analogRead(n3)<THRESHOLD)
              {
                  arr[2]=0;
                  midi((0x80 | ch),E5,0x55);
                  digitalWrite(led3,0);
                  break;
              }
          
          delay(d);
          
          //midi((0xE0 | ch) ,0,);
          //midi((0xB0 | ch),ctr,);
          
      }
  }
//--------------------------------
//__________________________________________________________

if ((analogRead(n4)>THRESHOLD)&&(arr[3]==0))
  {led[3]=map(analogRead(n4),0,1023,255,0);
          analogWrite(led4,led[3]);
      midi((0x90 | ch),F5,0x55);
      arr[3]=1;
      while(1)
      {
          if (analogRead(n4)<THRESHOLD)
              {
                  arr[3]=0;
                  midi((0x80 | ch),F5,0x55);
                  digitalWrite(led4,0);
                  break;
              }
          
          delay(d);
          
          //midi((0xE0 | ch) ,0,);
          //midi((0xB0 | ch),ctr,);
          
      }
  }
//--------------------------------
//__________________________________________________________

if ((analogRead(n5)>THRESHOLD)&&(arr[4]==0))
  {
      midi((0x90 | ch),G5,0x55);
      arr[4]=1;
      while(1)
      {
        led[4]=map(analogRead(n5),0,1023,255,0);
          analogWrite(led5,led[4]);
          if (analogRead(n5)<THRESHOLD)
              {
                  arr[4]=0;
                  midi((0x80 | ch),G5,0x55);
                  digitalWrite(led5,0);
                  break;
              }
          
          delay(d);
          
          //midi((0xE0 | ch) ,0,);
          //midi((0xB0 | ch),ctr,);
          
      }
  }
//--------------------------------
//__________________________________________________________

if ((analogRead(n6)>THRESHOLD)&&(arr[5]==0))
  {
    led[5]=map(analogRead(n6),0,1023,255,0);
      midi((0x90 | ch),A5a,0x55);
      arr[5]=1;
      while(1)
      {
          if (analogRead(n6)<THRESHOLD)
              {
                  arr[5]=0;
                  midi((0x80 | ch),A5a,0x55);
                  digitalWrite(led6,0);
                  break;
              }
          
          delay(d);
          
          //midi((0xE0 | ch) ,0,);
          //midi((0xB0 | ch),ctr,);
          
      }
  }  
  
}
//--------------------------------
/*
  if(drum==LOW&&flag_drum==1 ){
    while(1){
      if(drum==LOW&&flag_drum==1){
        midi(0x8F,60,00);
        break;
      }
      if(drum==HIGH){
        flag_drum=1;
      }
      midi(0x9F,60,0x55);
      delay(50);
      midi(0x8F,60,0);
    }
  }

}*/


