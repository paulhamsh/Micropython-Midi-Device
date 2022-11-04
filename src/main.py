
import time
import device, midi
import ustruct

from machine import Pin
led = Pin(25, Pin.OUT)
led.value(1)

usbd = device.get()
a = midi.AudioUSB()
m = midi.MidiUSB()

#usbd.add_interface(a)
usbd.add_interface(m)
usbd.reenumerate()

led.toggle()

time.sleep(3)  # TODO: provide a way to find out at runtime if an interface is active

led.toggle()

mi_on = ustruct.pack("<BBBB", 0x09, 0x90, 0x20, 0x7f)
mi_off =ustruct.pack("<BBBB", 0x08, 0x80, 0x20, 0x00)

led.toggle()

while True:
    time.sleep(1)
    m.send_midi(mi_on)
    led.toggle()
    
    time.sleep(1)
    m.send_midi(mi_off)
    led.toggle()
