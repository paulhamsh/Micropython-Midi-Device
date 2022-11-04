# Micropython-Midi-Device
A basic Midi device for Micropython using projectgus usbd_python   

https://github.com/projectgus/micropython/tree/feature/usbd_python   


DOESN'T WORK YET

I had a problem in getting the descriptors to look right, but I put in some debugging and fixed that.   
So now it looks like a good set of descriptors, but doesn’t really work for midi.   
If I put in the first empty Audio interface, nothing works.   
If I leave it as just the MIDI Interface, it worked for a few times (a single message made it, or some in bulk, like they got suck somewhere).   

This is under Windows 10 using MixiOx to look for midi messages.   
MidiView in Windows works ok.   
I haven't installed any 'driver' .inf files for this - the TinyUSB midi device test program didn't need it (and I think the embedded midi in Circuitpython didn't need a 'driver' inf file either).   
   


