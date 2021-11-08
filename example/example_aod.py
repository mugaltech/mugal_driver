# %%
from mugal_driver import AOM_driver as aod

# %%
import copy
# %%
aod1 = aod.AOD('COM1')
# %%
seg1 = aod.AOD_Segment(freq=80.0E6, set_power=1.2, duration=0.0, onoff=0)
seg2 = aod.AOD_Segment(freq=86.0E6, set_power=1.2, duration=0.04, onoff=0)
seg3 = aod.AOD_Segment(freq=86.0E6, set_power=1.2, duration=0.04, onoff=1)
seg4 = aod.AOD_Segment(freq=86.0E6, set_power=1.0, duration=0.10, onoff=0)
seg5 = aod.AOD_Segment(freq=106.0E6, set_power=0.9, duration=0.04, onoff=0)

aod1.segs1 = [seg1, seg2, seg3, seg4,seg5]
buffer = aod1.send_ch1()
print(','.join(['{:02X}'.format(b) for b in buffer]))
# %%
aod1.segs2 = copy.deepcopy(aod1.segs1)
aod1.segs2[1].freq=82.0E6
buffer = aod1.send_ch2()
print(','.join(['{:02X}'.format(b) for b in buffer]))
# %%
aod1.identifier
# %%
aod1.close()
# %%


