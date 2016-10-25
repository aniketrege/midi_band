import sys

#sys.path.append("C:\Python27\Lib\site-packages\mido")
#sys.path.append("C:\Python27\Lib\site-packages\mido-1.1.17-py2.7.egg-info")
#import time


from mido import Message

import mido



msg= Message("note_on", note=60)
print msg 
mido.set_backend('mido.backends.rtmidi_python')
names = mido.get_output_names()
print(names)

with mido.open_input("new_port", virtual=True) as inport:
	for message in inport:
		print message 
'''
output = mido.open_output(names[0])
while(1):
	output.send(mido.Message('note_on', note=60, velocity=64))
	time.sleep(0.3)
	output.send(mido.Message('note_off', note=60, velocity=64))
	time.sleep(0.1)


import time
import mido
import rtmidi
from mido import Message

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

# Original example:
# note_on = [0x99, 60, 112] # channel 10, middle C, velocity 112
# note_off = [0x89, 60, 0]

note_on = mido.Message('note_on', channel=9, note=60, velocity=112).bytes()
note_off = mido.Message('note_off', channel=9, note=60, velocity=0).bytes()
midiout.send_message(note_on)
time.sleep(0.5)
midiout.send_message(note_off)

del midiout
'''