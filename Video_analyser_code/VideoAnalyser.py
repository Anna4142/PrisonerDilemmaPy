from vimba import *
import time
import cv2
import numpy as np
import tkinter as tk
from Video_analyser_code.VideoWriter import VideoWriter
import pandas as pd


class Video_Analyzer:
    def __init__(self,filename,opponenttype):
        self.root = tk.Tk()

        # Initialize the Vimba SDK and VideoAnalyzer
        with Vimba.get_instance() as vimba:

            self.vimba = vimba



        # Formatting the date and time
        current_datetime = pd.Timestamp.now()
        datetime_string = current_datetime.strftime("%Y%m%d_%H%M%S")
        # Format the file path to include the filename and the date string
        if opponenttype=="MOUSE_COMPUTER" :
         self.video_file_loc = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/{filename}/video_captures/{datetime_string}.avi'
        else:
         self.video_file_loc = f'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/PILOT_RESULTS/{opponenttype}/video_captures/{datetime_string}.avi'

        self.video_writer = VideoWriter(output_file=self.video_file_loc)
        self.regions = self.define_regions()
        self.thresholds = self.define_thresholds()
        self.pixel_sums = {}
        self.frame_counter = 0
        self.trial_start_time = time.time()  # Initialize start time
        self.trial_end_time = None  # Initialize end time
        self.exp_zone=0


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
            'm1_c': [(475, 110), (510, 240)],  # Mouse 2 Cooperate Zone (Top Left)
            'm1_cen': [(330, 260), (400, 330)],  # Mouse 2 Center Zone (Center Left)
            'm1_d': [(455, 370), (490, 480)],  # Mouse 2 Defect Zone (Bottom Left)
            'm2_c': [(525, 110), (565, 235)],  # Mouse 1 Cooperate Zone (Top Right)
            'm2_cen': [(610, 260), (680, 330)],  # Mouse 1 Center Zone (Center Right)
            'm2_d': [(515, 370), (550, 480)],  # Adjusted Mouse 1 Defect Zone (Bottom Right)

        }
        return regions


    def define_thresholds(self):
        # Define the thresholds for each region
        self.thresholds = {
            'm1_c': 39800,  # Threshold for Mouse 2 Cooperate Zone
            'm1_cen': 300000,  # Threshold for Mouse 2 Center Zone
            'm1_d': 130000,  # Threshold for Mouse 2 Defect Zone
            'm2_c': 39500,  # Threshold for Mouse 1 Cooperate Zone
            'm2_cen': 117000,  # Threshold for Mouse 1 Center Zone
            'm2_d': 98941,  # Threshold for Mouse 1 Defect Zone


        }

        return self.thresholds

    def find_contours(self, frame):
        # Define the region (x1, y1, x2, y2)
        x1, y1, x2, y2 = 300, 90, 700, 510

        # Crop the frame to the region of interest
        roi_frame = frame[y1:y2, x1:x2]

        # Apply thresholding on the cropped frame
        ret, thresh = cv2.threshold(roi_frame, 25, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the thresholded image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Adjust the contour coordinates to be relative to the original frame
        adjusted_contours = [contour + np.array([[x1, y1]]) for contour in contours]

        return adjusted_contours

    """""
    def check_zones(self, frame):  #####    THRESHOLD BASED APPROACH
        zone_activation = [0] * 6 # [0, 0, 0, 0, 0, 0]

        for idx, region_key in enumerate(self.regions):
            (y1, x1), (y2, x2) = self.regions[region_key]
            #print(f"{region_key} coordinates: {(y1, x1)}, {(y2, x2)}")
            region_pixels = frame[y1:y2, x1:x2]
            sum_of_pixels = np.sum(frame[y1:y2, x1:x2])
            self.pixel_sums[region_key] = sum_of_pixels  # Update the class attribute
            print(f"{region_key}: Sum of pixels = {sum_of_pixels}, Region shape = {region_pixels.shape}")

            if sum_of_pixels <= self.thresholds[region_key]:

                zone_activation[idx] = 1
        #print("zone activation",zone_activation)
        return zone_activation
    """""

    def check_zones(self, frame, mouse_contours):
        zone_activation = [0] * len(self.regions)
        contour_counts = {region_key: 0 for region_key in self.regions}  # Initialize contour counts

        for idx, region_key in enumerate(self.regions):
            (y1, x1), (y2, x2) = self.regions[region_key]
            region_rect = (x1, y1, x2, y2)

            for contour in mouse_contours:
                if self.is_contour_in_region(contour, region_rect, region_key):
                    contour_counts[region_key] += 1  # Increment count for this region

            # Activate zone only if more than 4 contours are detected in the region
            if contour_counts[region_key] > 5:
                zone_activation[idx] = 1

        # Optional: Print the number of contours detected in each region
        #for region_key, count in contour_counts.items():
            #print(f"{region_key}: Number of contours detected = {count}")

        return zone_activation

    def is_contour_in_region(self, contour, region_rect,region_key):
        #x1, y1, w1, h1 = region_rect
        #x2, y2 = x1 + w1, y1 + h1  # Calculate bottom-right corner of the region
        y1,x1, y2, x2 = region_rect
        val=False
        for point in contour:
            x, y = point[0]  # Get the (x, y) coordinates of the contour point
            #print("contour points",point[0])
            if x1 <= x <= x2 and y1 <= y <= y2:
                # Debugging print statement
                #print(f"Contour Point: {(x, y)}, Region Rect: {region_rect}, Inside: True ,Region key: {region_key}")
                val= True
                break
            else:
                # Debugging print statement
                #print(f"Contour Point: {(x, y)}, Region Rect: {region_rect}, Inside: False ,Region key: {region_key}")
                val=False
        return val





    def format_time(self,seconds):
        # Helper function to format seconds into H:M:S format
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))

    def draw_rectangle_with_lines(self,frame, top_left, bottom_right, color, thickness):
        # Unpack the top left and bottom right coordinates
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Draw four lines to form a rectangle
        cv2.line(frame, (x1, y1), (x2, y1), color, thickness)  # Top edge
        cv2.line(frame, (x1, y2), (x2, y2), color, thickness)  # Bottom edge
        cv2.line(frame, (x1, y1), (x1, y2), color, thickness)  # Left edge
        cv2.line(frame, (x2, y1), (x2, y2), color, thickness)  # Right edge

    def draw_regions(self, frame, pixel_sums):
        for region_key in self.regions:
            top_left, bottom_right = self.regions[region_key]

            self.draw_rectangle_with_lines(frame, top_left, bottom_right, (255, 255, 255),2)

            # Prepare text for region name and sum of pixels
            region_name = region_key
            sum_of_pixels = pixel_sums.get(region_key, 0)
            text = f"{region_name}"

            # Calculate position for the text (slightly inside the top-left corner of the rectangle)
            text_pos = (top_left[0] + 5, top_left[1] + 20)

            # Draw the text
            cv2.putText(frame, text,text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

    def process_single_frame(self, timestamps):
        with self.vimba:
            with self.cam:
                frame = self.cam.get_frame().as_opencv_image()

                self.video_writer.write_frame(frame, timestamps)
                # Increment and display the frame number
                self.frame_counter += 1

                # Resize the frame
                frame = cv2.resize(frame, (960, 700))
                frame = self.draw_regions(frame, self.pixel_sums)
                #self.zone_activations = self.check_zones(frame)  ##FOR THRESHOLD BASED APPROACH
                contours = self.find_contours(frame)
                #print("no of contours detected", len(contours))
                cv2.drawContours(frame, contours, -1, (0, 0, 0), 5)
                self.zone_activations = self.check_zones(frame,contours)
                self.exp_zone = self.zone_activations[-1] if self.zone_activations else None


                time_since_trial_start = time.time() - self.trial_start_time

                # Format and display trial information and elapsed time
                #cv2.putText(frame, f"Trial: {trial_number}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"Since Start: {self.format_time(time_since_trial_start)}", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                #cv2.putText(frame, f"Frame: {self.frame_counter}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                #print(self.pixel_sums)


                cv2.imshow('Frame', frame)
                cv2.waitKey(1)

                #zone_activations = self.check_zones(frame)

                return self.zone_activations

    def get_zone_activations(self):
        # Return the latest zone activations
        return self.zone_activations
    def close_resources(self):
        # Close the video writer and any other resources
        self.video_writer.close()
