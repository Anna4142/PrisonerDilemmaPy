import winsound
from enum import Enum

class Sounds (Enum):
    Start               = 1
    Abort               = 2

def Play(sound):
    if sound == Sounds.Start:
        winsound.PlaySound("C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/sounds/beep.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif sound == Sounds.Abort:
        winsound.PlaySound("C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/sounds/annoying_noise.wav", winsound.SND_FILENAME |winsound.SND_ASYNC)
