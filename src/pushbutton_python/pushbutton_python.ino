<<<<<<< HEAD
int count=0;
=======
int count;
>>>>>>> saikamalkola-master

void setup() {
  pinMode(8,INPUT);
  Serial.begin(9600);
}
<<<<<<< HEAD
=======

void loop() {
  if(digitalRead(8)==HIGH)
    count++;
    
  Serial.println(count);
>>>>>>> saikamalkola-master

void loop() {
  if (digitalRead(8)==HIGH)
    count++;
  Serial.println(count);  
}

