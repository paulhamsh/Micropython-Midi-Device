import device, midi, time
import ustruct
from machine import Pin, I2C, Timer
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

m.start()

oled.text("MIDI Device", 0, 0)
oled.text("Starting...", 0, 6)
oled.show()

ticksthen = time.ticks_ms()
noteon = True

while True:
    ticksnow = time.ticks_ms()
    if (time.ticks_diff(ticksnow, ticksthen) > 1000):
        ticksthen = ticksnow
        led.toggle()
        if noteon:
            m.note_on(0, 64, 127)
        else:
            m.note_off(0, 64, 0)
        noteon = not noteon
   
    if m.midi_received():
        (cin, cmd, val1, val2) = m.get_midi()
        if cin is not None:  # not necessary as we checked midi_received()
            #s = str(cmd)
            s = "%2x %2x %2x" % (cmd, val1, val2)
            oled.fill_rect(0, 40, 100, 47, 0)
            oled.text(s, 0, 40)
            oled.show()   

