#changes
#1. Modify loadfile to read from audio source (On Unix systems, its essentially the same thing)

# phase vocoder example
# (c) V Lazzarini, 2010
# GNU Public License
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import sys

from scipy import *
from pylab import *
from scipy.io import wavfile

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

infile  = "../test/phase_vocoder/hello.wav"
stretching_factor = 1
outfile = "../test/phase_vocoder/hello"

for i in range(1,13):
    if(i==3 or i==7 or i==11):
        continue
    sr, signal = sound_stretch(infile, (1/pow(2,i/12.0)), outfile)
    sr = sr*pow(2,i/12.0)
    wavfile.write(outfile+str(i)+".wav", sr, signal)



