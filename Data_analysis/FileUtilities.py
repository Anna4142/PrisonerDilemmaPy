import os
from tkinter import messagebox
from enum import Enum
from datetime import datetime

class FileType(Enum):
    EXPERIMENT_CONFIGURATION    = 1
    EXPERIMENT_LOG              = 2
    VIDEO_CAPTURE               = 3
    DATA_ANALYSIS               = 4
    EXPERIMENT_EVENT_LOG        = 5
    MOUSE_PROFILE               = 6
    COMPARISON_EVENT_LOG        = 7
    DATA_ANALYSIS_PLOTS         = 8



project_directory = ""
experiment_directory = ""
mouse_directory = ""
file_name = ""


def get_mouse_sub_directory(filetype):
    mapping = {
        FileType.EXPERIMENT_CONFIGURATION:  "/trial_configuration",
        FileType.EXPERIMENT_LOG:            "/data_from_trials",
        FileType.VIDEO_CAPTURE:             "/video_captures",
        FileType.EXPERIMENT_EVENT_LOG:      "/event_data_from_trials",
        FileType.DATA_ANALYSIS:             "/data_analysis",
        FileType.COMPARISON_EVENT_LOG:      "/comparison_event_data",
        FileType.DATA_ANALYSIS_PLOTS:       "/data_analysis_plots"
    }
    return mapping.get(filetype)


def set_project_directory(path):
    global project_directory
    if os.path.exists(path) and os.path.isdir(path):
        project_directory = path
        with open("./ProjectDirectory.txt", 'w') as file:
            file.write(f'{project_directory}')
        return True
    else:
        return False


def get_project_directory():
    try:
        with open("./ProjectDirectory.txt", 'r') as file:
            path = file.read()
    except FileNotFoundError:
        path = ""
    return path


def set_experiment_directory(path):
    global experiment_directory, project_directory
    experiment_path = project_directory + "/" + path
    if os.path.exists(experiment_path) and os.path.isdir(experiment_path):
        experiment_directory = experiment_path
        return True
    else:
        result = messagebox.askquestion("Directory Warning", "Experiment directory does not exist. Create?", icon='warning')
        if result == "yes":
            experiment_directory = experiment_path
            os.makedirs(experiment_directory)
            return True
        else:
            return False


def set_mouse_directory(mouse):
    global experiment_directory, mouse_directory
    if mouse == 'COMPUTER':
        prefix = ''
    else:
        prefix = 'Mouse'
    mouse_path = f'{experiment_directory}/{prefix}{mouse}'
    if os.path.exists(mouse_path) and os.path.isdir(mouse_path):
        mouse_directory = mouse_path
        return True
    else:
        result = messagebox.askquestion("Directory Warning", "Mouse directory does not exist. Create?", icon='warning')
        if result == "yes":
            mouse_directory = mouse_path
            os.makedirs(mouse_directory)
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.EXPERIMENT_CONFIGURATION))
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.EXPERIMENT_LOG))
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.VIDEO_CAPTURE))
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.EXPERIMENT_EVENT_LOG))
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.DATA_ANALYSIS))
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.COMPARISON_EVENT_LOG))
            os.makedirs(mouse_directory + "/" + get_mouse_sub_directory(FileType.DATA_ANALYSIS_PLOTS))

            return True
        else:
            return False


def set_file_name(sessiontype, sessionnum):
    global file_name
    current_datetime = datetime.now()
    datetime_string = current_datetime.strftime("%Y%m%d-%H%M%S")
    splitindex = mouse_directory.rfind('/')
    mouseid = mouse_directory[splitindex + 1 : ]
    experiment = mouse_directory[:splitindex]
    splitindex = experiment.rfind('/')
    experiment = experiment[splitindex + 1 : ]
    file_name = f'{datetime_string}_{experiment}_{mouseid}_{sessiontype}{sessionnum}'


def get_file_path(filetype):
    global mouse_directory, file_name
    subdir = get_mouse_sub_directory(filetype)

    if filetype == FileType.DATA_ANALYSIS_PLOTS:
        # For DATA_ANALYSIS_PLOTS, return the directory path without setting a specific file name.
        # You might want to adjust this if you have a specific naming convention for plots.
        return f'{mouse_directory}{subdir}/'
    elif filetype in [FileType.DATA_ANALYSIS, FileType.MOUSE_PROFILE]:
        # For DATA_ANALYSIS and MOUSE_PROFILE, return the mouse_directory directly.
        return mouse_directory
    else:
        # For other file types, return the full path including the directory and the file name.
        return f'{mouse_directory}{subdir}/{file_name}'
