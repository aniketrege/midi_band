from sys import argv
from random import uniform 
import serial
import rtmidi_python as rtmidi
import time

midi_out = rtmidi.MidiOut()
midi_out.open_port(0)

if(len(argv)<3):
    print("Usage- python %s COM_PORT note1 [note2 note3 ...]"%(argv[0]))
    exit(0)

notes=[]
for note in argv[2:]:       # append all notes (params) passed in command line
    notes.append(note)
print "Notes- "+ str(notes)

com_port=argv[1]
print "Using COM port- " + com_port
ser = serial.Serial(com_port, 9600)
#ser.reset_input_buffer()


OFF=0x80
ON=0x90
CC_msg=0xB0
accelerometer_range=23.0    #range of values which adxl sends = 11 - (-11) +1
no_bins=len(argv)-2         #remove script name and com port number
bin_size = accelerometer_range/no_bins 
decision_boundary=[]
time.sleep(1)
off=0
on=1
pan_note=0
previousnote=0

def midi(cmd,data1,data2):

    Ser.write(cmd);
    Ser.write(data1);
    Ser.write(data2);


for i in range(0,no_bins):
    decision_boundary.append((-11+(bin_size*i),-11+(bin_size*(i+1)),i))  #list of all boundaries according to number of notes
print "number of bins- " + str(no_bins)
print "bin size- " + str(bin_size)
print "Decision Boundaries- " + str(decision_boundary)

while(1):
    #ser.write('t')  #activate Arduino to send adxl values
    reading = ser.readline().rstrip()
    reading=reading.split()
    zreading=int(reading[0].rstrip())
    xreading=int(reading[1].rstrip())
    count1=int(reading[2].rstrip())
    count2=int(reading[3].rstrip())
    #print zreading   #to observe the value sent from arduino
    #print xreading
    #print count
    for (lower,upper,index) in decision_boundary:
        current_note= (notes[index])

        if(count1%2==0 and count2%2==0): 

        #********       MODE ONE        ********

            if(lower<=zreading<upper):
                if(off==1):
                    midi_out.send_message([OFF,play_note,100])       #if mode switched from pan, switch off pan note
                if(previousnote!=int(current_note)):                 #if note is different from last, switch it off
                    on=1
                    midi_out.send_message([OFF,previousnote,100])
                if(on==1):
                    print "Playing note- " + str((current_note))                #display which note is playing
                    previousnote=int(current_note)                              #store previous note for next iteration to check
                    midi_out.send_message([ON, int(current_note),100])        #this will play note corresponding to whichever bin input is in
                    on=0
                    time.sleep(0.3)
                    midi_out.send_message([OFF, int(current_note),100])            #switch off current note
                    time.sleep(0.1)
                break   

        elif(count1%2==1 and count2%2!=1):                                       

        #********       MODE TWO        ********

            if(lower<=zreading<upper):
                print "holding note- " + str((current_note))
                print "panvalue ----"
                print xreading                    #display which note is playing
                if(off==0):
                       play_note=int(current_note)
                       midi_out.send_message([ON, int(current_note),100])     #This will be switched off only if mode changes
                time.sleep(0.3)
                off=1
                midi_out.send_message([CC_msg,10,xreading])                       #CC: Pan 
                time.sleep(0.1)
                break


        #********       MODE THREE     ********
        elif(count2%2==1 and count1%2!=1):
            if(lower<=zreading<upper):
                print "holding note- " + str((current_note))
                print "controller cc--noise--"
                print xreading                    #display which note is playing
                if(off==0):
                       play_note=int(current_note)
                       midi_out.send_message([ON, int(current_note),100])     #This will be switched off only if mode changes
                time.sleep(0.3)
                off=1
                midi_out.send_message([CC_msg,12,xreading])                       #CC: Pan 
                time.sleep(0.1)
                break


        else:
            if(lower<=zreading<upper):
                if(off==1):
                    midi_out.send_message([OFF,play_note,100])       #if mode switched from pan, switch off pan note
                if(previousnote!=int(current_note)):                 #if note is different from last, switch it off
                    on=1
                    midi_out.send_message([OFF,previousnote,100])
                if(on==1):
                    print "Playing note- " + str((current_note))                #display which note is playing
                    previousnote=int(current_note)                              #store previous note for next iteration to check
                    midi_out.send_message([ON, int(current_note),100])        #this will play note corresponding to whichever bin input is in
                    on=0
                    time.sleep(0.3)
                    midi_out.send_message([OFF, int(current_note),100])            #switch off current note
                    time.sleep(0.1)
                break 
            


#HBD 43(3) 43(1) 45(4) 43(4) 48(4) 47(8); Syntax: note_number(delay_time)

#Terminal Commands:
#cd C:\Users\Aniket\Documents\Projects\Technites\Glove 2.0 (navigate to where this code is locally)
#python ADXLmodified.py COM3 60 62 65 67 72
