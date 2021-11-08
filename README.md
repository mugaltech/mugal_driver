# mugal_driver
Device drivers for MugalTech products.

[![build add publish to PyPI](https://github.com/mugaltech/mugal_driver/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/mugaltech/mugal_driver/actions/workflows/publish-to-pypi.yml)


Including:

1. LNR: Low noise reference signal generator
2. AOD: Acousto-Optic Modulator driver
3. ...

## How to install
Install from [PYPI](https://pypi.org/project/mugal-driver/)
```shell
pip install mugal-driver
```

Install from source 

1. Git clone or download source code
2. install using pip from source:

```shell
pip install -e <source path>
```

## Low noise reference signal generator

A low noise reference signal generator can operate in segments of mode, each with a duration of about 655ms. Each segment can be a single point mode or frequency sweep mode. 

* mode : 0 for single frequency, 1 for frequency sweep
* duration: min 10us, max 655.35ms with step 10us
* freq_start, df : 0-120MHz, with step about 1E-6Hz
* dt 3.33ns to about 14.3s

### How to use low_noise_reference module

import LNR module
```python
from mugal_driver import low_noise_reference as lnr
```
create LNR object and a few segments
```python
lnr1 = lnr.LNR('COM1')
seg1 = lnr.LNR_Segment(mode=0,freq_start=80E6,duration=0.0)
seg2 = lnr.LNR_Segment(mode=1,freq_start=80E6,df=1.0E4,dt=1E-3,duration=2E-3)
lnr1.segs = [seg1, seg2]
```
send command
```python
lnr1.send()
```
close device after use
```python
lnr1.close()
```

## Acousto-Optic Modulator driver

Dual channal Acousto-Optic Modulator driver. frequency 50MHz-200MHz
Each channel operate in segments of frequencies, output RF power or OnOff state. Use segs1 for CH1, segs2 for CH2.

> &#9888; **warning: onoff==0 stand for ON**

``` python
from mugal_driver import AOM_driver as aod
import copy

aod1 = aod.AOD('COM1')
print(aod1.identifier)

seg1 = aod.AOD_Segment(freq=80.0E6, set_power=1.2, duration=0.0, onoff=0)
seg2 = aod.AOD_Segment(freq=86.0E6, set_power=1.2, duration=0.04, onoff=0)
seg3 = aod.AOD_Segment(freq=86.0E6, set_power=1.2, duration=0.04, onoff=1)
seg4 = aod.AOD_Segment(freq=86.0E6, set_power=1.0, duration=0.10, onoff=0)
seg5 = aod.AOD_Segment(freq=106.0E6, set_power=0.9, duration=0.04, onoff=0)

aod1.segs1 = [seg1, seg2, seg3, seg4,seg5]
buffer = aod1.send_ch1()
print(','.join(['{:02X}'.format(b) for b in buffer]))

aod1.segs2 = copy.deepcopy(aod1.segs1)
aod1.segs2[1].freq=82.0E6
buffer = aod1.send_ch2()
print(','.join(['{:02X}'.format(b) for b in buffer]))

aod1.close()
```

