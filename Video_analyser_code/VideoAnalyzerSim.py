# this module simulates the video analyzer. It uses arrow keys to signal mouse locations.
# the mouse location is the last arrow pressed. Mouse 1's location is simulated by the arrow kyes
# mouse 2's location is simulated by holding down the left shift key and pressing one of the arrow keys.

from pynput.keyboard import Key, Listener

class Video_Analyzer:
    def __init__(self, mouseID):
        self.mouseLocations = [0] * 6     # a list of 6 zeros
        self.mouse = 1
        listener = Listener(on_press = self.on_press, on_release = self.on_release)
        listener.start()  # start to listen on a separate thread

    def on_press(self, key):
        if key == Key.shift:
            self.mouse = 2
        if key == Key.left:
            self.updateLocations([1, 0, 0], self.mouse)
        elif key == Key.right:
            self.updateLocations([0, 0, 1], self.mouse)
        elif key == Key.down:
            self.updateLocations([0, 1, 0], self.mouse)
        elif key == Key.up:
            self.updateLocations([0, 0, 0], self.mouse)

    def on_release(self, key):
        if key == Key.shift:
            self.mouse = 1

    def updateLocations(self, locations, locationOffset):
        if self.mouse == 1:
            self.mouseLocations = locations + self.mouseLocations[3:]
        else:
            self.mouseLocations = self.mouseLocations[:3] + locations

    def process_single_frame(self):
        return self.mouseLocations

