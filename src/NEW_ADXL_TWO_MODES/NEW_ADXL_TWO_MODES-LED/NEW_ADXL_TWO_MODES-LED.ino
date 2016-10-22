#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

/* Assign a unique ID to this sensor at the same time */
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(12345);

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

#define OFF 0x80
#define ON 0x90
#define lockpin1 12

#define lockpin2 13
int prev=0;
int z;
int flag=0;
int zreading;
int xreading;
int counta=0;
int countb=0;

void displaySensorDetails(void)
{
  sensor_t sensor;
  accel.getSensor(&sensor);
  /*Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" m/s^2");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" m/s^2");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" m/s^2");  
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
  */
}

void displayDataRate(void)
{
  /*Serial.print  ("Data Rate:    "); 
  
  switch(accel.getDataRate())
  {
    case ADXL345_DATARATE_3200_HZ:
      Serial.print  ("3200 "); 
      break;
    case ADXL345_DATARATE_1600_HZ:
      Serial.print  ("1600 "); 
      break;
    case ADXL345_DATARATE_800_HZ:
      Serial.print  ("800 "); 
      break;
    case ADXL345_DATARATE_400_HZ:
      Serial.print  ("400 "); 
      break;
    case ADXL345_DATARATE_200_HZ:
      Serial.print  ("200 "); 
      break;
    case ADXL345_DATARATE_100_HZ:
      Serial.print  ("100 "); 
      break;
    case ADXL345_DATARATE_50_HZ:
      Serial.print  ("50 "); 
      break;
    case ADXL345_DATARATE_25_HZ:
      Serial.print  ("25 "); 
      break;
    case ADXL345_DATARATE_12_5_HZ:
      Serial.print  ("12.5 "); 
      break;
    case ADXL345_DATARATE_6_25HZ:
      Serial.print  ("6.25 "); 
      break;
    case ADXL345_DATARATE_3_13_HZ:
      Serial.print  ("3.13 "); 
      break;
    case ADXL345_DATARATE_1_56_HZ:
      Serial.print  ("1.56 "); 
      break;
    case ADXL345_DATARATE_0_78_HZ:
      Serial.print  ("0.78 "); 
      break;
    case ADXL345_DATARATE_0_39_HZ:
      Serial.print  ("0.39 "); 
      break;
    case ADXL345_DATARATE_0_20_HZ:
      Serial.print  ("0.20 "); 
      break;
    case ADXL345_DATARATE_0_10_HZ:
      Serial.print  ("0.10 "); 
      break;
    default:
      Serial.print  ("???? "); 
      break;
  }  
  Serial.println(" Hz");  
  */
}

void displayRange(void)
{
  /*Serial.print  ("Range:         +/- "); 
  
  switch(accel.getRange())
  {
    case ADXL345_RANGE_16_G:
      Serial.print  ("16 "); 
      break;
    case ADXL345_RANGE_8_G:
      Serial.print  ("8 "); 
      break;
    case ADXL345_RANGE_4_G:
      Serial.print  ("4 "); 
      break;
    case ADXL345_RANGE_2_G:
      Serial.print  ("2 "); 
      break;
    default:
      Serial.print  ("?? "); 
      break;
  }  
  Serial.println(" g");  
  */
}

void setup(void) 
{
#ifndef ESP8266
  while (!Serial); 
#endif
  Serial.begin(9600);
  pinMode(lockpin1,INPUT_PULLUP);
  pinMode(lockpin2,INPUT_PULLUP);
  //Serial.println("Accelerometer Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!accel.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    //Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
    while(1);
  }

  /* Set the range to whatever is appropriate for your project */
  accel.setRange(ADXL345_RANGE_8_G);
  //displaySetRange(ADXL345_RANGE_8_G);
  // displaySetRange(ADXL345_RANGE_4_G);
  // displaySetRange(ADXL345_RANGE_2_G);
  
  /* Display some basic information on this sensor */
  displaySensorDetails();
  
  /* Display additional settings (outside the scope of sensor_t) */
  displayDataRate();
  displayRange();
  //Serial.println("");
}

