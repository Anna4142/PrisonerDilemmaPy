from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM
if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as Arduino
else:
    import Arduino_related_code.ArduinoDigital as Arduino

from Arduino_related_code.ValveControl import ValveControl

class RewardManager:
    def __init__(self, comport, valves, m1_rewards, m2_rewards):
        Arduino.openComPort(comport)
        self.rewards = [{k: int(v) for k, v in m1_rewards.items()},
                        {k: int(v) for k, v in m2_rewards.items()}]
        self.valve_key = [{'CC': 'M1 Coo',
                           'CD': 'M1 Coo',
                           'DC': 'M1 Def',
                           'DD': 'M1 Def',
                           'CN': 'M1 Cen'},
                          {'CC': 'M2 Coo',
                           'CD': 'M2 Def',
                           'DC': 'M2 Coo',
                           'DD': 'M2 Def',
                           'CN': 'M2 Cen'}]
        self.valves = {}
        for key in valves:
            self.valves[key] = {'valve Obj': ValveControl(int(valves.get(key).get('Channel'))),
                                'flow unit': float(valves.get(key).get('flow unit'))}

    def deliver_reward(self, mouse_id, scenario):
        key = self.valve_key[mouse_id - 1].get(scenario)
        valve = self.valves.get(key).get('valve Obj')
        open_time = self.valves.get(key).get('flow unit') * self.rewards[mouse_id - 1].get(scenario)

        valve.OpenValve(open_time / 1000)  # time is converted to seconds

    def is_reward_delivered(self):
        rewarDelivered = True
        for key in self.valves:
            valve = self.valves.get(key).get('valve Obj')
            if valve.IsValveOpen():
                rewarDelivered = False
        return rewarDelivered

    def get_reward(self, mouse_id, scenario):
        return self.rewards[mouse_id -1].get(scenario)