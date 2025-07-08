from vmbpy import *
import time
import cv2
import numpy as np
from queue import Queue
from Video_analyser_code.VideoWriter import VideoWriter
import Data_analysis.FileUtilities as fUtile
import Data_analysis.CodeProfiler as Profiler

import traceback

class Video_Analyzer:
    def __init__(self):
        # Initialize the Vimba SDK and VideoAnalyzer
        self.video_file_loc=fUtile.get_file_path(fUtile.FileType.VIDEO_CAPTURE, 1) + '.avi'
        self.video_writer = VideoWriter(output_file=self.video_file_loc)
        self.regions = self.define_regions()
        self.zone_activation = [0] * len(self.regions)
        self.pixel_sums = {}
        self.frame_queue = Queue(10)  # queue depth is 10, the vimba buffer is 5. no need to monitor queue full
        self.previous_frame_id = None
        self.trial_start_time = 0
        self.trial_end_time = None  # Initialize end time
        #self.exp_zone=0
        cv2.namedWindow('MouseCam', cv2.WINDOW_NORMAL)
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

    def start_video(self):
        self.trial_start_time = time.time()  # Initialize start time
        self.cam.start_streaming(handler = self.frame_handler)

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

    def define_regions(self):
        # Define the regions of interest (ROI) for each mouse and their specific zones
        regions = {
            'm1_c': [(485, 145), (515, 215)],  # Mouse 2 Cooperate Zone (Top Left)
            'm1_cen': [(355, 290), (410, 335)],  # Mouse 2 Center Zone (Center Left)
            'm1_d': [(485, 410), (515, 480)],  # Mouse 2 Defect Zone (Bottom Left)
            'm2_c': [(540, 145), (570, 215)],  # Mouse 1 Cooperate Zone (Top Right)
            'm2_cen': [(635, 290), (690, 335)],  # Mouse 1 Center Zone (Center Right)
            'm2_d': [(540, 410), (570, 480)],  # Adjusted Mouse 1 Defect Zone (Bottom Right)
        }
        return regions

    def find_contours(self, frame):
        # Define the region (x1, y1, x2, y2)
        x1, y1, x2, y2 = 300, 90, 700, 510

        # Crop the frame to the region of interest
        roi_frame = frame[y1:y2, x1:x2]

        # Apply thresholding on the cropped frame
        ret, thresh = cv2.threshold(roi_frame, 25, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the threshold image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Adjust the contour coordinates to be relative to the original frame
        adjusted_contours = [contour + np.array([[x1, y1]]) for contour in contours]

        return adjusted_contours

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
            if contour_counts[region_key] > 0:
                zone_activation[idx] = 1

        # Optional: Print the number of contours detected in each region
        #for region_key, count in contour_counts.items():
            #print(f"{region_key}: Number of contours detected = {count}")

        return zone_activation

    def is_contour_in_region(self, contour, region_rect, region_key):
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

    def draw_rectangle_with_lines(self, frame, top_left, bottom_right, color, thickness):
        # Unpack the top left and bottom right coordinates
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Draw four lines to form a rectangle
        cv2.line(frame, (x1, y1), (x2, y1), color, thickness)  # Top edge
        cv2.line(frame, (x1, y2), (x2, y2), color, thickness)  # Bottom edge
        cv2.line(frame, (x1, y1), (x1, y2), color, thickness)  # Left edge
        cv2.line(frame, (x2, y1), (x2, y2), color, thickness)  # Right edge

    def draw_regions(self, frame, zone_activations):
        for region_key in self.regions:
            top_left, bottom_right = self.regions[region_key]

            # set region color based on its activation status
            index = list(self.regions.keys()).index(region_key)
            color = 0 if zone_activations[index] == 1 else 255  # black if zone activated white if not
            self.draw_rectangle_with_lines(frame, top_left, bottom_right, color,2)

            # Prepare text for region name
            region_name = region_key
            text = f'{region_name}'

            # Calculate position for the text (slightly inside the top-left corner of the rectangle)
            text_pos = (top_left[0] + 5, top_left[1] + 20)

            # Draw the text
            cv2.putText(frame, text,text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        return frame

    def process_single_frame(self):
        # get frame from queue, if available, and process; otherwise, skip.
        if not self.frame_queue.empty():
            frame = self.frame_queue.get(False)
            frameimage = frame.as_opencv_image()

            Profiler.EnterFunction('Find Contours')
            contours = self.find_contours(frameimage)
            Profiler.ExitFunction('Find Contours')

            #if len(contours) > 0:
            #    print("no of contours detected", len(contours))

            #Profiler.EnterFunction('Draw Contours')
            #cv2.drawContours(frameimage, contours, -1, (0, 0, 0), 5)
            #Profiler.ExitFunction('Draw Contours')

            Profiler.EnterFunction('Check Zones')
            self.zone_activations = self.check_zones(frameimage, contours)
            Profiler.ExitFunction('Check Zones')

            #self.exp_zone = self.zone_activations[-1] if self.zone_activations else None

            time_since_trial_start = time.time() - self.trial_start_time

            # Format and display trial information and elapsed time
            frameimage = self.draw_regions(frameimage, self.zone_activations)
            cv2.putText(frameimage, f"Since Start: {self.format_time(time_since_trial_start)}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            Profiler.EnterFunction('Write Frame')
            self.video_writer.write_frame(frameimage)
            Profiler.ExitFunction('Write Frame')

            cv2.imshow('MouseCam', frameimage)
            self.cam.queue_frame(frame)   #return the buffer to the API

        return self.zone_activations

    #def get_zone_activations(self):
        # Return the latest zone activations
        #return self.zone_activations

    def close_resources(self):
        # Close the video writer and any other resources
        self.cam.stop_streaming()
        #self.cam.close()
        self.cam.__exit__(None, None, None)
        self.vimba.__exit__(None, None, None)
        self.video_writer.close()
        cv2.destroyAllWindows()

    def display_features(self):
        for feature in self.cam.get_all_features():
            try:
                value = feature.get()
            except:
                #(AttributeError, VimbaFeatureError)
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


'''
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
'''




'''
from vimba import Vimba, Frame
import cv2
import numpy as np

class Video:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.vimba = Vimba.get_instance()
        self.camera = None
        self.streaming = False

    def __enter__(self):
        self.vimba.__enter__()
        self.camera = self.vimba.get_camera_by_id(self.camera_id)
        self.camera.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.streaming:
            self.camera.stop_streaming()
        self.camera.close()
        self.vimba.__exit__(exc_type, exc_val, exc_tb)

    def start_streaming(self):
        self.camera.start_streaming()
        self.streaming = True

    def get_frame(self):
        if not self.streaming:
            raise RuntimeError("Streaming has not been started. Call start_streaming() first.")
        
        frame = self.camera.get_frame()
        frame_data = frame.as_numpy_ndarray()
        return frame_data

    def stop_streaming(self):
        if self.streaming:
            self.camera.stop_streaming()
            self.streaming = False

    def save_video(self, duration, output_file='output.avi', fps=30):
        width, height = self.camera.get_frame().as_numpy_ndarray().shape[1], self.camera.get_frame().as_numpy_ndarray().shape[0]
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        self.start_streaming()

        num_frames = int(duration * fps)
        try:
            for _ in range(num_frames):
                frame_data = self.get_frame()
                out.write(cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR))  # Convert frame to BGR for OpenCV
        finally:
            self.stop_streaming()
            out.release()

# Example usage:
if __name__ == "__main__":
    with Video(camera_id=0) as video:
        video.save_video(duration=10, output_file='output.avi')
'''