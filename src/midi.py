# MicroPython USB MIDI module
# MIT license; Copyright (c) 2022 Angus Gratton, Paul Hamshere
from device import USBInterface
from micropython import const
import ustruct

dat = bytearray(64)

_INTERFACE_CLASS_IGNORE = 0x01
_INTERFACE_SUBCLASS_IGNORE = 0x01
_PROTOCOL_IGNORE = 0x00


class RingBuf:
    def __init__(self, size):
        self.data = bytearray(size)
        self.size = size
        self.index_put = 0
        self.index_get = 0
        
    def put(self, value):
        next_index = (self.index_put + 1) % self.size
        # check for overflow
        if self.index_get != next_index: 
            self.data[self.index_put] = value
            self.index_put = next_index
            return value
        else:
            return None
        
    def get(self):
        if self.index_get == self.index_put:
            return None  ## buffer empty
        else:
            value = self.data[self.index_get]
            self.index_get = (self.index_get + 1) % self.size
            return value
        
    def is_empty(self):
        return (self.index_get == self. index_put)
        

class AudioInterface(USBInterface):
    """ Abstract base class to implement a USB MIDI device in Python. """
    def __init__(self):
        super().__init__(
            _INTERFACE_CLASS_IGNORE, _INTERFACE_SUBCLASS_IGNORE, _PROTOCOL_IGNORE, 0x00
        )

        
    def get_itf_descriptor(self, num_eps, itf_idx, str_idx):
        """Return the MIDI USB interface descriptors.
        """
        
        ms_interface = ustruct.pack(
            "<BBBBBBBBB",
            9,        # bLength
            0x04,     # bDescriptorType INTERFACE
            itf_idx,  # bInterfaceNumber
            0x00,     # bAlternateSetting
            0x00,     # bNumEndpoints
            0x01,     # bInterfaceClass AUDIO
            0x01,     # bInterfaceSubclass AUDIO_CONTROL
            0x00,     # bInterfaceProtocol
            0x00      # iInterface
        )
        cs_ms_interface = ustruct.pack(
            "<BBBHHBB",
            9,      # bLength
            0x24,   # bDescriptorType CS_INTERFACE
            0x01,   # bDescriptorSubtype MS_HEADER
            0x0100, # BcdADC
            0x0009, # wTotalLength
            0x01,   # bInCollection,
            0x01    # baInterfaceNr
        )

        iface =  ms_interface + cs_ms_interface    
        return (iface, [])
        #return (b"", [])


