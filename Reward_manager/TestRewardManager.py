
from Arduino_related_code.ArduinoDigital import ArduinoDigital
import time
from Reward_manager.RewardManager import RewardManager
def test_reward_manager():
    # Assuming you have an Arduino instance ready
    arduino_instance = ArduinoDigital("COM11")  # Replace with your actual ArduinoDigital instance
    valve_channels = [7, 8, 9, 10, 11, 12]  # Example channel numbers for your valves
    reward_manager = RewardManager(arduino_instance, valve_channels)

    # Test different scenarios
    scenarios = ['cc', 'cd', 'dc', 'dd', 'center']
    for scenario in scenarios:
        for mouse_id in [1, 2]:
            print(f"Testing scenario: {scenario}, mouse ID: {mouse_id}")
            reward_manager.deliver_reward(scenario, mouse_id, 1)  # Test for 5 seconds
            time.sleep(6)  # Wait for the valve operation to complete plus a buffer

    print("Testing completed.")

# Call the test function
test_reward_manager()
