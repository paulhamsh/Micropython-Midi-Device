
import time
import device, midi

usbd = device.get()
#a = midi.AudioUSB()
m = midi.MidiUSB()

#usbd.add_interface(a)
usbd.add_interface(m)
usbd.reenumerate()

time.sleep(3)  # TODO: provide a way to find out at runtime if an interface is active

m.send_midi()

"""
import time
import device, hid

ud = device.get()

m = hid.MouseInterface()
ud.add_interface(m)
ud.reenumerate()

time.sleep(2)  # TODO: provide a way to find out at runtime if an interface is active

m.move_by(-100, 0)
time.sleep(0.25)

m.click_right(True)
time.sleep(0.25)
m.click_right(False)
"""
