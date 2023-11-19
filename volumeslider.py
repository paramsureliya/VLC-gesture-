from tkinter import *
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import ttk

import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def set_vol(vol):
    # pycaw
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    volumeRange = volume.GetVolumeRange()
    minVol = volumeRange[0]
    maxVol = volumeRange[1]
    print(vol)
    vol_value = np.interp(vol, [0, 100], [minVol, maxVol])
    volume.SetMasterVolumeLevel(vol_value, None)
    print(vol_value)


def main(vol):
    parent.title("Volume")
    parent.geometry('1350x20')
    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='green')
    bar = Progressbar(parent, length=1350, style='black.Horizontal.TProgressbar')
    bar['value'] = vol
    bar.grid(column=0, row=0)
    set_vol(vol)


if __name__ == "__main__":
    a = input()
    parent = tk.Tk()
    main(a)
    parent.mainloop()
