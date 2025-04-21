from vmbpy import *
from queue import Queue


class VimbaDriver:
    def __init__(self):
        self.vimba = VmbSystem.get_instance()
        self.vimba.__enter__()

        cams = self.vimba.get_all_cameras()
        if not cams:
            raise ValueError("No cameras found")
        self.cam = cams[0]
        self.cam.__enter__()
        #self.display_features()  # for debug only
        self.cam.Height.set(608)  #1216)
        self.cam.Width.set(968) #1936)
        self.cam.BinningHorizontal.set(2)
        self.cam.BinningVertical.set(2)
        self.cam.AcquisitionFrameRateEnable.set("True")
        self.cam.AcquisitionFrameRate.set(50)
        current_frame_rate = self.cam.AcquisitionFrameRate.get()
        print(f"Camera Frame Rate: {current_frame_rate} FPS")
        formats = self.cam.get_pixel_formats()
        opencv_formats = intersect_pixel_formats(formats, OPENCV_PIXEL_FORMATS)
        self.cam.set_pixel_format(opencv_formats[0])
        self.cam.AcquisitionMode.set('Continuous')
        self.cam.Gain.set(15)
        self.cam.ExposureTime.set(3000)
        self.frame_queue = Queue(10)  # queue depth is 10, the vimba buffer is 5. no need to monitor queue full
        self.previous_frame_id = None

    def start_video(self):
        self.cam.start_streaming(handler = self.frame_handler)

    def get_frame(self):
        frame = None
        if not self.frame_queue.empty():
            frame = self.frame_queue.get(False)
        return frame

    def release_frame(self, frame):
        self.cam.queue_frame(frame)  # return the buffer to the API

    def frame_handler(self, cam: Camera, stream: Stream, frame: Frame):
        #print ('frame handler')
        self.frame_queue.put(frame)
        #if self.frame_queue.empty():
        #    print ('Frame was not added to queue')
        if self.previous_frame_id is not None:
            dropped_frames = frame.get_id() - self.previous_frame_id - 1
        else:
            dropped_frames = 0
        self.previous_frame_id = frame.get_id()
        if dropped_frames != 0:
            print (f' {dropped_frames} frames dropped' )
        #print ('frame handler completed')

    def close_resources(self):
        # Close the video writer and any other resources
        self.cam.stop_streaming()
        # self.cam.close()
        self.cam.__exit__(None, None, None)
        self.vimba.__exit__(None, None, None)

    def display_features(self):
        for feature in self.cam.get_all_features():
            try:
                value = feature.get()
            except:
                # (AttributeError, VimbaFeatureError)
                value = None

            print(f"Feature name: {feature.get_name()}")
            print(f"Display name: {feature.get_display_name()}")
            if not value is None:
                if not feature.get_unit() == '':
                    print(f"Unit: {feature.get_unit()}", end=' ')
                    print(f"value={value}")
                else:
                    print(f"Not set")
                    print("--------------------------------------------")
