# %%
from mugal_driver import low_noise_reference as lnr
from  functools import reduce
# %%
lnr1 = lnr.LNR('COM1')

seg1 = lnr.LNR_Segment(mode=0,freq_start=80E6,duration=0.0)
seg2 = lnr.LNR_Segment(mode=1,freq_start=80E6,df=1.0E4,dt=1E-3,duration=2E-3)
seg3 = lnr.LNR_Segment(mode=0,freq_start=100E6,duration=2E-3)
seg4 = lnr.LNR_Segment(mode=1,freq_start=100E6,df=-2E4,dt=1E-3,duration=2E-3)
seg5 = lnr.LNR_Segment(mode=0,freq_start=60E6,duration=2E-3)
seg6 = lnr.LNR_Segment(mode=1,freq_start=60E6,df=1E4,dt=1E-3,duration=2E-3)
seg7 = lnr.LNR_Segment(mode=0,freq_start=80E6,duration=2E-3)

lnr1.segs=[seg1, seg2, seg3, seg4, seg5, seg6, seg7]

# %%
print(lnr1)

print(lnr1.segs)
# %%
buffer = lnr1.send()
print(','.join(['{:02X}'.format(b) for b in buffer]))

# %%
lnr1.close()
