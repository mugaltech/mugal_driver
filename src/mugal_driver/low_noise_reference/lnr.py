
import serial
import struct
from  functools import reduce
import libscrc

# Comand header byte
CMD_HEAD = b'\xAA'

# Comand tail byte
CMD_TAIL = b'\x55'

# DDS reference frequency
FREF = 300.0E6 

# Duration time unit
DURATION_UNIT = 10.0E-6

# DDS sweep step time unit
DT_UNIT = 1.0/FREF

def clamp(num, min_value, max_value):
    ''' clamp num between min_value and max_value.'''
    return max(min(num, max_value), min_value)


def _FTW(freq):
    freq = freq % FREF
    if freq > FREF/2:
        freq = freq - FREF
    return int(round((2**48)*freq/FREF))

class LNR_Segment(object):
    '''A segment of frequency step modes.
    --------
    mode 
        0 for single frequency
        1 for linear frequency sweep
    freq_start: float :unit Hz
        frequency for single frequency mode\\
        start frequency for sweep mode
    df: float :unit  Hz
        frequency step for sweep mode
    dt: float :unit s
        step time for sweep mode
    duration: float :unit s
        duration of sweep, after that time goes to next segment
    '''

    def __init__(self, mode=0, freq_start=80.0E6, df=0.0, dt=0.0, duration=0) -> None:
        super().__init__()
        self.mode = mode
        self.freq_start = freq_start
        self.df = df
        self.dt = dt
        self.duration = duration

    def pack(self):
        dt_num = clamp(self.dt/DT_UNIT-1,0,2**32-1)
        self.dt=(dt_num+1)*DT_UNIT
        duration_num = clamp(self.duration/DURATION_UNIT,0,2**16-1)
        self.duration = duration_num*DURATION_UNIT
        return struct.pack('>BqqLH',self.mode,
            _FTW(self.freq_start),
            _FTW(self.df),
            int(dt_num),
            int(duration_num))

    def __str__(self) -> str:
        return '<LNR_Segment:mode={},start freq={:.3e}Hz,df={:.3e}Hz,dt={:.3e}s and duration={:.3e}s>'\
            .format(self.mode,self.freq_start,self.df,self.dt,self.duration)

    def __repr__(self) -> str:
        return self.__str__()

class LNR(object):
    ''' Low noise referene signal generator
    --------
    serial_port : str
        port | device name for LNR device
    baudrate 
        defult baudrate 115200
    open_now: bool
        open serial port when construct LNR object.\\
        default True
    '''
    def __init__(self, serial_port, baudrate=115200, open_now=True) -> None:
        super().__init__()
        self.serial_port = serial_port
        if open_now:
            self.serial = serial.Serial(self.serial_port,baudrate)
            self.baudrate = baudrate
        else:
            self.serial = None
            self.baudrate = baudrate
        self.segs=[]

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
            
    def send(self):
        if len(self.segs) == 0:
            return
        if not self.is_open:
            return
        segs=self.segs
        if len(segs)>10:
            segs=self.segs[:10]
        buffer = CMD_HEAD + struct.pack('B', len(segs)) \
            + reduce(lambda a,b:a+b.pack(), segs, b'')
        checksum = libscrc.modbus(buffer)
        buffer = buffer + struct.pack('>H', checksum)  + CMD_TAIL
        self.serial.write(buffer)
        return buffer

    def __str__(self) -> str:
        return '<LNR:port={},baudrate={},with {} segments>'\
            .format(self.serial_port,self.baudrate,len(self.segs))

    def __repr__(self) -> str:
        return self.__str__()
