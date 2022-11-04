import time
import device, midi
import ustruct
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c=I2C(1,sda=Pin(2), scl=Pin(3), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

led = Pin(25, Pin.OUT)
led.value(1)


oled.text("MIDI Device", 0, 0)
oled.show()

usbd = device.get()
a = midi.AudioUSB()
m = midi.MidiUSB()

#usbd.add_interface(a)
usbd.add_interface(m)
usbd.reenumerate()

led.toggle()

time.sleep(3)  # TODO: provide a way to find out at runtime if an interface is active

led.toggle()

mo_on = ustruct.pack("<BBBB", 0x09, 0x90, 0x20, 0x7f)
mo_off =ustruct.pack("<BBBB", 0x08, 0x80, 0x20, 0x00)

#m.receive_midi()

oled.text("MIDI Device", 0, 0)
oled.text("Starting...", 0, 6)
oled.show()

while True:
    time.sleep(2)
    m.send_midi(mo_on)
    led.toggle()
    
    time.sleep(2)
    m.send_midi(mo_off)
    led.toggle()
    
    if m.got_data:
        oled.text("GOT DATA", 0, 16)
        oled.show()
        
    

