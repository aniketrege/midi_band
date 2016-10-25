from sys import argv    #to use command line arguments
import serial   #to read COM port using python  
import pyaudio  #to record and play audio
import wave     #to read or write .wav files 
import sys
from random import uniform
import time
from array import array
from struct import pack
from sys import byteorder
import copy
import rtmidi_python as rtmidi
from scipy import *
from pylab import *
from scipy.io import wavfile
from pygame import *
from mido import *
from mido import Message

import mido 
import pygame 
import time 


mido.set_backend("mido.backends.pygame")
names = mido.get_output_names()
print names

outport = mido.open_output(names[3])
midi_out = rtmidi.MidiOut()
midi_out.open_port(0)

ON=0x90
OFF=0x80
count=[0,0,0,0,0,0,0,0,0]
prevcount=[0,0,0,0,0,0,0,0,0]
prev_note=0
k=0
j=0
l=1
d=1
w=0
i=0
drum_notes=[27, 66, 69, 77, 63, 89, 111, 68, 76]
#["D#1","F#4","A4","F5","D#4","F6","D#8","G#4","A#9"]#change notes= names with hex numbers
master_count=0;
sel_count=0;
file_array=["1.wav","2.wav","3.wav","4.wav","5.wav","6.wav","7.wav","8.wav","9.wav"]
frequency_array=["f1.wav","f2.wav","f3.wav","f4.wav","f5.wav","f6.wav","f7.wav","f8.wav","f9.wav"]


if(len(argv)<3):
    print("Usage- python %s COM_PORT note1 [note2 note3 ...]"%(argv[0]))
    exit(0)

com_port=argv[1]
print "Using COM port- " + com_port

notes=[]

if(len(argv)>2):
    for note in argv[2:]:               # append all notes (params) passed in command line
        notes.append(note)
ser = serial.Serial(com_port, 9600)     #setting up the serialcommuication b/w python and COM port

def loadfile(infile):
    return wavfile.read(infile)

def sound_stretch(infile, stretching_factor, outfile):
    N = 2048
    H = N/4


    # read input and get the timescale factor
    (sr,signal) = loadfile(infile)
    if(len(signal[0]) == 2):
        signal2 = []
        for i,j in signal:
            signal2.append(i)
        signalin = np.array(signal2)
    L = len(signalin)
    tscale = float(stretching_factor)
    # signal blocks for processing and output
    phi  = zeros(N)
    out = zeros(N, dtype=complex)
    sigout = zeros(int(L/tscale)+N)

    print signalin

    # max input amp, window
    amp = max(signalin)
    win = hanning(N)
    p = 0
    pp = 0

    while p < L-(N+H):

        # take the spectra of two consecutive windows
        p1 = int(p)
        spec1 =  fft(win*signalin[p1:p1+N])
        spec2 =  fft(win*signalin[p1+H:p1+N+H])
        # take their phase difference and integrate
        phi += (angle(spec2) - angle(spec1))
        # bring the phase back to between pi and -pi
        while phi.all() < -pi: phi += 2*pi
        while phi.all() >= pi: phi -= 2*pi
        out.real, out.imag = cos(phi), sin(phi)
        # inverse FFT and overlap-add
        sigout[pp:pp+N] += win*ifft(abs(spec2)*out).real
        pp += H
        p += H*tscale
    return sr, array(amp*sigout/max(sigout), dtype='int16')

def record_audio(filename):#function to record audio from laptop or microphone
        CHUNK = 1024#we'll read 1 chunk of size 1024 from stream of digital stram of audio signal
        FORMAT = pyaudio.paInt16
        CHANNELS = 2#stereo mode
        RATE = 44100#sample rate..frequency at which we talk=20hz to 20000khz we'll use double of this freq 44.1khz for good sampling
        RECORD_SECONDS = 5#we can set this value 
        WAVE_OUTPUT_FILENAME = filename

        p = pyaudio.PyAudio()#setting up pyaudio

        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        
        if (1):
                print "* Recording audio..."

        frames = []#list to store all the chunks of audio
        """
                we have samplerate=(number of samples)per second=441000
                samplerate*recorseconds-----this gives total number of samples
                number of chunks=number of samples/chunksize
                in our case number of chunks=215
                hence we neet to read or run for loop 215 time to read 215 chunks of audio
        """
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)#appending all the chunks in to a list called frames

        
        print "* done\n" 

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')#opening a file in write mode('wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))#writing all the chunks present in frames list to wav file
        wf.close()



