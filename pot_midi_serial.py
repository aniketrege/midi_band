import serial
import pyaudio
import rtmidi_python as rtmidi
import time

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

oldtemp=int(ser.readline())

while(1):
    pot=int(ser.readline())
    msg(pot,oldtemp)
    print pot

ser.close()
print "serial closed"

