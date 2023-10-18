# Micropython-Midi-Device
A basic Midi device for Micropython using projectgus usbd_python   

https://github.com/projectgus/micropython/tree/feature/usbd_python   

Will send a note on note off every second, and receive notes and show ON / OFF on an OLED screen.      

# Install instuctions for Micropython


```
cd ~
git clone https://github.com/projectgus/micropython -b feature/usbd_python
cd micropython
sudo apt-get install build-essential libffi-dev git pkg-config

cd mpy-cross
make

cd ..
cd port/rp2
make submodules
cmake .
make
```

Then copy device.py and machine.py to your folder (included in src above)    

Official instructions here:    

https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf

