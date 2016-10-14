from sys import argv    #to use command line arguments
import serial   #to read COM port using python  
import pyaudio  #to record and play audio
import wave     #to read or write .wav files 
import sys
import time
from array import array
from struct import pack
from sys import byteorder
import copy

if(len(argv)<2):
    print("Usage- python %s COM_PORT"%(argv[0]))
    exit(0)

com_port=argv[1]
print "Using COM port- " + com_port
ser = serial.Serial(com_port, 9600)#setting up the serialcommuication b/w python and COM port
print "Press button once to record audio:"
prevcount=0

def record_audio():

        THRESHOLD = 500 # audio levels not normalised.
        CHUNK_SIZE = 1024
        SILENT_CHUNKS = 3 * 44100 / 1024  # about 3sec
        FORMAT = pyaudio.paInt16
        FRAME_MAX_VALUE = 2 ** 15 - 1
        NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
        RATE = 44100
        CHANNELS = 1
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
            """Record a word or words from the microphone and 
            return the data as an array of signed shorts."""

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
            record_to_file('demo.wav')
            print("Done - result written to demo.wav")

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

        
while(1):
        count=ser.readline().rstrip()
        count=int(count)
        if((count%2==1)and (prevcount!=count)):
                record_audio()
                print "Press button once to play audio:"

                
        elif(count%2==0):
            if((count!=0) and (prevcount!=count)):
                a = AudioFile("demo.wav")
                print "Playing audio..."
                a.play()
                a.close()
                print "Done"
                print "Press button once to record audio:"

       
        prevcount=count




