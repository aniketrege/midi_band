MIDI BAND

Welcome to MIDI BAND, a project from TECHNITES, the flagship event of ENGINEER, the annual tech fest
of the National Institute of Technology, Karnataka, India.

Here we present a variety of musical instruments, including an "Air Piano", "Sound Sensor Flute," "Laser Harp,"
"Voice Synthesizer," and "Musical Accelerometer Air Glove."

The instruments are controlled using an Arduino Microcontroller, and designed using a variety of analog sensors
and actuators mounted on tools, all mapped to LED sync for an aesthetically pleasing musical experience.

Processing is done in Python via PySerial wherever possible, to avoid load on the Arduino, a relatively less powerful
computing device. 

Welcome again, and enjoy your musical experience with MIDI Band! 

MIDI FLUTE

This instrument sounds almost similar to its acoustic counterpart thanks to MIDI CC messages that
controls the volume of the flute based on the intensity of the blow on the flute. On the software side
FL Studio is used for processing MIDI messages and hairless midi and loopMIDI for interfacing COM 
port with FL Studio. On the other side of COM port sits the arduino reading the flute and sending 
corresponding MIDI commands. And while it does sounds nice the LEDs on the flute takes care that 
it also "looks" nice.
