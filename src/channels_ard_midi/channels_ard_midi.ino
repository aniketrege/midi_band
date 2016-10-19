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
void midi(int cmd, int data1, int data2);
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}
int val=0;
void loop() {
  // put your main code here, to run repeatedly:
int i=0;
  midi(0x90,C5,0x55);
  midi(0xB0,12,val=val+5);
   delay(200);
   midi(0x80,C5,0x55);
   delay(100);
   if(val>127)
   val=0;

}
void midi(int cmd, int data1, int data2)
{
Serial.write(cmd);
Serial.write(data1);
Serial.write(data2);
}
