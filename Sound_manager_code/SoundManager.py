# Micky: I changed the file name, just to maintain consistency. Some naming conventions is good. It helps read the code. The occasional
#         use of '_" catches my attention and always think "why". What is special about this name compared to all the others?
#         what does this suppose to indicate?
# Micky: I also recommend using relative (e.g. starting from the python working directory, go one up and then to the Sounds/ ) file names
#         rather then absolute. This way you can move the project from one comuter to another. copy Ben's sound files to your project library
# Micky:  Also do not configure the sound files from the experiment manager. It defeats the purpose of having a class. Hide the details here.
# Micky;  I switched to the winsound module, becuase its simple and pure python. pygame is a lot havier and requires Visual C to be installed.
#         Any reason you chose pygame package? One caveat, windound requires wav files. Is it ok?
# Micky:  Also, please note that I wrote it as a module rather than a class. When you need one instance of a class and it does not require
#         any "self" variables, this is the preferred (I think) python solution. In C++ you would have used static classes.

import winsound
from enum import Enum

class Sounds (Enum):
    Start               = 1
    Abort               = 2

def Play(sound):
    if sound == Sounds.Start:
        winsound.PlaySound("C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/sounds/beep.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif sound == Sounds.Abort:
        winsound.PlaySound("C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/sounds/ping.wav", winsound.SND_FILENAME |winsound.SND_ASYNC)