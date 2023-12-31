import os
import time
from SoundManager import *

print(os.getcwd())
Play(Sounds.Abort)
time.sleep(2)
Play(Sounds.Start)
time.sleep(5)
Play(Sounds.Abort)
time.sleep(2)