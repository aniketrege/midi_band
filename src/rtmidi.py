from sys import argv
import rtmidi_python as rtmidi
import time
import serial
from random import uniform 
import argparse

parser=argparse.ArgumentParser(					# usage documentation
    description='''Command Line Usage ''',
    epilog="""Enjoy, MIDI band users!.""")
parser.add_argument('--com', type=int, default=3, help='COM Port on which Arduino is running.')
parser.add_argument('notes', nargs='*', default=[43, 43, 45, 43, 48, 47], help='String of notes to play.')
args=parser.parse_args()

com_port="COM"+(argv[2])
print "Arduino PORT: %s" % com_port	#print which port the Arduino is operating on

ser = serial.Serial(com_port, 9600) # Establish the connection on a specific port
			#make sure you are NOT also displaying from Arduino Serial Monitor (conflict)

midi_out = rtmidi.MidiOut()
midi_out.open_port(0)

no_of_notes = len(argv)-3	#store number of notes to split accelerometer value range into bins
bin_size = 22/no_of_notes +1
print "Number of Notes: %d" %no_of_notes
count=2;					#keep a count at start of notes to loop through argv 
print "Bin Size: %d" %bin_size


#for args in argv[3:]:	#read all command line arguments (notes) after the script name itself
while (1):
	ser.write("t")
	z = float(ser.readline().rstrip()) 

	#There's probably a much better way to do this: (To be examined)

	for i in range(-11,11, bin_size):
		count = count + 1
		print i 	#i will interate through bins, but count will address the note from argv list
		if(z <i ):	#check which bin the input is in
			print(z)
			midi_out.send_message([0x90, int(argv[count]),100])		#this will play note corresponding to whichever bin input is in
			time.sleep(0.3)
			midi_out.send_message([0x80,int(argv[count]),100])
			time.sleep(0.1)
	


#HBD 43(3) 43(1) 45(4) 43(4) 48(4) 47(8); Syntax: note(delay)

