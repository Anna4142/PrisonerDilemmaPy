from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM

if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as Arduino
else:
    import Arduino_related_code.ArduinoDigital as Arduino

from Arduino_related_code.ValveControl import ValveControl

class RewardManager:
    def __init__(self, comport, channels, rewards):
        Arduino.openComPort(comport)
        self.rewards = rewards
        self.recipient_key = [{'CC': 'Coo',
                               'CD': 'Coo',
                               'DC': 'Def',
                               'DD': 'Def',
                               'CN': 'Cen'},
                              {'CC': 'Coo',
                               'CD': 'Def',
                               'DC': 'Coo',
                               'DD': 'Def',
                               'CN': 'Cen'}]
        self.recipients = [{} for _ in range(len(channels))]
        for i in range(len(channels)):
            for key in channels[i]:
                self.recipients[i][key] = ValveControl(int(channels[i][key]))

    def deliver_reward(self, mouse_id, scenario):
        key = self.recipient_key[mouse_id - 1][scenario]
        valve = self.recipients[mouse_id - 1][key]
        open_time = int(self.rewards[mouse_id - 1][scenario]['opening time'])

        valve.OpenValve(open_time / 1000)  # time is converted to seconds

    def is_reward_delivered(self):
        reward_delivered = True
        for i in range(len(self.recipients)):
            for key in self.recipients[i]:
                if self.recipients[i][key].IsValveOpen():
                    reward_delivered = False
        return reward_delivered

    def get_reward(self, mouse_id, scenario):
        return self.rewards[mouse_id -1][scenario]['water volume']
