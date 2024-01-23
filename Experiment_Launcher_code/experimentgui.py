import tkinter as tk
from tkinter import messagebox
from modelling_opponent.OpponentType import OpponentType

class ExperimentGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma Experiment")
        self.window.geometry("500x630")

        # create window layout
        self.system_panel = tk.Frame(self.window, width = 490, height = 60, relief = tk.RAISED, borderwidth = 2)
        tk.Label(self.system_panel, text = "System Parameters").place(x = 210, y = 2)
        self.experiment_panel = tk.Frame(self.window, width=490, height=300, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.experiment_panel, text ="Experiment Parameters").place(x = 200, y = 2)
        self.first_opponent_panel = tk.Frame(self.window, width=245, height=250, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.first_opponent_panel, text ="First Computer Opponent Strategy").place(x = 20, y = 2)
        self.second_opponent_panel = tk.Frame(self.window, width=245, height=250, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.second_opponent_panel, text ="Second Computer Opponent Strategy").place(x = 20, y = 2)
        self.system_panel.place(x = 5, y = 5)
        self.experiment_panel.place(x = 5, y = 70)
        self.first_opponent_panel.place(x = 5, y = 370)
        self.second_opponent_panel.place(x = 250, y = 370)

        # Initialize entry variables
        self.experiment_name = tk.StringVar(value = "Experiment 1")
        self.comport_name = tk.StringVar(value = "COM11")
        self.num_trials_var = tk.StringVar(value = "50")
        self.return_time_var = tk.StringVar(value = "20")
        self.decision_time_var = tk.StringVar(value = "20")
        self.mouse_id_var = tk.StringVar(value="1777")
        self.selected_opp = tk.StringVar(value = None)
        self.first_opponent_type = tk.StringVar(value = None)
        self.second_opponent_type = tk.StringVar(value = None)
        self.first_opponent_prob = tk.StringVar(value = None)
        self.second_opponent_prob = tk.StringVar(value = None)

    def setup_gui(self):
        # Entry fields for trials, duration, etc.
        self.populate_system_parameters_panel()
        self.create_input_fields()
        self.create_opp_options()

        self.create_strategy_option(self.first_opponent_panel, self.first_opponent_type, self.first_opponent_prob)
        self.create_strategy_option(self.second_opponent_panel, self.second_opponent_type, self.second_opponent_prob)

        # Create a button to start the experiment and disable it initially
        self.start_button = tk.Button(self.window, text="Start Experiment", command=self.start_experiment)
        self.start_button.place(x = 205, y = 590)

        self.window.mainloop()


    def populate_system_parameters_panel(self):
        tk.Label(self.system_panel, text="COM port name:").place(x = 30, y = 30)
        comport_name_entry = tk.Entry(self.system_panel, textvariable = self.comport_name)
        comport_name_entry.place(x = 200, y = 30)

    def get_opponent_type(self,opponent_type_str):
        mapping = {
            "mouse_mouse": OpponentType.MOUSE_MOUSE,
            "mouse_computer": OpponentType.MOUSE_COMPUTER,
            "computer_computer": OpponentType.COMPUTER_COMPUTER
        }
        return mapping.get(opponent_type_str, None)

    def create_opp_options(self):
        # Create opponent selection radio buttons
        tk.Label(self.experiment_panel, text="Select the opponent:").place(x = 30, y = 180)
        self.selected_opp.set("mouse_computer")
        opp_options = [ ("Mouse and Mouse", "mouse_mouse"),
                        ("Mouse and Computer", "mouse_computer"),
                        ("Computer and Computer", "computer_computer")]

        buttonoffset = 0
        for text, mode in opp_options:
            radiobutton = tk.Radiobutton(self.experiment_panel, text=text, variable=self.selected_opp, value=mode)
            radiobutton.place(x = 200, y = 180 + buttonoffset * 30)
            buttonoffset += 1

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
        strategies = ["Unconditional Cooperator", "Unconditional Defector", "Random", "Tit for Tat",
                      "Probability p Cooperator","q learner"]
        opvar.set("Unconditional Cooperator")
        buttonoffset = 0
        for strategy in strategies:
            radiobutton = tk.Radiobutton(panel, text = strategy, variable = opvar, value = strategy)
            radiobutton.place(x = 50, y = 30 + buttonoffset * 30)
            buttonoffset += 1

        tk.Label(panel, text="Probability: ").place(x = 5, y = 210)
        probvar.set("0.1")
        probability_entry = tk.Entry(panel, textvariable = probvar)
        probability_entry.place(x = 80, y = 210)

    def start_experiment(self):
        # Validate the input values
        if not self.validate_inputs():
            messagebox.showerror("Invalid Input", "Please check your inputs.")
            return

        # Display a confirmation or start the experiment
        messagebox.showinfo("Experiment Starting", "The experiment is now starting with the provided settings.")
        self.window.destroy()

    def validate_inputs(self):
        # Retrieve the field values
        num_trials_str = self.num_trials_var.get()
        trial_duration_str = self.return_time_var.get()
        decision_time_str = self.decision_time_var.get()

        strategy1 = self.first_opponent_type.get()
        strategy2 = self.first_opponent_type.get()

        if not num_trials_str or not trial_duration_str or not decision_time_str:
            messagebox.showerror("Invalid Input", "One or more fields are empty. Please fill out all fields.")
            return False

        try:
            # Convert the field values to integers
            num_trials = int(num_trials_str)
            trial_duration = int(trial_duration_str)
            decision_time = int(decision_time_str)

            # Check if the values are greater than zero
            if num_trials <= 0 or trial_duration <= 0 or decision_time <= 0:
                messagebox.showerror("Invalid Input", "Values must be greater than zero.")
                return False

            return True

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for trials, duration, and decision time.")
            return False

    def on_start_clicked(self):
        # Retrieve settings when the button is clicked
        settings = self.get_settings()
        if settings:
            # If settings are valid, proceed with the next steps
            print("Settings retrieved:", settings)
            return settings

        else:
            # Handle the case where settings are not valid
            print("Invalid settings. Please check your inputs.")


    def get_settings(self):
        if not self.validate_inputs():
            # If validation fails, show an error message and then close the window
            messagebox.showerror("Invalid Input",
                                 "Invalid input detected. You must restart the application to try again.")

            return None
        try:
            # Retrieve the values from StringVars
            num_trials = int(self.num_trials_var.get())
            return_time = int(self.return_time_var.get())
            decision_time = int(self.decision_time_var.get())
            mouse_id = int(self.mouse_id_var.get())
            opponent_type=self.selected_opp.get()

            first_opponent_strategy = self.first_opponent_type.get()
            second_opponent_strategy = self.second_opponent_type.get()

            settings = {
                'experiment_name' : self.experiment_name.get(),
                'comport_name' : self.comport_name.get(),
                'num_trials': num_trials,
                'return_time': return_time,
                'decision_time': decision_time,
                'mouse_id': mouse_id,
                'opponent_type': self.get_opponent_type(opponent_type),
                'opponent1_strategy': first_opponent_strategy,
                'opponent2_strategy': second_opponent_strategy,
                'opponent1_probability' : self.first_opponent_prob.get(),
                'opponent2_probability' : self.second_opponent_prob.get()
            }

            #print(settings)
            return settings

        except ValueError:
            # Handle the case where the input is not a valid integer
            messagebox.showerror("Invalid Input", "Please enter valid numbers for trials, duration, and decision time.")
            return None

