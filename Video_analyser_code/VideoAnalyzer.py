from vimba import *
from vidgear.gears import WriteGear
import time
import cv2
import numpy as np

class Video_Analyzer:
    def __init__(self):
        self.video_file_loc = 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/event_based_conditiong/video/1472/28_09_23_01_down.avi'
        self.regions = self.define_regions()
        self.thresholds = self.define_thresholds()

    """""
    def define_regions(self):
        # Define the regions of interest (ROI) for the mouse
        regions = {
             'r1': [(500, 310), (535, 380)],#bottom right
            'r2': [(500, 110), (535, 180)],#top right
            'r3': [(455, 310), (490, 380)],#bottom left

            'r4': [(455, 110), (490, 180)],#top left

            'r5': [(610, 220), (680, 290)],#center right
            'r6': [(330, 220), (400, 280)],#center left
        }
        return regions
    """
    def define_regions(self):
        # Define the regions of interest (ROI) for each mouse and their specific zones
        regions = {
            'mouse1_cooperate': [(500, 310), (535, 380)],  # Mouse 1 Cooperate Zone
            'mouse1_center': [(500, 110), (535, 180)],  # Mouse 1 Center Zone
            'mouse1_defect': [(455, 310), (490, 380)],  # Mouse 1 Defect Zone
            'mouse2_cooperate': [(455, 110), (490, 180)],  # Mouse 2 Cooperate Zone
            'mouse2_center': [(590, 220), (660, 280)],  # Mouse 2 Center Zone
            'mouse2_defect': [(330, 220), (400, 280)],  # Mouse 2 Defect Zone
        }
        return regions


    def draw_regions(self, frame):
        for region_key in self.regions:
            top_left, bottom_right = self.regions[region_key]
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle
        return frame
    def define_thresholds(self):
        # Define the thresholds for each region
        thresholds = {
            'r1': 90000,
            'r2': 90000,
            'r3': 90000,
            'r4': 90000,
            'r5': 90000,
            'r6': 90000,
        }
        return thresholds

    def check_zones(self, frame):
        zone_activation = [0] * 6  # [0, 0, 0, 0, 0, 0]
        pixel_sums = {}

        for idx, region_key in enumerate(self.regions):
            (y1, x1), (y2, x2) = self.regions[region_key]
            sum_of_pixels = np.sum(frame[y1:y2, x1:x2])
            pixel_sums[region_key] = sum_of_pixels

            if sum_of_pixels <= self.thresholds[region_key]:
                zone_activation[idx] = 1

        return zone_activation, pixel_sums

    def format_time(self,seconds):
        # Helper function to format seconds into H:M:S format
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))
    def process_single_frame(self):
        # Capture a single frame from the camera and convert it to an OpenCV image
        frame = self.camera.get_frame().as_opencv_image()

        # Process the frame to determine zone activations
        # This typically involves analyzing the frame to check if certain regions of interest
        # meet specific conditions (like movement, color changes, etc.)
        zone_activations = self.check_zones(frame)

        # Return the processed frame and the zone activations
        # frame: The latest frame captured from the camera
        # zone_activations: A list or dictionary containing the activation status of each zone
        return frame, zone_activations
    def stream_and_process(self):
        with Vimba.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            with cams[0] as cam:
                for feature in cam.get_all_features():
                    try:
                        value = feature.get()
                    except:
                        (AttributeError, VimbaFeatureError)
                        value = None
                    cam.Height.set(1216)
                    cam.Width.set(1936)
                    cam.BinningHorizontal = 4
                    cam.BinningVertical = 4
                    cam.AcquisitionFrameRateEnable.set("True")

                    formats = cam.get_pixel_formats()
                    print(f"Feature name: {feature.get_name()}")
                    print(f"Display name: {feature.get_display_name()}")
                    if not value == None:
                        if not feature.get_unit() == '':
                            print(f"Unit: {feature.get_unit()}", end=' ')
                            print(f"value={value}")
                        else:
                            print(f"Not set")
                            print("--------------------------------------------")
                    opencv_formats = intersect_pixel_formats(formats, OPENCV_PIXEL_FORMATS)
                    cam.set_pixel_format(opencv_formats[0])
                    cam.AcquisitionMode = 'Continuous'
                    cam.ExposureTime.set(10000)
                trial_number = 1  # Start with the first trial
                trial_start_time = time.time()  # Start time of the current trial
                trial_end_time = None
                while True:
                    frame = cam.get_frame().as_opencv_image()
                    frame = cv2.resize(frame, (960, 540))
                    self.zone_activations, pixel_sums = self.check_zones(frame)

                    # Print sum of pixels for each zone
                    for region_key, sum_of_pixels in pixel_sums.items():
                        print(f"Zone {region_key} sum: {sum_of_pixels}")
                    # Calculate elapsed times
                    time_since_trial_start = time.time() - trial_start_time
                    time_since_trial_end = time.time() - trial_end_time if trial_end_time else 0

                    # Format and display trial information and elapsed times
                    trial_info_text = f"Trial: {trial_number}"
                    start_time_text = f"Since Start: {self.format_time(time_since_trial_start)}"
                    end_time_text = f"Since End: {self.format_time(time_since_trial_end)}" if trial_end_time else ""

                    cv2.putText(frame, trial_info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(frame, start_time_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    if trial_end_time:
                        cv2.putText(frame, end_time_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    frame= self.draw_regions(frame)
                    cv2.imshow('Frame', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):

                       cam.stop_streaming()

    def get_zone_activations(self):
        # Return the latest zone activations
        return self.zone_activations

#analyzer = VideoAnalyzer()
#analyzer.stream_and_process()