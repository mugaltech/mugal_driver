
import serial
import struct
from  functools import reduce
import libscrc
import enum

from time import sleep

# Command header byte
CMD_HEAD = b'\xAA'

# Command bytes
CMD_CH1 = b'\x00'
CMD_CH2 = b'\x04'
CMD_IDN = b'\x09'

# Command tail byte
CMD_TAIL = b'\x55'

# DDS reference frequency
FREF = 499.2E6 

# Duration time unit
DURATION_UNIT = 1.0E-6

def clamp(num, min_value, max_value):
    ''' clamp num between min_value and max_value.'''
    return max(min(num, max_value), min_value)


def _FTW(freq):
    freq = freq % FREF
    if freq > FREF/2:
        freq = freq - FREF
    return int(round((2**32)*freq/FREF))


class AOD_Segment(object):
    '''A segment of driver state.
    --------
    freq:  frequency in unit (Hz)
    set_power: RF driver power, 0V-3.3V
    duration: in unit (s)
    onoff: 0 for on, 1 for off, others keep onoff of last segment
    '''

    def __init__(self, freq=0.0, set_power=0.0, duration=0.0, onoff=0) -> None:
        super().__init__()
        self.freq = freq
        self.set_power = set_power
        self.duration = duration
        self.onoff = clamp(onoff,0,255)

    def valid(self)->bool:
        change = False
        _freq = _FTW(self.freq)*FREF/2**32
        if _freq != self.freq:
            change = True
            self.freq = _freq
        _duration = clamp(self.duration/DURATION_UNIT,0,2**32-1)*DURATION_UNIT
        if _duration != self.duration:
            change = True
            self.duration = _duration
        _set_power = clamp(self.set_power,0,3.3)
        if _set_power != self._set_power:
            change = True
            self.set_power = _set_power
        return change

    def pack(self):
        duration_num = clamp(self.duration/DURATION_UNIT,0,2**32-1)
        _set_power_num = clamp(self.set_power,0,3.3)/3.3*2**12
        self.duration = duration_num*DURATION_UNIT
        return struct.pack('>lHlB',
            _FTW(self.freq),
            round(_set_power_num),
            int(duration_num),
            self.onoff)

    @classmethod
    def onoff_str(cls, onoff):
        if onoff == 0:
            return "ON"
        if onoff == 1:
            return "OFF"
        else:
            return "Keep"

    def __str__(self) -> str:
        return '<AOD_Segment:freq={:.3e}Hz,set power={:.3e}Hz,duration={:.3e}s and {}>'\
            .format(self.freq,self.set_power,self.duration,self.onoff_str(self.onoff))

    def __repr__(self) -> str:
        return self.__str__()

class AOD_type(enum.Enum):
    Dual_Channel = "DP"
    Single_Channel = "SP"
    Dual_Channel_Fixed_Freq = "D"
    Single_Channel_Fixed_Freq = "S"

class AOD(object):
    ''' Acousto-Optic Modulator driver
    --------
    serial_port : str
        port | device name for LNR device
    baudrate 
        defult baudrate 115200
    open_now: bool
        open serial port when construct LNR object.\\
        default True
    type: 
    '''


    def __init__(self, serial_port, baudrate=115200, open_now=True, type=AOD_type.Dual_Channel) -> None:
        super().__init__()
        self.serial_port = serial_port
        if open_now:
            self.serial = serial.Serial(self.serial_port,baudrate)
            self.baudrate = baudrate
        else:
            self.serial = None
            self.baudrate = baudrate
        self.type=type
        self.segs1=[]
        if self.type == AOD_type.Dual_Channel_Fixed_Freq or self.type == AOD_type.Dual_Channel:
            self.segs2=[]
        self._idn = None

    @property
    def is_open(self) -> bool:
        if self.serial:
            return self.serial.is_open
        else:
            return False

    def open(self):
        if self.serial_port and (not self.serial):
            self.serial = serial.Serial(self.serial_port, self.baudrate)
        elif self.serial:
            self.serial.open()

    def close(self):
        if self.serial:
            self.serial.close()
            
    def send_ch1(self)->bytearray:
        if len(self.segs1) == 0:
            return b''
        if not self.is_open:
            return b''
        segs=self.segs1
        if len(segs)>10:
            segs=self.segs1[:10]
        buffer = CMD_HEAD + CMD_CH1 + struct.pack('B', len(segs)) \
            + reduce(lambda a,b:a+b.pack(), segs, b'')
        checksum = libscrc.modbus(buffer)
        buffer = buffer + struct.pack('>H', checksum)  + CMD_TAIL
        self.serial.write(buffer)
        return buffer

    def send_ch2(self)->bytearray:
        if self.type == AOD_type.Single_Channel_Fixed_Freq or self.type == AOD_type.Single_Channel:
            return b''
        if len(self.segs2) == 0:
            return b''
        if not self.is_open:
            return b''
        segs=self.segs2
        if len(segs)>10:
            segs=self.segs2[:10]
        buffer = CMD_HEAD + CMD_CH2 + struct.pack('B', len(segs)) \
            + reduce(lambda a,b:a+b.pack(), segs, b'')
        checksum = libscrc.modbus(buffer)
        buffer = buffer + struct.pack('>H', checksum)  + CMD_TAIL
        self.serial.write(buffer)
        return buffer

    @property
    def identifier(self)->str:
        if self._idn:
            return self._idn
        if not self.is_open:
            return ''
        buffer = CMD_HEAD + CMD_IDN
        checksum = libscrc.modbus(buffer)
        buffer = buffer + struct.pack('>H', checksum)  + CMD_TAIL
        self.serial.write(buffer)
        sleep(0.02)
        idn = self.serial.read_all()
        self._idn = idn.decode()
        return self._idn

    def __str__(self) -> str:
        if self.type == AOD_type.Dual_Channel or self.type == AOD_type.Dual_Channel_Fixed_Freq:
            return '<AOD-D:port={},baudrate={},with ch1 {} segments and ch2 {} segments>'\
                .format(self.serial_port,self.baudrate,len(self.segs1),len(self.segs2))
        if self.type == AOD_type.Single_Channel or self.type == AOD_type.Single_Channel_Fixed_Freq:
            return '<AOD-S:port={},baudrate={},with ch1 {} segments>'\
                .format(self.serial_port,self.baudrate,len(self.segs1))

    def __repr__(self) -> str:
        return self.__str__()
