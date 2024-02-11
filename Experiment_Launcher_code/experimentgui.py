import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from modelling_opponent.OpponentType import OpponentType
import Data_analysis.FileUtilities as fUtile

class ExperimentGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma Experiment setup")
        self.window.geometry("550x620")

        # create window layout
        self.system_panel = tk.Frame(self.window, width = 540, height = 90, relief = tk.RAISED, borderwidth = 2)
        tk.Label(self.system_panel, text = "System Parameters").place(x = 210, y = 2)
        self.experiment_panel = tk.Frame(self.window, width=540, height=122, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.experiment_panel, text ="Experiment Parameters").place(x = 200, y = 2)
        self.first_opponent_panel = tk.Frame(self.window, width=268, height=500, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.first_opponent_panel, text ="First Opponent").place(x = 70, y = 2)
        self.second_opponent_panel = tk.Frame(self.window, width=268, height=500, relief=tk.RAISED, borderwidth=2)
        tk.Label(self.second_opponent_panel, text ="Second Opponent").place(x = 70, y = 2)
        self.system_panel.place(x = 5, y = 5)
        self.experiment_panel.place(x = 5, y = 100)
        self.first_opponent_panel.place(x = 5, y = 227)
        self.second_opponent_panel.place(x = 277, y = 227)

        # Initialize entry variables
        self.comport_name = tk.StringVar(value = "COM11")
        self.project_directory_var = tk.StringVar(value = None)
        self.experiment_name = tk.StringVar(value = "Experiment-1")
        self.session_type = tk.StringVar(value = "Session")
        self.session_num = tk.StringVar(value = "1")
        self.num_trials_var = tk.StringVar(value = "50")
        self.return_time_var = tk.StringVar(value = "20")
        self.decision_time_var = tk.StringVar(value = "20")
        self.mouse_1_id = tk.StringVar(value="1777")
        self.mouse_2_id = tk.StringVar(value="1778")
        self.first_opponent_type = tk.StringVar(value = None)
        self.second_opponent_type = tk.StringVar(value = None)
        self.first_opponent_strategy = tk.StringVar(value=None)
        self.second_opponent_strategy = tk.StringVar(value=None)
        self.first_opponent_learning_strategy = tk.StringVar(value = None)
        self.second_opponent_learning_strategy = tk.StringVar(value = None)
        self.first_opponent_prob = tk.StringVar(value = None)
        self.second_opponent_prob = tk.StringVar(value = None)

        # Control Variables
        self.start_button_clicked = False

    def setup_gui(self):
        # Entry fields for trials, duration, etc.
        self.populate_system_parameters_panel()
        self.populate_experiment_panel()
        self.create_opponent_options(self.first_opponent_panel, self.first_opponent_type, "Mouse")
        self.create_opponent_options(self.second_opponent_panel, self.second_opponent_type, "Mouse")
        #self.create_opponent_options(self.second_opponent_panel, self.second_opponent_type, "Fixed Strategy")
        self.create_mouseid_field(self.first_opponent_panel, self.mouse_1_id)
        self.create_mouseid_field(self.second_opponent_panel, self.mouse_2_id)

        #self.create_strategy_option(self.first_opponent_panel, self.first_opponent_strategy, self.first_opponent_prob)
        #self.create_strategy_option(self.second_opponent_panel, self.second_opponent_strategy, self.second_opponent_prob)
        #self.create_strategy_option(self.first_opponent_panel, self.first_opponent_strategy, self.first_opponent_prob)
        #self.create_strategy_option(self.second_opponent_panel, self.second_opponent_strategy,self.second_opponent_prob)

        # Create a button to start the experiment
        start_button = tk.Button(self.window, text="Start Experiment", command=self.start_experiment)
        start_button.place(x = 225, y = 595)

        self.project_directory_var.set(fUtile.get_project_directory())
        self.window.mainloop()

    def populate_system_parameters_panel(self):
        tk.Label(self.system_panel, text="COM port name:").place(x = 130, y = 30)
        comport_name_entry = tk.Entry(self.system_panel, textvariable = self.comport_name)
        comport_name_entry.place(x = 230, y = 30)
        tk.Label(self.system_panel, text="Project Directory:").place(x = 5, y = 60)
        pd_name_entry = tk.Entry(self.system_panel, width = 60, textvariable = self.project_directory_var)
        pd_name_entry.place(x = 110, y = 60)
        pd_button = tk.Button(self.window, text="Browse", command=self.browse_project_directory)
        pd_button.place(x = 490, y = 60)

    def get_opponent_type(self,opponent_type_str):
        mapping = {
            "Mouse": OpponentType.MOUSE,
            "Fixed Strategy": OpponentType.FIXED_STRATEGY,
            "Learner": OpponentType.LEARNER
        }
        return mapping.get(opponent_type_str, None)

    def create_opponent_options(self, panel, opvar, default):
        tk.Label(panel, text="Opponent type:").place(x=5, y=25)
        opponent_types = ["Mouse", "Fixed Strategy", "Learner"]
        buttonoffset = [50, 105, 280]  # Adjusted offsets for proper alignment
        opvar.set(default)
        for type in opponent_types:
            radiobutton = tk.Radiobutton(panel, text=type, variable=opvar, value=type,
                                         command=self.update_opponent_options)  # Added command
            radiobutton.place(x=20, y=buttonoffset[opponent_types.index(type)])

    def create_mouseid_field(self, panel, mousevar):
        tk.Label(panel, text="Mouse ID:").place(x=50, y=75)
        mouse_id_entry = tk.Entry(panel, textvariable=mousevar)
        mouse_id_entry.place(x=120, y=75)

    def populate_experiment_panel(self):
        tk.Label(self.experiment_panel, text="Experiment Name:").place(x = 5, y = 30)
        experiment_name_entry = tk.Entry(self.experiment_panel, textvariable = self.experiment_name)
        experiment_name_entry.place(x = 130, y = 30)

        tk.Label(self.experiment_panel, text="Session Type:").place(x = 5, y = 60)
        st_entry = tk.Entry(self.experiment_panel, textvariable = self.session_type)
        st_entry.place(x = 130, y = 60)

        tk.Label(self.experiment_panel, text="Session Number:").place(x = 5, y = 90)
        sn_entry = tk.Entry(self.experiment_panel, textvariable = self.session_num)
        sn_entry.place(x = 130, y = 90)

        tk.Label(self.experiment_panel, text="Number of Trials:").place(x = 270, y = 30)
        self.num_trials_entry = tk.Entry(self.experiment_panel, textvariable=self.num_trials_var)
        self.num_trials_entry.place(x = 400, y = 30)

        tk.Label(self.experiment_panel, text="Decision Time (sec):").place(x = 270, y = 60)
        self.decision_time_entry = tk.Entry(self.experiment_panel, textvariable=self.decision_time_var)
        self.decision_time_entry.place(x = 400, y = 60)

        tk.Label(self.experiment_panel, text="Return Time (sec):").place(x = 270, y = 90)
        self.decision_time_entry = tk.Entry(self.experiment_panel, textvariable=self.return_time_var)
        self.decision_time_entry.place(x = 400, y = 90)

    def create_strategy_option(self, panel, opvar, probvar):
        # Define strategy options
        strategies = ["Unconditional Cooperator", "Unconditional Defector", "Random", "Tit for Tat",
                      "Probability p Cooperator"]
        opvar.set("Unconditional Cooperator")

        buttonoffset = 0
        for strategy in strategies:
            radiobutton = tk.Radiobutton(panel, text = strategy, variable = opvar, value = strategy)
            radiobutton.place(x = 50, y = 130 + buttonoffset * 25)
            buttonoffset += 1

        tk.Label(panel, text="Probability: ").place(x = 70, y = 260)
        probvar.set("0.1")
        probability_entry = tk.Entry(panel, textvariable = probvar)
        probability_entry.place(x = 150, y = 260, width = 50)

    def create_learner_option(self, panel, opvar):
        # Clear existing strategy options
        for widget in panel.winfo_children():
            if isinstance(widget, tk.Radiobutton) or isinstance(widget, tk.Label) and widget.cget(
                    "text") == "Probability: ":
                widget.destroy()

        # Define learner options
        learner_options = ["Q-Learning Agent", "Actor-Critic Agent", "Reinforce Agent"]
        opvar.set(learner_options[0])  # Set default selection

        tk.Label(panel, text="Learning Strategy:").place(x=50, y=130)
        for index, option in enumerate(learner_options):
            radiobutton = tk.Radiobutton(panel, text=option, variable=opvar, value=option)
            radiobutton.place(x=70, y=160 + index * 30)

    def update_opponent_options(self):
        # Assuming self.first_opponent_type and self.second_opponent_type are the variables for the opponent type
        self.update_sub_options(self.first_opponent_panel, self.first_opponent_type.get())
        self.update_sub_options(self.second_opponent_panel, self.second_opponent_type.get())

    def update_sub_options(self, panel, opponent_type):
        # Clear any existing sub-options first
        self.clear_sub_options(panel)

        # Based on the opponent type, show relevant sub-options
        if opponent_type == "Learner":
            self.create_learner_option(panel)
        elif opponent_type == "Fixed Strategy":
            self.create_fixed_strategy_option(panel)

    def clear_sub_options(self, panel):
        # This function will clear sub-options from the panel
        for widget in panel.winfo_children():
            if isinstance(widget, tk.Radiobutton) or isinstance(widget, tk.Label):
                if widget.cget("text") in ["Learning Strategy:", "Strategy:", "Probability: "]:
                    widget.destroy()

    def start_experiment(self):
        # Start the experiment only if input data is valid
        if self.validate_inputs():
            self.start_button_clicked = True
            messagebox.showinfo("Experiment Starting", "The experiment is now starting with the provided settings.")
            self.window.destroy()

    def validate_inputs(self):
        # comport name must be defined.
        if self.comport_name.get() == "":
            messagebox.showerror("Invalid Input", "COM port name must be defined")
            return False

        # Project directory must exist
        if not fUtile.set_project_directory(self.project_directory_var.get()):
            messagebox.showerror("Invalid Input", "Project Directory Does not Exist")
            return False

        # Experiment name must be defined and experiment directory must exist
        ed = self.experiment_name.get()
        if ed == "":
            messagebox.showerror("Invalid Input", "Experiment directory must be defined")
            return False
        if not fUtile.set_experiment_directory(ed):
            return False

        # if opponent1 is a mouse mouse_1_id must be defined and mouse directory must exist.
        # else mouse_1_id is set to "COMPUTER" and directory must exist.
        if self.get_opponent_type(self.first_opponent_type.get()) == OpponentType.MOUSE:
            mouse = self.mouse_1_id.get()
            if mouse == "":
                messagebox.showerror("Invalid Input", "First opponent is a mouse. Mouse ID must be defined")
                return False
            if not fUtile.set_mouse_directory(mouse):
                return False
        else:
            if not fUtile.set_mouse_directory("COMPUTER"):
                return False

        # if opponent2 is a mouse mouse_2_id must be defined
        if self.get_opponent_type(self.second_opponent_type.get()) == OpponentType.MOUSE:
            mouse = self.mouse_2_id.get()
            if mouse == "":
                messagebox.showerror("Invalid Input", "Second opponent is a mouse. Mouse ID must be defined")
                return False

        # Session type must be defined
        if self.session_type.get() == "":
            messagebox.showerror("Invalid Input", "Session type must be defined")
            return False

        # Session Num must be a positive integer
        try:
            num = int(self.session_num.get())
        except ValueError:
            num = -1
        if num <= 0:
            messagebox.showerror("Invalid Input", "Session Num must be a positive integer")
            return False

        # Trials Num must be a positive integer
        try:
            num = int(self.num_trials_var.get())
        except ValueError:
            num = -1
        if num <= 0:
            messagebox.showerror("Invalid Input", "Trials Number must be a positive integer")
            return False

        # Return Time must be a positive integer
        try:
            num = int(self.return_time_var.get())
        except ValueError:
            num = -1
        if num <= 0:
            messagebox.showerror("Invalid Input", "Return Time must be a positive integer")
            return False

        # Decision Time must be a positive integer
        try:
            num = int(self.decision_time_var.get())
        except ValueError:
            num = -1
        if num <= 0:
            messagebox.showerror("Invalid Input", "Decision Time must be a positive integer")
            return False

        return True

    def update_opponent_options(self):
        # Check for the first opponent panel
        if self.first_opponent_type.get() == "Learner":
            self.create_learner_option(self.first_opponent_panel, self.first_opponent_learning_strategy)
        else:
            # You might need to clear the learner options or recreate standard options here
            self.create_strategy_option(self.first_opponent_panel, self.first_opponent_strategy,
                                        self.first_opponent_prob)

        # Repeat for the second opponent panel
        if self.second_opponent_type.get() == "Learner":
            self.create_learner_option(self.second_opponent_panel, self.second_opponent_learning_strategy)
        else:
            # Similarly, clear the learner options or recreate standard options for the second panel
            self.create_strategy_option(self.second_opponent_panel, self.second_opponent_strategy,
                                        self.second_opponent_prob)

    def create_learner_option(self, panel, opvar):
        # Clear existing strategy options and probability field if they exist
        for widget in panel.winfo_children():
            widget.destroy()  # This removes all widgets, including labels and entries previously added




        # Define learner options
        learner_options = ["Q-Learning Agent", "Actor-Critic Agent", "Reinforce Agent"]
        opvar.set(learner_options[0])  # Set default selection

        tk.Label(panel, text="Learning Strategy:", anchor="w").place(x=50, y=100)
        for index, option in enumerate(learner_options):
            radiobutton = tk.Radiobutton(panel, text=option, variable=opvar, value=option)
            radiobutton.place(x=70, y=100 + 30 + (index * 30))  # Adjust y for each option

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
            'session_type': self.session_type.get(),
            'session_num': self.session_num.get()}
        print(settings)
        return settings

    def get_opponent_configuration(self):
        settings = {
            'opponent1_type': self.get_opponent_type(self.first_opponent_type.get()),
            'opponent2_type': self.get_opponent_type(self.second_opponent_type.get()),
            'opponent1_strategy': self.first_opponent_strategy.get(),
            'opponent2_strategy': self.second_opponent_strategy.get(),
            'opponent1_probability' : self.first_opponent_prob.get(),
            'opponent2_probability' : self.second_opponent_prob.get(),
            'mouse_1_id' : self.mouse_1_id.get(),
            'mouse_2_id' : self.mouse_2_id.get()}
        print(settings)
        return settings

    def browse_project_directory(self):
        directory_path = filedialog.askdirectory(title="Select a directory")
        if directory_path != "":
            self.project_directory_var.set(directory_path)