void loop(void) 
{
  /* Get a new sensor event */ 
  sensors_event_t event; 
  accel.getEvent(&event);
  xreading=constrain(map(event.acceleration.x,-11,11,1,126), 0, 127);  //required as pitchbend takes 8 bit argument
  //Serial.print("Z: "); Serial.print(event.acceleration.z); Serial.print("  ");Serial.println("m/s^2 ");
  
  if(digitalRead(lockpin1)==LOW){
      counta=counta+1 ;
      zreading=event.acceleration.z;//value of z-acceleration when the button is pressed
  }
  if(digitalRead(lockpin2)==LOW){
      countb=countb+1 ;
      zreading=event.acceleration.z;//value of z-acceleration when the button is pressed
  }
     
     if(counta%2==0&&countb%2==0){
      serialcomm(event.acceleration.z, xreading, counta,countb);
      notescale(event.acceleration.z);}
      //if switch is not pressed or pressed even number of times then send the values according to accelerometer z value
      else if(counta%2==1 && countb%2==1){countb=0;
     serialcomm(zreading,xreading,counta,countb);
     ledscale(zreading,xreading);}
      else if(countb%2==0&&counta%2==1){
      serialcomm(zreading,xreading,counta,countb);
      ledscale(zreading,xreading);}
      else{
        serialcomm(zreading,xreading,counta,countb);
        ledscale(zreading,xreading);}
        
     
      delay(400);
      
   /* Arduino Packet Syntax:  "zvalue <space> xvalue <space> count <newline character> "
    Split() method was used in Python to generate a list "zvalue, xvalue, count"
    reading= ser.readline.rstrip().split()
    print reading 
    will give output "-10, 10, 2" 
    */
}

void serialcomm(int zvalue, int xvalue, int counta,int countb)
{
      Serial.print(zvalue); 
      Serial.print(" ");
      Serial.print(xvalue);
      Serial.print(" ");
      Serial.print(counta);
      Serial.print(" ");
       Serial.println(countb);
}


void ledscale(int z,int x){

  int i =2;
  while(i<12) digitalWrite(i++,LOW);
  digitalWrite(A3,LOW);
  digitalWrite(A0,LOW);
  digitalWrite(A1,LOW);
  digitalWrite(A2,LOW);
    x = constrain(map(x,15,110,-3,3),-3,3);
    z = constrain(map(z,-8,9,-4,3),-4,4);
    switch(z){
      case 4: digitalWrite(9,HIGH);
      case 3: digitalWrite(8,HIGH);
      case 2: digitalWrite(7,HIGH);
      case 1: digitalWrite(6,HIGH);
              break;
      case -4: digitalWrite(5,HIGH);
      case -3: digitalWrite(4,HIGH);
      case -2: digitalWrite(3,HIGH);
      case -1: digitalWrite(2,HIGH);
              break;
      default: break;
              
      
    }
   switch(x){
      
      case 3: digitalWrite(A2,HIGH);
      case 2: digitalWrite(A1,HIGH);
      case 1: digitalWrite(A0,HIGH);
              break;
      case -3: digitalWrite(A3,HIGH);
      case -2: digitalWrite(11,HIGH);
      case -1: digitalWrite(10,HIGH);
              break;
      default: break;
              
      
    }
    //Serial.println(x);
}
void notescale(int z){
  int i =2;
  while(i<10) digitalWrite(i++,LOW);
  
    
    z = constrain(map(z,-8,8,-4,4),-4,4);
    switch(z){
      case 4: digitalWrite(9,HIGH);
      case 3: digitalWrite(8,HIGH);
      case 2: digitalWrite(7,HIGH);
      case 1: digitalWrite(6,HIGH);
              break;
      case -4: digitalWrite(5,HIGH);
      case -3: digitalWrite(4,HIGH);
      case -2: digitalWrite(3,HIGH);
      case -1: digitalWrite(2,HIGH);
              break;
      default: break;
}
}
