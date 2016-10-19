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

midi_out = rtmidi.MidiOut()
midi_out.open_port(0)


count=[0,0,0,0,0,0,0,0,0]
prevcount=[0,0,0,0,0,0,0,0,0]
prev_note=0
k=0
j=0
d=1
w=0
i=0
drum_notes=[]
master_count=0;
sel_count=0;
file_array=["1.wav","2.wav","3.wav","4.wav","5.wav","6.wav","7.wav","8.wav","9.wav"]
frequency_array=["f1.wav","f2.wav","f3.wav","f4.wav","f5.wav","f6.wav","f7.wav","f8.wav"]


if(len(argv)<2):
    print("Usage- python %s COM_PORT "%(argv[0]))
    exit(0)


com_port=argv[1]
print "Using COM port- " + com_port

notes=[]

if(len(argv)>2):
    for note in argv[2:]:       # append all notes (params) passed in command line
        notes.append(note)
ser = serial.Serial(com_port, 9600)#setting up the serialcommuication b/w python and COM port

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



def record_audio(filename):

        THRESHOLD = 500 # audio levels not normalised.
        CHUNK_SIZE = 1024
        SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
        FORMAT = pyaudio.paInt16
        FRAME_MAX_VALUE = 2 ** 15 - 1
        NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
        RATE = 44100
        CHANNELS = 2
        TRIM_APPEND = RATE / 4

        def is_silent(data_chunk):
            """Returns 'True' if below the 'silent' threshold"""
            return max(data_chunk) < THRESHOLD

        def normalize(data_all):
            """Amplify the volume out to max -1dB"""
            # MAXIMUM = 16384
            normalize_factor = (float(NORMALIZE_MINUS_ONE_dB * FRAME_MAX_VALUE)/ max(abs(i) for i in data_all))
                                                                                        

            r = array('h')
            for i in data_all:
                r.append(int(i * normalize_factor))
            return r

        def trim(data_all):
            _from = 0
            _to = len(data_all) - 1
            for i, b in enumerate(data_all):
                if abs(b) > THRESHOLD:
                    _from = max(0, i - TRIM_APPEND)
                    break

            for i, b in enumerate(reversed(data_all)):
                if abs(b) > THRESHOLD:
                    _to = min(len(data_all) - 1, len(data_all) - 1 - i + TRIM_APPEND)
                    break

            return copy.deepcopy(data_all[_from:(_to + 1)])

        def record():
            """Record a word or words from the microphone and return the data as an array of signed shorts."""

            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

            silent_chunks = 0
            audio_started = False
            data_all = array('h')

            while True:
                # little endian, signed short
                data_chunk = array('h', stream.read(CHUNK_SIZE))
                if byteorder == 'big':
                    data_chunk.byteswap()
                data_all.extend(data_chunk)

                silent = is_silent(data_chunk)

                if audio_started:
                    if silent:
                        silent_chunks += 1
                        if silent_chunks > SILENT_CHUNKS:
                            break
                    else: 
                        silent_chunks = 0
                elif not silent:
                    audio_started = True              

            sample_width = p.get_sample_size(FORMAT)
            stream.stop_stream()
            stream.close()
            p.terminate()

            data_all = trim(data_all)  # we trim before normalize as threshhold applies to un-normalized wave (as well as is_silent() function)
            data_all = normalize(data_all)
            return sample_width, data_all

        def record_to_file(path):
            "Records from the microphone and outputs the resulting data to 'path'"
            sample_width, data = record()
            data = pack('<' + ('h' * len(data)), *data)

            wave_file = wave.open(path, 'wb')
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(sample_width)
            wave_file.setframerate(RATE)
            wave_file.writeframes(data)
            wave_file.close()

        if __name__ == '__main__':
            print("Wait in silence to begin recording; wait in silence to terminate")
            record_to_file(filename)
            print("done - result written to ")+str(filename)


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
print "k"
while(1):
        print "kamal"   
        i=0

        output_from_ard =  ser.readline().rstrip()
        counts = output_from_ard.split()
        master_count=int(counts[0].rstrip())
        sel_count=int(counts[1].rstrip()) 
        for i in range(2,11):
                count[i-2]=int(counts[i].rstrip()) 
                print count[i-2]     
        print master_count
        print sel_count      
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
                                            print "all the 9 buttons were mapped to their respective audio_recordings"
                                            prevcount[k]=count[k]
                                            continue
                                            
                    if(j==9):
                            if((count[k]!=0) and (prevcount[k]!=count[k])):
                                    a = AudioFile(file_array[k])
                                    print "playing audio..."
                                    a.play()
                                    a.close()
                                    print "done"
                    prevcount[k]=count[k]


        #****************************           MODE TWO            *********************************************


            if(master_count%5==2):
                if(d==1):
                    prevcount=[0,0,0,0,0,0,0,0,0]
                d=2
                print "press button one in 3*3 matrix to start recording:"
                if(count[0]!=prevcount[0] or count[0]==1):
                    record_audio("f.wav")
                    w=1
                if(w==1):
                    stretching_factor = 1
                    infile="f.wav"
                    k=0
                    for i in range(1,13):
                        if(i==3 or i==7 or i==11):
                            continue
                        k=k+1
                        outfile=frequency_array[k-1]
                        sr, signal = sound_stretch(infile, (1/pow(2,i/12.0)), outfile)
                        sr = sr*pow(2,i/12.0)
                        wavfile.write(outfile, sr, signal)
                    print "all 8 buttons mapped to 8 different frequencies of recorded audio"
                    print "press buttons to play..."
                    for i in range(2,9):
                        if(prevcount[i]!=count[i]):
                                k=i
                                break
                        if((count[k]!=0) and (prevcount[k]!=count[k])):
                                a = AudioFile(frequency_array[k])
                                print "playing audio..."
                                a.play()
                                a.close()
                                print "done"
                    prevcount[k]=count[k]



        #****************************           MODE THREE          *********************************************



            if(master_count%5==3):
                if(d==1):
                    prevcount=[0,0,0,0,0,0,0,0,0]
                d=2
                for i in range(0,9):
                            if((count[i]%2==1)and (prevcount[i]!=count[i])):
                                    k=i
                                    break
                current_note=notes[k]
                if(prev_note!=current_note and prev_note!=0):
                    midi_out.send_message([OFF, int(prev_note),100])
                if(count[k]==prevcount[k] and count[k]%2==1):
                    print "playing note..."+str(current_note)
                    midi_out.send_message([ON, int(current_note),100])
                prev_note=current_note    


        #****************************           MODE FOUR          *********************************************       
                

            if(master_count%5==4):
                if(d==1):
                    prevcount=[0,0,0,0,0,0,0,0,0]
                d=2
                for i in range(0,9):
                            if((count[i]%2==1)and (prevcount[i]!=count[i])):
                                    k=i
                                    break
                current_note=drum_notes[k]
                if(prevnote!=current_note and prev_note!=0):
                    midi_out.send_message([OFF, int(prev_note),100])
                if(count[k]==prevcount[k] and count[k]%2==1):
                    print "playing note..."+str(current_note)
                    midi_out.send_message([ON, int(current_note),100])
                prev_note=current_note    





            
#python python_3_3_matrix_4modes.py COM3