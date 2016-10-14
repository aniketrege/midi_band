/* Technites 2016
 *  MIDI Band 
 *  Instrument : Flute
 *  Author(s) : Vibhore Jain, Prabhanjan Mannari, MIDI Band Team
 *  Date : 09/10/2016
 */


/*  This Sketch demonstrates the use of MIDI messages to turn on/off a note  
 *  for a monophonic (only one note played at a time) flute and also control 
 *  its "expression" (volume in plain words :P) using MIDI CC (Control Change)
 *  message on MIDI channel 1 controller 11. MIDI CC messages allow you to change  
 *  the quality of notes and their charecteristics once they are played. Read 
 *  the end of the code for more information about MIDICC messages. 
 *  PS: The volume is a function of the blow on the blow detection circuit on the flute.
 *  If you're curious about the circuit google "electret microphone" and "peek detectors".
 */

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
#define pitchbend 0xE0
#define poly 0xA0
#define midiccExpression 0xB0 //Midi controller 11 to control volume of selected channel (Midi channel 1 in our case)
boolean flag=LOW;
int arr[] = {0X48,0X4A,0X4C,0X4D,0x4F,0X51}; //Array of six notes starting from C6


void setup() {
  pinMode(2,INPUT_PULLUP);//Inputs for the six buttons for the notes
  pinMode(3,INPUT_PULLUP);
  pinMode(4,INPUT_PULLUP);
  pinMode(5,INPUT_PULLUP);
  pinMode(6,INPUT_PULLUP);
  pinMode(7,INPUT_PULLUP);
  Serial.begin(19200); //Begin serial communcation with PC
}
//Figure out what's going on. I am too lazy to comment every line :P. Just kiddin.
void loop() {
    
    for(int i = 2;i<8;i++)  //Continously check if any button is pressed
    {
     if(digitalRead(i)==LOW)playnote(i);// Call play note if any pin goes low and play corresponding note
    }
}

void midi(int cmd, int data1, int data2)//Function to send midi commands serially 
{
Serial.write(cmd);
Serial.write(data1);
Serial.write(data2);
}
void playnote(int key)// Key argument is used to know which button is pressed
{
  int pressure = map(analogRead(A0),200,520,1,127);// A0 is connected to the output of the blow detection circuit.
       midi(ON,arr[key-2],0x55) ; //Turning the corresponding note on
       delay(80);// delay just for debouncing
       while(digitalRead(key)== LOW) 
       {
        pressure = map(analogRead(A0),70,350,1,127);// Continuously read A0 map its value to 1-127 (volume of that channel)
        pressure = constrain(pressure,1,127); //Truncate the value of pressure so as to make the midi message valid even if the flute is stuck in typhoon/ Hurricane 
        midi(midiccExpression ,0x0B, pressure);// Send MIDI CC message to change volume according to pressure while the button is still pressed.
        delay(10);//Avoids flooding of commands in fl studio
       }
       midi(OFF,arr[key-2],0x55);// Turn off the note when the button is released
       delay(40);// I dont know why but its good to have nominal delays between consecutive serial writes especially at higher baud rates

}
/*  NOTES ON MIDI CC
 *  I assume that you're familiar with basic MIDI messages 
 *  and the structure of valid midi messages. The following
 *  notes explain what is MIDI CC, how to implement it on 
 *  arduino and how to map in FL studio.
 *  MIDI CC :
 *  I'll still briefly describe the structure of a valid midi
 *  message to begin with. A complete midi message is as follows
 *  Status Byte     Data Byte 1     Data Byte 2 (may or may not be there)
 *  1001 0000       0011 1100       0101 0101
 *  0x90            0x3C            0x55
 *  The above message is read by fl studio as 
 *   Status Byte 1001 means turn a note on (This part defines command)
 *               0000 means turn it on on MIDI channel 1 (This part defines the channel)
 *   Data Byte 1 0011 1100 turn on C5 note on (refer the #define section) 
 *   
 *   Data Byte 2 0101 0101 The velocity (volume) of the note should be 85 
 *   
 *   To send CC messages we have 1011 command part in the status byte.
 *   Here are some other common command bytes
 *   1000 NOTE OFF
 *   1001 NOTE ON
 *   1010 AFTERTOUCH
 *   1011 CONTROL CHANGE
 *   1100 PROGRAM CHANGE
 *   1101 CHANNEL PRESSURE
 *   1110 PITCH BEND
 *   I'll only discuss the control change command and that too 
 *   specifically on controller 11 (0X0B).I guess the arduino code part is pretty 
 *   much self explanatory the second parameter in 
 *   midi(midiccExpression ,0x0B, pressure) defines which controller is the value 
 *   of pressure going to. Yeah ambiguous explaination but plase consider.
 *   While most of the controllers are reserved for specific functions 
 *   there are some controllers which can be defined by the user.
 *   In this sketch we used controller 11 which is reserved for expression
 *   of a channel. What I found was though controller 11 is reserved FL studio 
 *   doesnot recognizes it untill you map it to any "knob" in your plugin.
 *   For the example I used eFlute plugin. Search it from tools -> browser smart 
 *   find. Once you setup your midi device and its is recognized by fl studio
 *   you can start mapping different controllers to different functions.
 *   In eflute you'll find a small volume knob on the top right corner between  
 *   pitch and pan. Right click and go to link to controller.
 *   Select the channel you want the controller to control. In our case MIDI channel 1.
 *   Then change Ctrl (controller) to 11. Also enable the smoothening option 
 *   for smooth changes in volume. Then hit accept and the controller is mapped.
 *   I think you can map any knob to the controller this way. Due to little shortage 
 *   of time I couldn't try all of them but refer this link to know about different
 *   CC data bytes and their functions: 
 *   https://www.midi.org/specifications/item/table-3-control-change-messages-data-bytes-2
 *   Also refer videos by Notes and Volts if you want to learn about MIDI from the
 *   basics.
 *              
  */
