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

    def write_frame(self, frame, timestamps):
        if frame is not None:
            # Draw each timestamp on the frame
            y_offset = 20  # Vertical offset for each line of text
            for idx, (key, value) in enumerate(timestamps.items()):
                if value is not None:
                    timestamp_text = f"{key}: {value}"
                    cv2.putText(frame, timestamp_text, (10, y_offset + idx * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 255), 2)

            # Write frame to video
            self.writer.write(frame)

    def close(self):
        self.writer.close()
