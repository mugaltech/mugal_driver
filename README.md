# mugal_driver
Device drivers for MugalTech products.

[![build add publish to PyPI](https://github.com/mugaltech/mugal_driver/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/mugaltech/mugal_driver/actions/workflows/publish-to-pypi.yml)


Including:

1. LNR signal generator
2. ...

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
