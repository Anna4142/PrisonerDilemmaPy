from ValveControl import ValveControl
import threading

class RewardManager:
    def __init__(self, arduino_instance, valve_channels):
        self.valve_channels = valve_channels
        self.valves = [ValveControl(channel, arduino_instance) for channel in valve_channels]

    def _valve_number_to_index(self, valve_number):
        if valve_number in self.valve_channels:
            return self.valve_channels.index(valve_number)
        else:
            return None


    def _threaded_deliver(self, valve_index, duration):

        if valve_index is not None and valve_index < len(self.valves):
            valve = self.valves[valve_index]
            valve.OpenValve(duration)
            while valve.IsValveOpen():
                pass    # Micky. I added it just to have a working code.should be removed.
              # print("valve open")                    # Micky: This is a tight loop waiting on the valve the close. it prints this message continiously
                                                     #        its pointless to run it in a sparate thred. It will just seat here and wait
                                                     #        for the valve to close. Its better to call it from the main loop of the experiment
                                                     #        manager. I'll show you how next round.

                # Wait a bit before checking again to avoid overloading the CPU
        else:
            print(f"Valve index {valve_index} is out of range.")


    def _get_valve_index(self, scenario, mouse_id):
        mapping = {
            'cc': {1: 12, 2: 7},
            'cd': {1: 12, 2: 9},
            'dc': {1: 10, 2: 7},
            'dd': {1: 10, 2: 11},
            'center': {1: 11, 2: 8},
        }
        valve_number = mapping.get(scenario, {}).get(mouse_id)
        return self._valve_number_to_index(valve_number)

    def deliver_reward(self, scenario, mouse_id, reward_time):
        valve_index = self._get_valve_index(scenario, mouse_id)
        if valve_index is not None:
            thread = threading.Thread(target=self._threaded_deliver, args=(valve_index, reward_time))
            thread.start()                         # Micky: You are not using the threads correctly. The Start() function
                                                   #        will return after the valve is closed.
            thread.join()                          # Micky: I think the join() fucntion is not doing anything.


# Example usage:
# arduino_instance = Arduino()  # This should be your actual Arduino instance
# valve_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Example channel numbers for your valves
# reward_manager = RewardManager(arduino_instance, valve_channels)

# To deliver a reward, call:
# reward_manager.deliver_reward('cc', 1, 5)  # 'cc' scenario, mouse_id 1, for 5 seconds

