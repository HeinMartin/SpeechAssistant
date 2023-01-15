"""
Get and set access to master volume example.
"""
from __future__ import print_function

from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import numpy as np

def main():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    print("volume.GetMute(): %s" % volume.GetMute())
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())
    print("volume.GetVolumeRange(): (%s, %s, %s)" % volume.GetVolumeRange())
    print("volume.SetMasterVolumeLevel()")
    volume.SetMasterVolumeLevel(-20.0, None)
    print("volume.GetMasterVolumeLevel(): %s" % volume.GetMasterVolumeLevel())

def from_dB(dB):
    return 10**(1/dB)
def to_dB(x):
    return 5*np.log10(x)

if __name__ == "__main__":
    
    p = 80

    print(to_dB(p))
    print(from_dB(p))
