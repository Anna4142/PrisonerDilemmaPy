from Experiment_Launcher_code.ModuleConfiguration import __USE_ARDUINO_SIM

if __USE_ARDUINO_SIM:
    import Arduino_related_code.ArduinoDigitalSim as Arduino
else:
    import Arduino_related_code.ArduinoDigital as Arduino

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import Data_analysis.FileUtilities as fUtile

from Arduino_related_code.ValveControl import ValveControl

class MouseReward:
    def __init__(self):
        self.opening_time = tk.StringVar(value=None)
        self.water_volume = tk.StringVar(value=None)

class HWConfGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma, HW Configuration screen")
        self.window.geometry("555x581")

        # create window layout
        self.system_panel = tk.Frame(self.window, width=545, height=90, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.system_panel, text="System Parameters").place(x=210, y=2)
        self.M1Panel = tk.Frame(self.window, width=270, height=335, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M1Panel, text='Mouse 1', font=("Arial", 8)).place(x=30, y=2)
        self.M1ValvesPanel = tk.Frame(self.M1Panel, width=257, height=85, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M1ValvesPanel, text='Valves', font=("Arial", 8)).place(x=100, y=2)
        self.M1RewardsPanel = tk.Frame(self.M1Panel, width=257, height=210, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M1RewardsPanel, text='Rewards', font=("Arial", 8)).place(x=100, y=2)
        self.M2Panel = tk.Frame(self.window, width=270, height=335, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M2Panel, text='Mouse 2', font=("Arial", 8)).place(x=30, y=2)
        self.M2ValvesPanel = tk.Frame(self.M2Panel, width=257, height=85, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M2ValvesPanel, text='Valves', font=("Arial", 8)).place(x=100, y=2)
        self.M2RewardsPanel = tk.Frame(self.M2Panel, width=257, height=210, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M2RewardsPanel, text='Valves', font=("Arial", 8)).place(x=100, y=2)
        self.CalibrationPanel = tk.Frame(self.window, width=327, height=100, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.CalibrationPanel, text='Valve Calibration', font=("Arial", 8)).place(x=130, y=2)
        self.ScanningPanel = tk.Frame(self.window, width=213, height=100, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.ScanningPanel, text='Valve Scanning', font=("Arial", 8)).place(x=80, y=2)

        self.system_panel.place(x=5, y=5)
        self.M1Panel.place(x=5, y=100)
        self.M1ValvesPanel.place(x=5, y=25)
        self.M1RewardsPanel.place(x=5, y=115)
        self.M2Panel.place(x=280, y=100)
        self.M2ValvesPanel.place(x=5, y=25)
        self.M2RewardsPanel.place(x=5, y=115)
        self.CalibrationPanel.place(x=5, y=440)
        self.ScanningPanel.place(x=337, y=440)

        self.calibrate_button = tk.Button(self.window, text="Calibrate")
        self.calibrate_button.place(x=125, y=545)
        self.calibrate_button.config(font=("Arial", 12), state='disabled', command=self.calibrate_callback)

        self.abort_button = tk.Button(self.window, text="Abort")
        self.abort_button.place(x=324, y=545)
        self.abort_button.config(font=("Arial", 12), state='disabled', command=self.abort_callback)

        self.scan_button = tk.Button(self.window, text="Scan")
        self.scan_button.place(x=237, y=545)
        self.scan_button.config(font=("Arial", 12), state='disabled', command=self.scan_callback)

        self.save_button = tk.Button(self.window, text="Save")
        self.save_button.place(x=410, y=545)
        self.save_button.config(font=("Arial", 12), state='disabled', command=self.save_callback)

        # Initialize entry variables
        self.comport_name = tk.StringVar(value=None)
        self.heart_beat_channel = tk.StringVar(value=None)
        self.project_directory_var = tk.StringVar(value=None)
        self.M1_Valves = {'Coo' : tk.StringVar(value=None),
                          'Cen' : tk.StringVar(value=None),
                          'Def' : tk.StringVar(value=None)}
        self.M1_rewards = {'CC': MouseReward(), 'CD': MouseReward(),
                           'DC': MouseReward(), 'DD': MouseReward(),
                           'CN': MouseReward()}
        self.M2_Valves = {'Coo' : tk.StringVar(value=None),
                          'Cen' : tk.StringVar(value=None),
                          'Def' : tk.StringVar(value=None)}
        self.M2_rewards = {'CC': MouseReward(), 'CD': MouseReward(),
                           'DC': MouseReward(), 'DD': MouseReward(),
                           'CN': MouseReward()}
        self.calibration_reward = tk.StringVar(value='CC')
        self.calibration_mouse = tk.StringVar(value='M1')
        self.iterations = tk.StringVar(value=None)
        self.expected_volume = tk.StringVar(value=None)
        self.scan_iterations = tk.StringVar(value=None)
        self.scan_duration = tk.StringVar(value=None)

        # Populate Panels
        self.populate_system_parameters_panel()
        self.populate_valves_panel(self.M1ValvesPanel, self.M1_Valves)
        self.populate_valves_panel(self.M2ValvesPanel, self.M2_Valves)
        self.populate_reward_panel(self.M1RewardsPanel, self.M1_rewards)
        self.populate_reward_panel(self.M2RewardsPanel, self.M2_rewards)
        self.populate_calibration_panel()
        self.populate_scanning_panel()

        # control vars
        self.abort = False
        self.open_duration = 0
        self.open_iterations = 0
        self.open_channel_list = None
        self.iterations_count = 0
        self.channel_list_index = 0
        self.valve = None

        # queue the window init routines
        self.window.after_idle(self.init_window)

    def populate_reward_panel(self, panel, rewards):
        tk.Label(panel, text='Reward      Opening Time       Water Volume').place(x=15, y=25)
        tk.Label(panel, text=' Type               [mSec]                      [uL]').place(x=15, y=42)
        tk.Label(panel, text="CC").place(x=20, y=75)
        tk.Label(panel, text="CD").place(x=20, y=100)
        tk.Label(panel, text="DC").place(x=20, y=125)
        tk.Label(panel, text="DD").place(x=20, y=150)
        tk.Label(panel, text="Cen").place(x=20, y=175)
        for i, (key, value) in enumerate(rewards.items()):
            tk.Entry(panel, textvariable=value.opening_time, width = 5).place(x=92, y=75 + (i * 25))
            tk.Entry(panel, textvariable=value.water_volume, width=5).place(x=188, y=75 + (i * 25))

    def populate_calibration_panel(self):
        tk.Label(self.CalibrationPanel, text="Mouse:").place(x=5, y=28)
        tk.Label(self.CalibrationPanel, text="Reward:").place(x=5, y=63)
        tk.OptionMenu(self.CalibrationPanel, self.calibration_mouse, 'M1', 'M2').place(x=60, y=26)
        tk.OptionMenu(self.CalibrationPanel, self.calibration_reward, *list(self.M1_rewards.keys())).place(x=60, y=60)
        tk.Label(self.CalibrationPanel, text="Num of Iterations:").place(x=130, y=28)
        tk.Entry(self.CalibrationPanel, textvariable=self.iterations, width=7).place(x=270, y=28)
        tk.Label(self.CalibrationPanel, text="Expected Volume [uLit]:").place(x=130, y=63)
        tk.Entry(self.CalibrationPanel, textvariable=self.expected_volume, width=7, state='readonly').place(x=270, y=63)

    def populate_scanning_panel(self):
        tk.Label(self.ScanningPanel, text="Num of Iterations:").place(x=12, y=28)
        tk.Entry(self.ScanningPanel, textvariable=self.scan_iterations, width=8).place(x=145, y=28)
        tk.Label(self.ScanningPanel, text="Opening time [mSec]:").place(x=12, y=63)
        tk.Entry(self.ScanningPanel, textvariable=self.scan_duration, width=8).place(x=145, y=63)

    def populate_valves_panel(self, panel, valves):
        tk.Label(panel, text='Dig. Pin #:').place(x=2, y=50)
        for i, (key, value) in enumerate(valves.items()):
            tk.Label(panel, text=key).place(x=85 + (i * 60), y=25)
            tk.Entry(panel, textvariable=value, width = 5).place(x=80 + (i * 60), y=50)

    def init_window(self):
        path = fUtile.get_project_directory()
        if not path == 'Error':
            fUtile.set_project_directory(path)
            self.project_directory_var.set(path)
            sys_conf = fUtile.load_system_configuration('1.0')
            if not sys_conf.get('version') == 'Error':
                if sys_conf.get('version') == 'Init':
                    sys_conf = HWConfGUI.init_system_parameters()
                self.save_button.config(state='normal')
                self.calibrate_button.config(state='normal')
                self.scan_button.config(state='normal')
                self.comport_name.set(sys_conf.get('Com Port'))

                Arduino.openComPort(self.comport_name.get())
                self.heart_beat_channel.set(sys_conf.get('Heart Beat Channel'))
                
                for key in self.M1_Valves:
                    self.M1_Valves[key].set(sys_conf.get('M1 valves')[key])
                    self.M2_Valves[key].set(sys_conf.get('M2 valves')[key])
                for key in self.M1_rewards:
                    self.M1_rewards[key].opening_time.set(sys_conf.get('M1 Rewards').get(key)['opening time'])
                    self.M1_rewards[key].water_volume.set(sys_conf.get('M1 Rewards').get(key)['water volume'])
                    self.M2_rewards[key].opening_time.set(sys_conf.get('M2 Rewards').get(key)['opening time'])
                    self.M2_rewards[key].water_volume.set(sys_conf.get('M2 Rewards').get(key)['water volume'])
                self.iterations.set(sys_conf.get('Cal Iterations'))
                self.scan_iterations.set(sys_conf.get('Scan Iterations'))
                self.scan_duration.set(sys_conf.get('Scan Duration'))

    def is_valid_integer(self, value, entry_name, min, max):
        try:
            num = int(value)
        except ValueError:
            num = -1
        if num < min or num > max:
            messagebox.showerror('Invalid Input', f'{entry_name} is non integer or out of range')
            return False
        else:
            return True

    def validate_configuration(self):
        all_valid = True
        if not self.comport_name.get()[:3] == 'COM':
            all_valid = False
            messagebox.showerror('Invalid Input', 'com port name must start with COM')
        else:
            try:
                num = int(self.comport_name.get()[3:])
            except ValueError:
                num = -1
            if num < 0:
                all_valid = False
                messagebox.showerror('Invalid Input','com port name must start with COM (immediately followed by an integer)')

        if not self.is_valid_integer(self.heart_beat_channel.get(), 'Heart Beat Channel', 1, 12):
            all_valid = False
        for key in self.M1_Valves:
            if not self.is_valid_integer(self.M1_Valves[key].get(), f'M1 {key} valve dig pin num', 1, 12):
                all_valid = False
            if not self.is_valid_integer(self.M2_Valves[key].get(), f'M2 {key} valve dig pin num', 1, 12):
                all_valid = False
        for key in self.M1_rewards:
            if not self.is_valid_integer(self.M1_rewards[key].opening_time.get(), f'M1 {key} Reward opening time', 0, 200):
                all_valid = False
            if not self.is_valid_integer(self.M1_rewards[key].water_volume.get(), f'M1 {key} Reward water volume', 0, 30):
                all_valid = False
            if not self.is_valid_integer(self.M2_rewards[key].opening_time.get(), f'M2 {key} Reward opening time', 0, 200):
                all_valid = False
            if not self.is_valid_integer(self.M2_rewards[key].water_volume.get(), f'M2 {key} Reward water volume', 0, 30):
                all_valid = False

        if not self.is_valid_integer(self.scan_duration.get(), 'Scan opening time', 1,200):
            all_valid = False
        if not self.is_valid_integer(self.iterations.get(), 'Calibrate num of Iterations', 1,50):
            all_valid = False
        if not self.is_valid_integer(self.scan_iterations.get(), 'Scan iterations', 1, 50):
            all_valid = False

        if all_valid:   # if all the parameters are valid check for proper relationships
            for key in self.M1_rewards:
                if self.M1_rewards[key].opening_time.get() == '0' or self.M1_rewards[key].water_volume.get() == '0':
                    if not (self.M1_rewards[key].opening_time.get() == '0' and self.M1_rewards[key].water_volume.get() == '0'):
                        messagebox.showerror('Invalid Input',
                                             f'M1 {key} reward: if one of the arguments is 0 both must be 0')
                        all_valid = False
                if self.M2_rewards[key].opening_time.get() == '0' or self.M2_rewards[key].water_volume.get() == '0':
                    if not (self.M2_rewards[key].opening_time.get() == '0' and self.M2_rewards[key].water_volume.get() == '0'):
                        messagebox.showerror('Invalid Input',
                                             f'M2 {key} reward: if one of the arguments is 0 both must be 0')
                        all_valid = False
        return all_valid

    def save_callback(self):
        if self.validate_configuration():
            m1_valves = {}
            m2_valves = {}
            m1_rewards = {}
            m2_rewards = {}
            for key in self.M1_Valves:
                m1_valves[key] = self.M1_Valves[key].get()
                m2_valves[key] = self.M2_Valves[key].get()
            for key in self.M1_rewards:
                m1_rewards[key] = {'opening time': self.M1_rewards[key].opening_time.get(),
                                   'water volume': self.M1_rewards[key].water_volume.get()}
                m2_rewards[key] = {'opening time': self.M2_rewards[key].opening_time.get(),
                                   'water volume': self.M2_rewards[key].water_volume.get()}
            sys_par = {
                 'version': '1.0',
                 'Com Port': self.comport_name.get(),
                 'Heart Beat Channel': self.heart_beat_channel.get(),
                 'M1 valves': m1_valves,
                 'M2 valves': m2_valves,
                 'M1 Rewards': m1_rewards,
                 'M2 Rewards': m2_rewards,
                 'Cal Iterations': self.iterations.get(),
                 'Scan Iterations': self.scan_iterations.get(),
                 'Scan Duration': self.scan_duration.get()
            }
            fUtile.save_system_configuration(sys_par)

    @staticmethod
    def init_system_parameters():
        return {'version': '1.0',
                'Com Port': 'COM11',
                'Heart Beat Channel': '4',
                'M1 valves': {'Coo': '1',
                              'Cen': '1',
                              'Def': '1'
                              },
                'M2 valves': {'Coo': '1',
                              'Cen': '1',
                              'Def': '1'
                              },
                'M1 Rewards': {'CC': {'opening time': '1', 'water volume': '12'},
                               'CD': {'opening time': '1', 'water volume': '0'},
                               'DC': {'opening time': '1', 'water volume': '16'},
                               'DD': {'opening time': '1', 'water volume': '3'},
                               'CN': {'opening time': '1', 'water volume': '2'}
                               },
                'M2 Rewards': {'CC': {'opening time': '1', 'water volume': '12'},
                               'CD': {'opening time': '1', 'water volume': '16'},
                               'DC': {'opening time': '1', 'water volume': '0'},
                               'DD': {'opening time': '1', 'water volume': '3'},
                               'CN': {'opening time': '1', 'water volume': '2'}
                               },
                'Cal Iterations': '25',
                'Scan Iterations': '2',
                'Scan Duration': 10
                }

    def scan_callback(self):
        if self.validate_configuration():
            self.disable_buttons()
            self.open_channel_list = []
            self.channel_list_index = 0
            for key in self.M1_Valves:
                self.open_channel_list.append(int(self.M1_Valves[key].get()))
            for key in self.M2_Valves:
                self.open_channel_list.append(int(self.M2_Valves[key].get()))
            self.open_duration = int(self.scan_duration.get()) / 1000  # Convert duration from milliseconds to seconds
            self.open_iterations = int(self.scan_iterations.get())
            self.open_valves()

    def disable_buttons(self):
        self.calibrate_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.scan_button.config(state='disabled')
        self.abort_button.config(state='normal')

    def enable_buttons(self):
        self.calibrate_button.config(state='normal')
        self.save_button.config(state='normal')
        self.scan_button.config(state='normal')
        self.abort_button.config(state='disabled')

    def calibrate_callback(self):
        self.disable_buttons()
        valve_map = {'CC': ('Coo', 'Coo'),
                     'CD': ('Coo', 'Def'),
                     'DC': ('Def', 'Coo'),
                     'DD': ('Def', 'Def'),
                     'CN': ('Cen', 'Cen')
                     }
        if self.calibration_mouse.get() == 'M1':
            valve = self.M1_Valves
            reward = self.M1_rewards
            valve_index = 0
        else:
            valve = self.M2_Valves
            reward = self.M2_rewards
            valve_index = 1
        self.open_channel_list = [int(valve[valve_map[self.calibration_reward.get()][valve_index]].get())]
        self.open_duration = int(reward[self.calibration_reward.get()].opening_time.get())
        self.open_duration = self.open_duration / 1000  # Convert duration from milliseconds to seconds
        self.open_iterations = int(self.iterations.get())
        self.iterations_count = 0
        self.channel_list_index = 0
        volume = int(reward[self.calibration_reward.get()].water_volume.get())
        self.expected_volume.set(str(volume * self.open_iterations))
        self.open_valves()

    def abort_callback(self):
        self.abort = True

    def open_valves(self):
        if not self.abort:
            if self.iterations_count == 0:
                    self.valve = ValveControl(self.open_channel_list[self.channel_list_index])
            if self.iterations_count < self.open_iterations:
                self.iterations_count += 1
                print(f'Calibrating valve on pin {self.open_channel_list[self.channel_list_index]}. Iteration #: {self.iterations_count}')
                self.valve.OpenValve(self.open_duration)
                while self.valve.IsValveOpen():
                    pass
                print(f"Valve on pin {self.open_channel_list[self.channel_list_index]} closed.")
            else:
                self.iterations_count = 0
                self.channel_list_index += 1
                del self.valve
                if self.channel_list_index == len(self.open_channel_list):
                    self.abort = True
        if not self.abort:
            self.window.after(2000, self.open_valves)
        else:
            self.enable_buttons()
            self.abort = False

    def populate_system_parameters_panel(self):
        tk.Label(self.system_panel, text="Project Directory:").place(x=5, y=30)
        pd_name_entry = tk.Entry(self.system_panel, width=60, textvariable=self.project_directory_var)
        pd_name_entry.place(x=110, y=30)
        pd_button = tk.Button(self.window, text="Browse", command=self.browse_project_directory)
        pd_button.place(x=490, y=30)
        tk.Label(self.system_panel, text="COM port name:").place(x = 40, y = 60)
        comport_name_entry = tk.Entry(self.system_panel, textvariable = self.comport_name, width=10)
        comport_name_entry.place(x = 150, y = 60)
        tk.Label(self.system_panel, text="Heart Beat Dig Pin #:").place(x=270, y=60)
        comport_name_entry = tk.Entry(self.system_panel, textvariable=self.heart_beat_channel, width=10)
        comport_name_entry.place(x=400, y=60)

    def browse_project_directory(self):
        directory_path = filedialog.askdirectory(title="Select a directory")
        if directory_path != "":
            self.project_directory_var.set(directory_path)
            fUtile.set_project_directory(self.project_directory_var.get())
            self.init_window()

    def run_GUI(self):
        self.window.mainloop()