class MIDIInterface(USBInterface):
    """ Base class to implement a USB MIDI device in Python. """
    def __init__(self):
        super().__init__(
            _INTERFACE_CLASS_IGNORE, _INTERFACE_SUBCLASS_IGNORE, _PROTOCOL_IGNORE, 0x00
        )
        self.ep_out = 0x03  # set during enumeration
        self.ep_in = 0x83
        self.got_data = False
        self.rx_data = bytearray(64)
        self.rb = RingBuf(128)


    def send_data(self, tx_data):
        """ Helper function to send data. """
        self.submit_xfer(0x83, tx_data)

    def midi_received(self):
        return not self.rb.is_empty()

    def get_rb(self):
        return self.rb.get()

    def receive_data_callback(self, ep_addr, result, xferred_bytes):
        for i in range (0, xferred_bytes):
            self.rb.put(self.rx_data[i])
        self.submit_xfer(0x03, self.rx_data, self.receive_data_callback)       

    def start_receive_data(self):
        self.submit_xfer(0x03, self.rx_data, self.receive_data_callback) # self.receive_data_callback)

    def get_itf_descriptor(self, num_eps, itf_idx, str_idx):
        """Return the MIDI USB interface descriptors.  """

        ms_interface = ustruct.pack(
            "<BBBBBBBBB",
            9,        # bLength
            0x04,     # bDescriptorType INTERFACE
            itf_idx,  # bInterfaceNumber
            0x00,     # bAlternateSetting
            0x02,     # bNumEndpoints
            0x01,     # bInterfaceClass AUDIO
            0x03,     # bInterfaceSubclass MIDISTREAMING
            0x00,     # bInterfaceProtocol
            0x00      # iInterface
        )
        cs_ms_interface = ustruct.pack(
            "<BBBHH",
            7,      # bLength
            0x24,   # bDescriptorType CS_INTERFACE
            0x01,   # bDescriptorSubtype MS_HEADER
            0x0100, # BcdADC
            0x0041  # wTotalLength
        )

        jack1 = ustruct.pack(
            "<BBBBBB",
            6,     # bLength
            0x24,  # bDescriptorType CS_INTERFACE
            0x02,  # bDescriptorSubtype MIDI_IN_JACK
            0x01,  # bJackType EMBEDDED
            0x01,  # bJackID
            0x00   # iJack
        )
        jack2 = ustruct.pack(
            "<BBBBBB",
            6,     # bLength
            0x24,  # bDescriptorType CS_INTERFACE
            0x02,  # bDescriptorSubtype MIDI_IN_JACK
            0x02,  # bJackType EXTERNAL
            0x02,  # bJackID
            0x00   # iJack
        )
        jack3 = ustruct.pack(
            "<BBBBBBBBB",
            9,     # bLength
            0x24,  # bDescriptorType CS_INTERFACE
            0x03,  # bDescriptorSubtype MIDI_OUT_JACK
            0x01,  # bJackType EMBEDDED
            0x03,  # bJackID
            0x01,  # bNrInputPins
            0x02,  # BaSourceID
            0x01,  # BaSourcePin
            0x00   # iJack
        ) 
        jack4 = ustruct.pack(
            "<BBBBBBBBB",
            9,     # bLength
            0x24,  # bDescriptorType CS_INTERFACE
            0x03,  # bDescriptorSubtype MIDI_OUT_JACK
            0x02,  # bJackType EXTERNAL
            0x04,  # bJackID
            0x01,  # bNrInputPins
            0x01,  # BaSourceID
            0x01,  # BaSourcePin
            0x00   # iJack
        )
        iface =  ms_interface + cs_ms_interface + jack1 + jack2 + jack3 + jack4
        return (iface, [])

    def get_endpoint_descriptors(self, ep_addr, str_idx):
        """Return the MIDI USB endpoint descriptors.
        """
    
        epA = ustruct.pack(
            "<BBBBHBBB",
            9,      # bLength
            0x05,   # bDescriptorType ENDPOINT
            0x03,   # bEndpointAddress 
            0x02,   # bmAttributes
            0x0040, # wMaxPacketSize
            0x00,   # bInterval
            0x00,   # bRefresh
            0x00    # bSyncAddress
        )
        cs_epA = ustruct.pack(
            "<BBBBB",
            5,     # bLength
            0x25,  # bDescriptorType CS_ENDPOINT
            0x01,  # bDescriptorSubtype MS_GENERAL
            0x01,  # bNumEmbMIDIJack
            0x01   # BaAssocJackID
        )
        epB = ustruct.pack(
            "<BBBBHBBB",
            9,      # bLength
            0x05,   # bDescriptorType ENDPOINT
            0x83,   # bEndpointAddress 
            0x02,   # bmAttributes
            0x0040, # wMaxPacketSize
            0x00,   # bInterval
            0x00,   # bRefresh
            0x00    # bSyncAddress
        )
        cs_epB = ustruct.pack(
            "<BBBBB",
            5,     # bLength
            0x25,  # bDescriptorType CS_ENDPOINT
            0x01,  # bDescriptorSubtype MS_GENERAL
            0x01,  # bNumEmbMIDIJack
            0x03   # BaAssocJackID
        )    
        
        desc = epA + cs_epA + epB + cs_epB
        ep_addr = [0x03, 0x83]
        return (desc, [], ep_addr)


class AudioUSB(AudioInterface):
    """ Empty USB Audio interface """
    def __init__(self):
        super().__init__()
        
class MidiUSB(MIDIInterface):
    """ Very basic synchronous USB MIDI interface """
    def __init__(self):
        super().__init__()

    def note_on(self, channel, pitch, vel):
        obuf = ustruct.pack("<BBBB", 0x09, 0x90 | channel, pitch, vel)
        super().send_data(obuf)
        
    def note_off(self, channel, pitch, vel):
        obuf = ustruct.pack("<BBBB", 0x08, 0x80 | channel, pitch, vel)
        super().send_data(obuf)     
        
    def start(self):
        super().start_receive_data()
    
    def midi_received(self):
        return super().midi_received()
  
    def get_midi(self):
        if super().midi_received():
            cin = super().get_rb()
            cmd = super().get_rb()
            val1 = super().get_rb()
            val2 = super().get_rb()
            return (cin, cmd, val1, val2)
        else:
            return (None, None, None, None)
            

