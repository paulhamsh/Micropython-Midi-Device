# Micropython-Midi-Device
A basic Midi device for Micropython using projectgus usbd_python   

Based on projectgus work here: https://github.com/projectgus/micropython-lib/tree/feature/usbd_python/micropython/usbd    

In projectgus github, select the micropython-lib repository, select the usbd_python branch and look in micropython-lib/micropython/usbd    


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

Then copy ``device.py`` to your folder (included in src above)    

Official instructions here:    

https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf

