from vimba import *
from vidgear.gears import WriteGear
import time
import cv2
import numpy as np

class Video_Analyzer:
    def __init__(self,vimba_instance):
        self.vimba = vimba_instance
        self.video_file_loc = 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/event_based_conditiong/video/1472/28_09_23_01_down.avi'
        self.regions = self.define_regions()
        self.thresholds = self.define_thresholds()
        self.pixel_sums = {}
        self.frame_counter = 0
        self.trial_start_time = time.time()  # Initialize start time
        self.trial_end_time = None  # Initialize end time

        with Vimba.get_instance() as vimba:

            cams = vimba.get_all_cameras()
            if not cams:
                raise ValueError("No cameras found")
            with cams[0] as cam:
                self.cam = cams[0]
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
                    cam.ExposureTime.set(7000)


    """""
    def define_regions(self):
        # Define the regions of interest (ROI) for the mouse
        regions = {
             'r1': [(500, 310), (535, 380)],#bottom right
            'r2': [(500, 110), (535, 180)],#top right
            'r3': [(455, 310), (490, 380)],#bottom left

            'r4': [(455, 110), (490, 180)],#top left

            'r5': [(590, 220), (660, 280)],#center right
            'r6': [(330, 220), (400, 280)],#center left
        }
        return regions
    """

    def define_regions(self):
        # Define the regions of interest (ROI) for each mouse and their specific zones
        regions = {
            'm1_c': [(500, 110), (535, 180)],  # Mouse 1 Cooperate Zone (Top Right)
            'm1_cen': [(610, 280), (680, 350)],  # Mouse 1 Center Zone (Center Right)
            'm1_d': [(500, 400), (535, 470)],  # Adjusted Mouse 1 Defect Zone (Bottom Right)

            'm2_c': [(455, 110), (490, 180)],  # Mouse 2 Cooperate Zone (Top Left)
            'm2_cen': [(330, 280), (400, 350)],  # Mouse 2 Center Zone (Center Left)
            'm2_d': [(455, 400), (490, 470)],  # Mouse 2 Defect Zone (Bottom Left)
        }
        return regions

    """""
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
        """

    def define_thresholds(self):
        # Define the thresholds for each region
        thresholds = {
            'm1_c': 39500,  # Threshold for Mouse 1 Cooperate Zone
            'm1_cen': 117000,  # Threshold for Mouse 1 Center Zone
            'm1_d': 110000,  # Threshold for Mouse 1 Defect Zone
            'm2_c': 35500,  # Threshold for Mouse 2 Cooperate Zone
            'm2_cen': 300000,  # Threshold for Mouse 2 Center Zone
            'm2_d': 140000,  # Threshold for Mouse 2 Defect Zone
        }
        #{'m1_d': 106569, 'm1_cen': 2632, 'm1_c': 256415, 'm2_d': 112012, 'm2_cen': 505708, 'm2_c': 234711}
        return thresholds

    def check_zones(self, frame):
        zone_activation = [0] * 6  # [0, 0, 0, 0, 0, 0]

        for idx, region_key in enumerate(self.regions):
            (y1, x1), (y2, x2) = self.regions[region_key]
            #print(f"{region_key} coordinates: {(y1, x1)}, {(y2, x2)}")
            region_pixels = frame[y1:y2, x1:x2]
            sum_of_pixels = np.sum(frame[y1:y2, x1:x2])
            self.pixel_sums[region_key] = sum_of_pixels  # Update the class attribute
            #print(f"{region_key}: Sum of pixels = {sum_of_pixels}, Region shape = {region_pixels.shape}")

            if sum_of_pixels <= self.thresholds[region_key]:
                zone_activation[idx] = 1
        #print("zone activation",zone_activation)
        return zone_activation

    def format_time(self,seconds):
        # Helper function to format seconds into H:M:S format
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))

    def draw_regions(self, frame, pixel_sums):
        for region_key in self.regions:
            top_left, bottom_right = self.regions[region_key]

            # Draw the rectangle
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle

            # Prepare text for region name and sum of pixels
            region_name = region_key
            sum_of_pixels = pixel_sums.get(region_key, 0)
            text = f"{region_name}"

            # Calculate position for the text (slightly inside the top-left corner of the rectangle)
            text_pos = (top_left[0] + 5, top_left[1] + 20)

            # Draw the text
            cv2.putText(frame, text,text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

    def process_single_frame(self):
        with self.vimba:
            with self.cam:
                frame = self.cam.get_frame().as_opencv_image()
                # Increment and display the frame number
                self.frame_counter += 1

                # Resize the frame
                frame = cv2.resize(frame, (960, 700))
                self.zone_activations = self.check_zones(frame)

                # Print sum of pixels for each zone

                #for region_key, sum_of_pixels in pixel_sums.items():
                  #  print(f"Zone {region_key} sum: {sum_of_pixels}")
                # Calculate elapsed time since trial start
                time_since_trial_start = time.time() - self.trial_start_time

                # Format and display trial information and elapsed time
                #cv2.putText(frame, f"Trial: {trial_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"Since Start: {self.format_time(time_since_trial_start)}", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                #cv2.putText(frame, f"Frame: {self.frame_counter}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                frame = self.draw_regions(frame, self.pixel_sums)
                #print(self.pixel_sums)
                # Display the frame
                cv2.imshow('Frame', frame)
                cv2.waitKey(1)

                #zone_activations = self.check_zones(frame)

                return self.zone_activations

    def get_zone_activations(self):
        # Return the latest zone activations
        return self.zone_activations


#analyzer = VideoAnalyzer()
#analyzer.stream_and_process()