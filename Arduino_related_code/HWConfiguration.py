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
import time

class Mouse_Valve:
    def __init__(self, location_id):
        self.location_id = location_id
        self.digital_pin_num = tk.StringVar(value=None)
        self.time_unit = tk.StringVar(value=None)

class HWConfGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma, HW Configuration screen")
        self.window.geometry("555x576")

        # create window layout
        self.system_panel = tk.Frame(self.window, width=545, height=90, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.system_panel, text="System Parameters").place(x=210, y=2)
        self.M1Panel = tk.Frame(self.window, width=270, height=285, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M1Panel, text='Mouse 1 - Valves', font=("Arial", 8)).place(x=80, y=2)
        self.M2Panel = tk.Frame(self.window, width=270, height=285, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.M2Panel, text='Mouse 2 - Valves', font=("Arial", 8)).place(x=80, y=2)
        self.CalibrationPanel = tk.Frame(self.window, width=220, height=180, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.CalibrationPanel, text='Valve Calibration', font=("Arial", 8)).place(x=50, y=2)
        self.RewardPanel = tk.Frame(self.window, width=220, height=180, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.RewardPanel, text='Reward Matrix [uLiter]', font=("Arial", 8)).place(x=50, y=2)

        self.system_panel.place(x=5, y=5)
        self.M1Panel.place(x=5, y=100)
        self.M2Panel.place(x=280, y=100)
        self.CalibrationPanel.place(x=5, y=390)
        self.RewardPanel.place(x=330, y=390)

        self.calibrate_button = tk.Button(self.window, text="Calibrate")
        self.calibrate_button.place(x=240, y=420)
        self.calibrate_button.config(font=("Arial", 12), state='disabled', command=self.calibrate_callback)

        self.update_button = tk.Button(self.window, text="Set Value")
        self.update_button.place(x=238, y=475)
        self.update_button.config(font=("Arial", 12), state='disabled', command=self.set_value_callback)

        self.save_button = tk.Button(self.window, text="Save")
        self.save_button.place(x=255, y=530)
        self.save_button.config(font=("Arial", 12), state='disabled', command=self.save_callback)

        # Initialize entry variables
        self.comport_name = tk.StringVar(value=None)
        self.heart_beat_channel = tk.StringVar(value=None)
        self.project_directory_var = tk.StringVar(value=None)
        self.Valves = {'M1 Coo' : Mouse_Valve('M1 Coo'),
                       'M1 Cen' : Mouse_Valve('M1 Cen'),
                       'M1 Def' : Mouse_Valve('M1 Def'),
                       'M2 Coo' : Mouse_Valve('M2 Coo'),
                       'M2 Cen' : Mouse_Valve('M2 Cen'),
                       'M2 Def' : Mouse_Valve('M2 Def')}
        self.valve_name = tk.StringVar(value=None)
        self.duration = tk.StringVar(value=None)
        self.iterations = tk.StringVar(value=None)
        self.volume = tk.StringVar(value=None)
        self.M1_rewards = {'CC': tk.StringVar(value=None), 'CD': tk.StringVar(value=None),
                           'DC': tk.StringVar(value=None), 'DD': tk.StringVar(value=None),
                           'CN': tk.StringVar(value=None)}
        self.M2_rewards = {'CC': tk.StringVar(value=None), 'CD': tk.StringVar(value=None),
                           'DC': tk.StringVar(value=None), 'DD': tk.StringVar(value=None),
                           'CN': tk.StringVar(value=None)}

        # Populate Panels
        self.populate_system_parameters_panel()
        self.populate_mice_valves(self.M1Panel, self.Valves.get('M1 Coo'), 1)
        self.populate_mice_valves(self.M1Panel, self.Valves.get('M1 Cen'), 2)
        self.populate_mice_valves(self.M1Panel, self.Valves.get('M1 Def'), 3)
        self.populate_mice_valves(self.M2Panel, self.Valves.get('M2 Coo'), 1)
        self.populate_mice_valves(self.M2Panel, self.Valves.get('M2 Cen'), 2)
        self.populate_mice_valves(self.M2Panel, self.Valves.get('M2 Def'), 3)
        self.populate_calibration_panel()
        self.populate_reward_panel()

        self.init_window()

    def populate_reward_panel(self):
        tk.Label(self.RewardPanel, text="M1    M2                 M1         M2").place(x=20, y=25)
        tk.Label(self.RewardPanel, text=" C       C").place(x=20, y=50)
        tk.Label(self.RewardPanel, text=" C       D").place(x=20, y=75)
        tk.Label(self.RewardPanel, text=" D       C").place(x=20, y=100)
        tk.Label(self.RewardPanel, text=" D       D").place(x=20, y=125)
        tk.Label(self.RewardPanel, text="Cen   Cen").place(x=18, y=150)
        self.create_reward_entry(self.M1_rewards.get('CC'),1,1)
        self.create_reward_entry(self.M1_rewards.get('CD'), 1, 2)
        self.create_reward_entry(self.M1_rewards.get('DC'), 1, 3)
        self.create_reward_entry(self.M1_rewards.get('DD'), 1, 4)
        self.create_reward_entry(self.M1_rewards.get('CN'), 1, 5)
        self.create_reward_entry(self.M2_rewards.get('CC'), 2, 1)
        self.create_reward_entry(self.M2_rewards.get('CD'), 2, 2)
        self.create_reward_entry(self.M2_rewards.get('DC'), 2, 3)
        self.create_reward_entry(self.M2_rewards.get('DD'), 2, 4)
        self.create_reward_entry(self.M2_rewards.get('CN'), 2, 5)

    def create_reward_entry(self, entry, x_ind, y_ind):
        x_loc = 110 + 45 * (x_ind - 1)
        y_loc = 50 + 25 * (y_ind - 1)
        tk.Entry(self.RewardPanel, textvariable=entry, width=5).place(x=x_loc, y=y_loc)

    def populate_calibration_panel(self):
        tk.Label(self.CalibrationPanel, text="Valve Name:").place(x=5, y=25)
        valve_list = list(self.Valves.keys())
        self.valve_name.set('Scan')
        valve_list.append(self.valve_name.get())
        tk.OptionMenu(self.CalibrationPanel, self.valve_name, *valve_list).place(x=110, y=23)
        tk.Label(self.CalibrationPanel, text="Opening Time [mSec]:").place(x=5, y=70)
        tk.Entry(self.CalibrationPanel, textvariable=self.duration, width=10).place(x=140, y=70)
        tk.Label(self.CalibrationPanel, text="Num of Iterations:").place(x=5, y=110)
        tk.Entry(self.CalibrationPanel, textvariable=self.iterations, width=10).place(x=140, y=110)
        tk.Label(self.CalibrationPanel, text="Water Volume [uLit]:").place(x=5, y=150)
        tk.Entry(self.CalibrationPanel, textvariable=self.volume, width=10).place(x=140, y=150)

    def populate_mice_valves(self, panel, location, position):
        xBase = 5
        yBase = 25 + 85 * (position - 1)
        valve_panel = tk.Frame(panel, width=250, height=80, relief=tk.RAISED, borderwidth=2)
        valve_panel.place(x=5, y=yBase)
        tk.Label(valve_panel, text=location.location_id).place(x=xBase + 175, y=2)
        tk.Entry(valve_panel, textvariable=location.digital_pin_num, width = 10).place(x=xBase+165, y=25)
        tk.Label(valve_panel, text="Arduino Digital Pin Number:").place(x=xBase + 5, y=25)
        tk.Entry(valve_panel, textvariable=location.time_unit, width = 10).place(x=xBase+165, y=50)
        tk.Label(valve_panel, text="Opening Time [mSec/uLit]:").place(x=xBase + 5, y=50)

    def init_window(self):
        path = fUtile.get_project_directory()
        if not path == 'Error':
            fUtile.set_project_directory(path)
            self.project_directory_var.set(path)
            sys_par = fUtile.load_system_configuration('1.0')
            if not sys_par.get('version') == 'Error':
                if sys_par.get('version') == 'Init':
                    sys_par = HWConfGUI.init_system_parameters()
                self.save_button.config(state='normal')
                self.calibrate_button.config(state='normal')
                self.update_button.config(state='normal')
                self.comport_name.set(sys_par.get('Com Port'))
                Arduino.openComPort(self.comport_name.get())
                self.heart_beat_channel.set(sys_par.get('Heart Beat Channel'))
                for key in self.Valves:
                    self.Valves[key].digital_pin_num.set(sys_par.get('valves').get(key).get('Channel'))
                    self.Valves[key].time_unit.set(sys_par.get('valves').get(key).get('flow unit'))
                self.duration.set(sys_par.get('Cal Open Time'))
                self.iterations.set(sys_par.get('Cal Open Iteration'))
                self.volume.set(sys_par.get('Cal Volume'))
                for key in self.M1_rewards:
                    self.M1_rewards[key].set(sys_par.get('M1 Rewards').get(key))
                    self.M2_rewards[key].set(sys_par.get('M2 Rewards').get(key))

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

    def is_valid_float(self, value, entry_name, min, max):
        try:
            num = float(value)
        except ValueError:
            num = -1
        if num < min or num > max:
            messagebox.showerror('Invalid Input', f'{entry_name} is non numeric or out of range')
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
        for key in self.Valves:
            if not self.is_valid_integer(self.Valves.get(key).digital_pin_num.get(), f'{key} valve dig pin num', 1, 12):
                all_valid = False
            if not self.is_valid_float(self.Valves.get(key).time_unit.get(), f'{key} valve flow unit', 1,200):
                all_valid = False
        if not self.is_valid_integer(self.duration.get(), 'Opening time', 1,200):
            all_valid = False
        if not self.is_valid_integer(self.iterations.get(), 'Num of Iterations', 1,50):
            all_valid = False
        if not self.is_valid_integer(self.volume.get(), 'Water Volume', 1, 150):
            all_valid = False
        for key in self.M1_rewards:
            if not self.is_valid_integer(self.M1_rewards.get(key).get(), f'M1 {key} Reward', 0, 30):
                all_valid = False
            if not self.is_valid_integer(self.M2_rewards.get(key).get(), f'M2 {key} Reward', 0, 30):
                all_valid = False
        return all_valid

    def save_callback(self):
        if self.validate_configuration():
            valves = {}
            for key in self.Valves:
                valves[key] = {'Channel': self.Valves.get(key).digital_pin_num.get(),
                               'flow unit': self.Valves.get(key).time_unit.get()}
            m1 = {}
            m2 = {}
            for key in self.M1_rewards:
                m1[key] = self.M1_rewards.get(key).get()
                m2[key] = self.M2_rewards.get(key).get()

            sys_par = {
                 'version': '1.0',
                 'Com Port': self.comport_name.get(),
                 'Heart Beat Channel': self.heart_beat_channel.get(),
                 'valves': valves,
                 'Cal Open Time': self.duration.get(),
                 'Cal Open Iteration': self.iterations.get(),
                 'Cal Volume': self.volume.get(),
                 'M1 Rewards': m1,
                 'M2 Rewards': m2}
            fUtile.save_system_configuration(sys_par)

    @staticmethod
    def init_system_parameters():
        return {'version': '1.0',
                'Com Port': 'COM11',
                'Heart Beat Channel': '4',
                'valves': {'M1 Coo': {'Channel': '1',
                                      'flow unit': '1'},
                           'M1 Cen': {'Channel': '1',
                                      'flow unit': '1'},
                           'M1 Def': {'Channel': '1',
                                      'flow unit': '1'},
                           'M2 Coo': {'Channel': '1',
                                      'flow unit': '1'},
                           'M2 Cen': {'Channel': '1',
                                      'flow unit': '1'},
                           'M2 Def': {'Channel': '1',
                                      'flow unit': '1'}
                           },
                'Cal Open Time': '40',
                'Cal Open Iteration': '25',
                'Cal Volume': '100',
                'M1 Rewards': {'CC': '12',
                               'CD': '0',
                               'DC': '16',
                               'DD': '3',
                               'CN': '2'
                               },
                'M2 Rewards': {'CC': '12',
                               'CD': '0',
                               'DC': '16',
                               'DD': '3',
                               'CN': '2'
                               }
                }

    def set_value_callback(self):
        if not self.valve_name.get() == 'Scan':
            time_unit = float(self.duration.get()) * float(self.iterations.get()) / float(self.volume.get())
            self.Valves[self.valve_name.get()].time_unit.set(time_unit)
        else:
            messagebox.showerror('Invalid Input', 'PLease select a specific valve to Set')

    def calibrate_callback(self):
        for key, value in self.Valves.items():
           if self.valve_name.get() == key or self.valve_name.get() == 'Scan':
               self.calibrate_valve(self.Valves.get(key))

    def calibrate_valve(self, valve: Mouse_Valve):
        pin = int(valve.digital_pin_num.get())
        valve_control = ValveControl(pin)
        duration_s = float(self.duration.get())  / 1000  # Convert duration from milliseconds to seconds
        time.sleep(4)
        for i in range(int(self.iterations.get())):
            print(f"Calibrating valve on pin {pin}: Iteration {i + 1}")
            valve_control.OpenValve(duration_s)  # Open valve for the specified duration in seconds
            while valve_control.IsValveOpen():
                pass
            print(f"Valve on pin {pin} closed.")
            time.sleep(1)  # Short delay between iterations
        del valve_control

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












