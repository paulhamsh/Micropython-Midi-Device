
import time
import device, midi

usbd = device.get()
a = midi.AudioUSB()
m = midi.MidiUSB()

usbd.add_interface(a)
usbd.add_interface(m)
usbd.reenumerate()

time.sleep(3)  # TODO: provide a way to find out at runtime if an interface is active

mi= ustruct.pack("<BBBB", 0x09, 0x90, 0x20, 0xff)

while True:
    time.sleep(1)
    m.send_midi(mi)

