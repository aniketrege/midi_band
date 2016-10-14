from sys import argv    #to use command line arguments
import serial   #to read COM port using python  
import pyaudio  #to record and play audio
import wave     #to read or write .wav files 
import sys
import time

com_port=argv[1]

if(len(argv)<1):
    print("Usage- python %s COM_PORT"%(argv[0]))
    exit(0)

print "Using COM port- " + com_port
ser = serial.Serial(com_port, 9600) #setting up the serialcommuication b/w python and COM port
print "Press button once to record audio:"
prevcount=0

def record_audio():                 #function to record audio from laptop or microphone
        CHUNK = 1024                #we'll read 1 chunk of size 1024 from stream of digital stram of audio signal
        FORMAT = pyaudio.paInt16
        CHANNELS = 20000            #stereo mode
        RATE = 44100                #sample rate..frequency at which we talk=20hz to 20000khz we'll use double of this freq 44.1khz for good sampling
        RECORD_SECONDS = 10         #we can set this value 
        WAVE_OUTPUT_FILENAME = "apt.wav"

        p = pyaudio.PyAudio()       #setting up pyaudio

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

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  #opening a file in write mode('wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))            #writing all the chunks present in frames list to wav file
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


while(1):
    
        count=ser.readline().rstrip()
        count=int(count)
        if((count%2==1)and (prevcount!=count)):
                record_audio()
                print "Press button once to play audio:"

                
        elif(count%2==0):
            if((count!=0) and (prevcount!=count)):
                a = AudioFile("apt.wav")
                print "Playing audio...\n"
                a.play()
                a.close()
                print "Done\n"
                print "Press button once to record audio:"

       
        prevcount=count




