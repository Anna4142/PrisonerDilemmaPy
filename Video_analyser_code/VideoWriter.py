from vidgear.gears import WriteGear
import cv2

class VideoWriter:
    def __init__(self, output_file, frame_size=(960, 700), fps=30.0):
        self.output_file = output_file
        self.frame_size = frame_size
        self.fps = fps
        self.init_writer()

    def init_writer(self):

        self.writer = WriteGear(output=self.output_file)

    def write_frame(self, frame):
        if frame is not None:
            # Resize frame

            self.writer.write(frame)

    def close(self):
        self.writer.close()
