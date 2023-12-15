# Micky: Can we, please, get tid of the 1 in the file name?
from enum import Enum         # Micky: looks like this import is not needed.
from locations import Locations

class MouseMonitor:
    def __init__(self, video,mouse_id):
        self.mouse_id = mouse_id
        self.video_analyser=video

    def get_mouse_location(self, zones_list):
        # Split the zones based on mouse_id
        #print("ZONES LIST",zones_list)                          # Micky: These prints are flooding the consol wondow. not recomanded.
        mouse_zones = zones_list[(self.mouse_id - 1) * 3 : self.mouse_id * 3]
        #print(self.mouse_id)
        #print(mouse_zones)
        # Interpret the zones list to return the corresponding location
        location = Locations.Unknown
        if mouse_zones[0] == 1:
            location = Locations.Cooperate
        elif mouse_zones[1] == 1:
            location = Locations.Center
        elif mouse_zones[2] == 1:
            location = Locations.Defect
        #print("location",location)
        return location





