import tkinter as tk
from tkinter import messagebox
from modelling_opponent.OpponentType import OpponentType

class ExperimentGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma Experiment")
        self.window.geometry("500x620")

        # create window layout
        self.system_panel = tk.Frame(self.window, width = 490, height = 60, relief = tk.RAISED, borderwidth = 2)
        tk.Label(self.system_panel, text = "System Parameters").place(x = 210, y = 2)
        self.experiment_panel = tk.Frame(self.window, width=490, height=185, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.experiment_panel, text ="Experiment Parameters").place(x = 200, y = 2)
        self.first_opponent_panel = tk.Frame(self.window, width=243, height=325, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.first_opponent_panel, text ="First Opponent").place(x = 70, y = 2)
        self.second_opponent_panel = tk.Frame(self.window, width=243, height=325, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.second_opponent_panel, text ="Second Opponent").place(x = 70, y = 2)
        self.system_panel.place(x = 5, y = 5)
        self.experiment_panel.place(x = 5, y = 70)
        self.first_opponent_panel.place(x = 5, y = 260)
        self.second_opponent_panel.place(x = 252, y = 260)

        # Initialize entry variables
        self.experiment_name = tk.StringVar(value = "Experiment 1")
        self.comport_name = tk.StringVar(value = "COM11")
        self.num_trials_var = tk.StringVar(value = "20")
        self.return_time_var = tk.StringVar(value = "30")
        self.decision_time_var = tk.StringVar(value = "30")
        self.mouse_id_var = tk.StringVar(value="1777")
        self.first_opponent_type = tk.StringVar(value = None)
        self.second_opponent_type = tk.StringVar(value = None)
        self.first_opponent_strategy = tk.StringVar(value = None)
        self.second_opponent_strategy = tk.StringVar(value = None)
        self.first_opponent_prob = tk.StringVar(value = None)
        self.second_opponent_prob = tk.StringVar(value = None)

        # Control Variables
        self.start_button_clicked = False

    def setup_gui(self):
        # Entry fields for trials, duration, etc.
        self.populate_system_parameters_panel()
        self.create_input_fields()
        self.create_opponent_options(self.first_opponent_panel, self.first_opponent_type, "Mouse")
        self.create_opponent_options(self.second_opponent_panel, self.second_opponent_type, "Fixed Strategy")
        self.create_strategy_option(self.first_opponent_panel, self.first_opponent_strategy, self.first_opponent_prob)
        self.create_strategy_option(self.second_opponent_panel, self.second_opponent_strategy, self.second_opponent_prob)

        # Create a button to start the experiment
        self.start_button = tk.Button(self.window, text="Start Experiment", command=self.start_experiment)
        self.start_button.place(x = 205, y = 590)

        self.window.mainloop()


    def populate_system_parameters_panel(self):
        tk.Label(self.system_panel, text="COM port name:").place(x = 30, y = 30)
        comport_name_entry = tk.Entry(self.system_panel, textvariable = self.comport_name)
        comport_name_entry.place(x = 200, y = 30)

    def get_opponent_type(self,opponent_type_str):
        mapping = {
            "Mouse": OpponentType.MOUSE,
            "Fixed Strategy": OpponentType.FIXED_STRATEGY,
            "Learner": OpponentType.LEARNER
        }
        return mapping.get(opponent_type_str, None)

    def create_opponent_options(self, panel, opvar, default):
        # Create opponent type selection radio buttons
        tk.Label(panel, text="Opponent type:").place(x = 5, y = 25)
        opponent_types = ["Mouse", "Fixed Strategy", "Learner"]
        opvar.set(default)
        buttonoffset = 0
        for type in opponent_types:
            radiobutton = tk.Radiobutton(panel, text = type, variable = opvar, value = type)
            radiobutton.place(x = 50, y = 50 + buttonoffset * 25)
            buttonoffset += 1
            if type == "Learner":
                radiobutton.config(state='disabled')

    def create_input_fields(self):
        tk.Label(self.experiment_panel, text="Experiment Name:").place(x = 30, y = 30)
        experiment_name_entry = tk.Entry(self.experiment_panel, textvariable = self.experiment_name)
        experiment_name_entry.place(x = 200, y = 30)

        tk.Label(self.experiment_panel, text="Number of Trials:").place(x = 30, y = 60)
        self.num_trials_entry = tk.Entry(self.experiment_panel, textvariable=self.num_trials_var)
        self.num_trials_entry.place(x = 200, y = 60)

        tk.Label(self.experiment_panel, text="Decision Time (seconds):").place(x = 30, y = 90)
        self.decision_time_entry = tk.Entry(self.experiment_panel, textvariable=self.return_time_var)
        self.decision_time_entry.place(x = 200, y = 90)

        tk.Label(self.experiment_panel, text="Return to center (seconds):").place(x = 30, y = 120)
        self.decision_time_entry = tk.Entry(self.experiment_panel, textvariable=self.decision_time_var)
        self.decision_time_entry.place(x = 200, y = 120)

        tk.Label(self.experiment_panel, text="Mouse ID:").place(x=30, y=150)
        mouse_id_entry = tk.Entry(self.experiment_panel, textvariable=self.mouse_id_var)
        mouse_id_entry.place(x=200, y=150)

    def create_strategy_option(self, panel, opvar, probvar):
        # Define strategy options
        tk.Label(panel, text="Select Strategy:").place(x = 5, y = 140)
        strategies = ["Unconditional Cooperator", "Unconditional Defector", "Random", "Tit for Tat",
                      "Probability p Cooperator"]
        opvar.set("Unconditional Cooperator")
        buttonoffset = 0
        for strategy in strategies:
            radiobutton = tk.Radiobutton(panel, text = strategy, variable = opvar, value = strategy)
            radiobutton.place(x = 50, y = 165 + buttonoffset * 25)
            buttonoffset += 1

        tk.Label(panel, text="Probability: ").place(x = 5, y = 295)
        probvar.set("0.1")
        probability_entry = tk.Entry(panel, textvariable = probvar)
        probability_entry.place(x = 80, y = 295)

    def start_experiment(self):
        # Validate the input values
        if not self.validate_inputs():
            messagebox.showerror("Invalid Input", "Please check your inputs.")
            return

        # Display a confirmation or start the experiment
        self.start_button_clicked = True
        messagebox.showinfo("Experiment Starting", "The experiment is now starting with the provided settings.")
        self.window.destroy()

    def validate_inputs(self):
        # Retrieve the field values
        num_trials_str = self.num_trials_var.get()
        trial_duration_str = self.return_time_var.get()
        decision_time_str = self.decision_time_var.get()
        mouse_id_str = self.mouse_id_var.get()
        if not num_trials_str or not trial_duration_str or not decision_time_str:
            messagebox.showerror("Invalid Input", "One or more fields are empty. Please fill out all fields.")
            return False

        try:
            # Convert the field values to integers
            num_trials = int(num_trials_str)
            trial_duration = int(trial_duration_str)
            decision_time = int(decision_time_str)
            mouse_id = int(mouse_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for trials, duration, and decision time.")
            return False

        # Check if the values are greater than zero
        if num_trials <= 0 or trial_duration <= 0 or decision_time <= 0:
            messagebox.showerror("Invalid Input", "Values must be greater than zero.")
            return False

        return True

    def experiment_started(self):
        return self.start_button_clicked

    def get_com_port(self):
        return self.comport_name.get()

    def get_experiment_parameters(self):
        settings = {
            'experiment_name' : self.experiment_name.get(),
            'num_trials': int(self.num_trials_var.get()),
            'return_time': int(self.return_time_var.get()),
            'decision_time': int(self.decision_time_var.get()),
            'mouse_id': int(self.mouse_id_var.get())}
        print(settings)
        return settings

    def get_opponent_configuration(self):
        settings = {
            'opponent1_type': self.get_opponent_type(self.first_opponent_type.get()),
            'opponent2_type': self.get_opponent_type(self.second_opponent_type.get()),
            'opponent1_strategy': self.first_opponent_strategy.get(),
            'opponent2_strategy': self.second_opponent_strategy.get(),
            'opponent1_probability' : self.first_opponent_prob.get(),
            'opponent2_probability' : self.second_opponent_prob.get()}
        print(settings)
        return settings

