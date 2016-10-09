import serial
import rtmidi_python as rtmidi
import time
import sys
from scipy.interpolate import interp1d

#time.sleep(0.5)
on=0x90
off=0x80
vel=100

def msg (note,oldtemp):

    midi_out.send_message([off,oldtemp,vel])
    midi_out.send_message([off,temp,vel])

    midi_out.send_message([on,note,vel])
    temp=note



#ser=serial.Serial("/dev/cu.usbserial-A9G7JH5T",9600)

ser=serial.Serial("/dev/cu.usbmodem1411",9600)

midi_out = rtmidi.MidiOut()
midi_out.open_port(0)
print "Midi port open"


notes= sys.argv[1:]											# all params besides name of this script itself, ie the notes we pass in hex
number_of_notes= len(sys.argv) - 1 							# number of notes we are parsing
z_map = int(interp1d([-11,11],[1,number_of_notes]))			# z value of accelerometer ranges from -11 to 11 approx. Map this to integer range


while(1):
    pot=int(ser.readline())
    mapped_pot=z_map(pot)									# this will give a range from 1 to number of notes in float
    for i in range(1,number_of_notes):						
		if (mapped_pot<i)&&(mapped_pot>(i-1)) 				# check which range the mapped value is in, and send a midi msg to play corresponding note
			msg(sys.argv[i], oldtemp)
	
    #msg(pot,oldtemp)
    #print pot

ser.close()
print "serial closed"