class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """ 
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = self.p.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)#read the wav file one chunk after another
        while data != '':#all chunks are seperated by an white space character(delimiter)
            self.stream.write(data)#writing data chunks is same as play that particular chunk
            data = self.wf.readframes(self.chunk) #moves from the present chunk to next chunk

    def close(self):
        """ Graceful shutdown """ 
        self.stream.close()
        self.p.terminate()



#*******************************        CONTROL         START           *************************************

IN=0
while(1):  
        i=0
        
        output_from_ard =  ser.readline().rstrip()
        counts = output_from_ard.split()
        master_count=int(counts[0].rstrip())
        sel_count=int(counts[1].rstrip()) 
        print master_count
        print sel_count
        for i in range(2,11):
                count[i-2]=int(counts[i].rstrip())  #count[i] is the number of times ith button has been pressed
        print count
        if(sel_count%2==0):
            if(master_count%5==0 and IN==0):
                print("Press master button to select modes:")
                IN=1


            
    #****************************           MODE ONE            *********************************************
        else:
            if(master_count%5==0 and IN==0):
                print("Press master button to select modes:")
                IN=1
            if(master_count%5==1):
                    for i in range(0,9):
                            if((count[i]%2==1)and (prevcount[i]!=count[i])):
                                    k=i
                                    break
                    if(j<9):
                            if((count[k]%2==1)and (prevcount[k]!=count[k])):
                                    record_audio(file_array[k])
                                    j=j+1
                                    if(j==9):
                                            print "All 9 buttons were mapped to their respective audio_recordings"
                                            prevcount[k]=count[k]
                                            continue
                                            
                    if(j==9):
                            if((count[k]!=0) and (prevcount[k]!=count[k])):
                                    a = AudioFile(file_array[k])
                                    print "Playing audio..."
                                    a.play()
                                    a.close()
                                    print "Done"
                    prevcount[k]=count[k]


        #****************************           MODE TWO            *********************************************


            if(master_count%5==2):
                if(d==1):
                    prevcount=[0,0,0,0,0,0,0,0,0]
                    if(l==1):
                        print "press button one in 3*3 matrix to start recording:"
                        l=2
                    if(count[0]!=prevcount[0] or count[0]==1):
                        record_audio("f.wav")
                        w=1
                        d=2
                    if(w==1):
                        stretching_factor = 1
                        infile="f.wav"
                        k=0
                        for i in range(1,13):
                            if(i==3 or i==7 or i==11):
                                continue
                            outfile=frequency_array[k]
                            k=k+1
                            sr, signal = sound_stretch(infile, (1/pow(2,i/12.0)), outfile)
                            sr = sr*pow(2,i/12.0)
                            wavfile.write(outfile, sr, signal)
                        print "all 8 buttons mapped to 8 different frequencies of recorded audio"
                        print "press buttons to play..."
                        for i in range(0,9):
                            prevcount[i]=count[i]
                k=0
                for i in range(1,9):
                    if(prevcount[i]!=count[i]):
                            k=i
                            break
                if(k!=0):
                        a = AudioFile(frequency_array[k-1])
                        print "playing audio..."
                        a.play()
                        a.close()
                        print "done"
                prevcount[k]=count[k]
                prevnote=0



        #****************************           MODE THREE          *********************************************



            if(master_count%5==3):
                if(d==1):
                    prevcount=[0,0,0,0,0,0,0,0,0]
                d=2
                for i in range(0,9):
                            if(prevcount[i]!=count[i]):
                                    k=i
                                    break
                current_note=notes[k]
                if(prev_note!=current_note and prev_note!=0):
                    msg=Message("note_off", channel=0,note=int(prev_note), velocity=100)
                    outport.send(msg)    
                if(count[k]!=prevcount[k]):
                    print "playing note..."+str(current_note)
                    msg=Message("note_on", channel=0,note=int(current_note), velocity=100)
                    outport.send(msg)
                prev_note=current_note 
                prevcount[k]=count[k]   



        #****************************           MODE FOUR          *********************************************       
                

            
            if(master_count%5==4):
                if(d==1):
                    prevcount=[0,0,0,0,0,0,0,0,0]
                d=2
                for i in range(0,9):
                            if(prevcount[i]!=count[i]):
                                    k=i
                                    break
                current_note=drum_notes[k]
                #if(prev_note!=current_note and prev_note!=0):
                    #msg=Message("note_off", channel=0,note=int(prev_note), velocity=100)
                    #outport.send(msg)    
                if(count[k]!=prevcount[k]):
                    print "playing note..."+str(current_note)
                    msg=Message("note_on", channel=0,note=int(current_note), velocity=100)
                    outport.send(msg)
                prev_note=current_note 
                prevcount[k]=count[k]       





            
#python matrix_py_sync.py COM3 60 62 64 66 68 70