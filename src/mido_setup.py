from pygame import *
from mido import *
from mido import Message

import mido 
import pygame 
import time 

mido.set_backend("mido.backends.pygame")
names = mido.get_output_names()
print names
msg = Message("note_on", channel=0, note=60, velocity=64)
print msg
outport = mido.open_output(names[3])

for i in range(60,66):
	msg = Message("note_on", channel=0, note=i, velocity=64)
	outport.send(msg)
	
	for j in range(0,127):
		cc = Message("control_change", channel= 0, control= 10 , value=j)
		outport.send(cc)
		time.sleep(0.05)
	
	time.sleep(0.2)
	msg = Message("note_off", channel=0, note=i, velocity=64)
	time.sleep(0.2)
	outport.send(msg)

	