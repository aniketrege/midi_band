from sys import argv
from random import uniform 
import serial
import rtmidi_python as rtmidi
import time

com_port=argv[1]
midi_out = rtmidi.MidiOut()
midi_out.open_port(0)

if(len(argv)<3):
    print("Usage- python %s COM_PORT note1 [note2 note3 ...]"%(argv[0]))
    exit(0)
print "Using COM port- " + com_port
notes=[]
for note in argv[2:]:       # append all notes (params) passed in command line
    notes.append(note)
print "Notes- "+ str(notes)

ser = serial.Serial(com_port, 9600)
ser.reset_input_buffer()

accelerometer_range=23.0    #range of values which adxl sends = 11 - (-11) +1
no_bins=len(argv)-2         #remove script name and com port number
bin_size = accelerometer_range/no_bins 
decision_boundary=[]       
for i in range(0,no_bins):
    decision_boundary.append((-11+(bin_size*i),-11+(bin_size*(i+1)),i))  #list of all boundaries according to number of notes
print "number of bins- " + str(no_bins)
print "bin size- " + str(bin_size)
print "Decision Boundaries- " + str(decision_boundary)
time.sleep(1)

#To read from a file (if you don't have an Arduino and wish to simulate)

#with open("arduino","w") as arduino_readings:
#    for i in range(1,10):
#        reading=uniform(-11,11)
#        arduino_readings.write(str(reading)+"\r\n")

#with open("arduino","r") as arduino_readings:
#    for reading in arduino_readings:
#        reading=reading.rstrip()
#        for (lower,upper,index) in decision_boundary:
#            if(lower<=float(reading)<upper):
#                print reading + " belongs to decision boundary- %s",str(decision_boundary[index])
#                print "Playing note- " + str((notes[index]))
#                break

#Use the following if you have an Arduino

while(1):
    ser.write("t")  #activate Arduino to send adxl values
    reading = float(ser.readline().rstrip())    #typecast to float

    print reading   #to observe the value sent from arduino

    for (lower,upper,index) in decision_boundary:
        if(lower<=reading<upper):
            print "Playing note- " + str((notes[index]))                #display which note is playing
            midi_out.send_message([0x90, int(notes[index]),100])        #this will play note corresponding to whichever bin input is in
            time.sleep(0.3)
            midi_out.send_message([0x80, int(notes[index]),100])
            time.sleep(0.1)
            break


#HBD 43(3) 43(1) 45(4) 43(4) 48(4) 47(8); Syntax: note_number(delay_time)

#Terminal Commands:
#cd C:\Users\Aniket\Documents\Projects\Technites\Glove 2.0 (navigate to where this code is locally)
#python accelerometer.py COM3 60 62 65 67 72
