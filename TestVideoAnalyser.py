import cv2
from VideoAnalyzer1 import Video_Analyzer  # Replace 'your_module' with the actual name of your module

def test_video_analyzer_with_camera():
    # Create an instance of the Video_Analyzer class
    analyzer = Video_Analyzer()

    try:
        # Start the stream and process method
        analyzer.stream_and_process()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Release resources, if any (e.g., camera)
        # Depending on how your class handles the camera, you might need to release it here
        pass

# Run the test function
test_video_analyzer_with_camera()
