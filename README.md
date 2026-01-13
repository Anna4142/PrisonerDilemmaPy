# Prisoner's Dilemma Experiment System

A comprehensive experimental framework for conducting Prisoner's Dilemma experiments with mice, featuring real-time video tracking, automated reward delivery, and support for both biological and simulated learning agents.

## Overview

This system enables researchers to conduct behavioral experiments where two mice (or simulated agents) engage in repeated Prisoner's Dilemma games. The system tracks mouse positions in real-time using computer vision, delivers rewards based on their choices, and logs all experimental data for analysis.

## Features

- **Real-time Video Tracking**: Monitors mouse positions using Vimba-compatible cameras
- **Automated Reward Delivery**: Controls Arduino-based valve system for precise reward timing
- **Multiple Opponent Types**: 
  - Real mice (tracked via video)
  - Fixed strategy opponents (Cooperator, Defector, Tit-for-Tat, Probability Cooperator)
  - Reinforcement learning agents (Q-learning, REINFORCE, Actor-Critic)
- **State Machine Management**: Handles complex experiment flow with timeout controls
- **Comprehensive Data Logging**: Records trials, events, and state transitions
- **GUI Interface**: User-friendly setup and real-time monitoring
- **Data Analysis Tools**: Post-experiment analysis and visualization capabilities

## Project Structure

```
PrisonerDilemmaPy/
├── Arduino_related_code/          # Arduino communication and valve control
│   ├── ArduinoDigital.py          # Real Arduino interface
│   ├── ArduinoDigitalSim.py       # Simulated Arduino for testing
│   └── ValveControl.py            # Valve control logic
│
├── Data_analysis/                 # Logging and analysis tools
│   ├── logger.py                  # Trial data logging
│   ├── event_logger.py            # Event-level logging
│   ├── DataAnalysisScript.py      # Post-experiment analysis
│   └── RunTimeAnalysis.py         # Real-time performance monitoring
│
├── Experiment_Launcher_code/      # Main experiment control
│   ├── ExperimentLauncher.py      # Entry point
│   ├── ExperimentManager.py       # Core experiment logic
│   ├── experimentgui.py           # Setup GUI
│   └── RunTimeGui.py              # Runtime monitoring GUI
│
├── Video_analyser_code/            # Computer vision components
│   ├── VideoAnalyser.py           # Real camera interface
│   ├── VideoAnalyzerSim.py        # Simulated video for testing
│   └── ConfigureDetectionRegions.py # ROI configuration
│
├── State_manager_code/             # State machine
│   └── StateManager.py            # Experiment state transitions
│
├── Reward_manager/                 # Reward delivery system
│   └── RewardManager.py           # Reward timing and delivery
│
├── Sound_manager_code/             # Audio feedback
│   └── SoundManager.py            # Sound cues for trials
│
├── modelling_opponent/             # Opponent implementations
│   ├── MouseMonitor.py            # Real mouse tracking
│   ├── FixedStrategyPrisoner.py   # Fixed strategy opponents
│   └── Simulated_learner.py       # Learning agent wrapper
│
├── models/Learning_agents/         # Reinforcement learning agents
│   ├── QlearningAgent.py         # Deep Q-Network implementation
│   ├── ReinforceAgent.py          # REINFORCE algorithm
│   └── ActorCriticAgent.py        # Actor-Critic implementation
│
└── Ground_Truth_Data/              # Reference data for validation
    └── StrategyData/              # Pre-recorded strategy data
```

## Requirements

### Hardware
- Vimba-compatible camera (e.g., Allied Vision cameras)
- Arduino board with digital I/O for valve control
- 6-channel valve system for reward delivery
- Windows-compatible system (for Vimba SDK)

### Software Dependencies
- Python 3.7+
- PyTorch (for learning agents)
- OpenCV (cv2)
- vmbpy (Vimba Python SDK)
- tkinter (GUI framework)
- pyserial (for Arduino communication)
- numpy

### Installation

1. Install Python dependencies:
```bash
pip install torch torchvision
pip install opencv-python
pip install numpy
pip install pyserial
```

2. Install Vimba SDK:
   - Download and install the Vimba SDK from Allied Vision
   - Install the vmbpy Python package (usually included with SDK)

3. Configure Arduino:
   - Upload `Arduino_related_code/ValveControlAr/ValveControlAr.ino` to your Arduino
   - Connect valves to digital pins 0-5 (channels 7-12 in software)

## Configuration

### Module Configuration
Edit `Experiment_Launcher_code/ModuleConfiguration.py` to set simulation modes:

```python
__USE_VIDEO_SIM = False      # Set True to use simulated video (no camera needed)
__USE_ARDUINO_SIM = False    # Set True to use simulated Arduino (no hardware needed)
__FRAME_RATE_ONLY = True     # Frame rate monitoring mode
```

### Detection Regions
Configure mouse detection regions in `Video_analyser_code/VideoAnalyser.py`:
- Mouse 1 zones: Cooperate, Center, Defect (left side)
- Mouse 2 zones: Cooperate, Center, Defect (right side)
- Experimenter zone: For manual experiment start

## Usage

### Starting an Experiment

1. Run the main launcher:
```bash
cd PrisonerDilemmaPy
python Experiment_Launcher_code/ExperimentLauncher.py
```

2. Configure experiment parameters in the GUI:
   - **System Parameters**: COM port for Arduino, project directory
   - **Experiment Parameters**: 
     - Experiment name
     - Session type and number
     - Termination condition (trials or minutes)
     - Decision time limit
     - Return time limit
   - **Opponent Configuration**: 
     - Choose opponent type (Mouse, Fixed Strategy, or Learner)
     - For fixed strategies: select strategy type
     - For learners: select learning algorithm

3. Click "Start Experiment" to begin

### Experiment Flow

1. **Start State**: System initializes
2. **Center Reward**: Both mice receive center reward
3. **Trial Started**: Decision period begins
4. **Decision States**: 
   - M1CM2C: Both cooperate
   - M1CM2D: Mouse 1 cooperates, Mouse 2 defects
   - M1DM2C: Mouse 1 defects, Mouse 2 cooperates
   - M1DM2D: Both defect
5. **Trial Completed**: Return period begins
6. **Return States**: Mice return to center for next trial
7. **End State**: Experiment terminates

### Reward Structure

- **Mutual Cooperation (CC)**: 0.012 units each
- **Temptation (DC)**: 0.016 units for defector, 0 for cooperator
- **Mutual Defection (DD)**: 0.003 units each
- **Center Reward**: 0.002 units (for returning to center)

## Data Output

The system generates several data files:

- **Trial Logs**: `*_trial_log_mouse1.csv` and `*_trial_log_mouse2.csv`
  - Trial number, status, choices, rewards, decision times, return times
  
- **Event Logs**: `*_event_log_mouse1.csv` and `*_event_log_mouse2.csv`
  - Detailed event-level data (state transitions, location changes)
  
- **Video Recording**: `*_video.avi`
  - Complete video recording of the experiment
  
- **Configuration File**: `*_configuration.txt`
  - Experiment parameters and opponent settings

## Learning Agents

### Q-Learning Agent
- Deep Q-Network (DQN) implementation
- Replay buffer for experience storage
- Epsilon-greedy exploration

### REINFORCE Agent
- Policy gradient method
- Monte Carlo updates

### Actor-Critic Agent
- Combines value function and policy learning
- Lower variance than REINFORCE

## Testing and Simulation

The system includes simulation modes for testing without hardware:

- **Video Simulation**: Use `VideoAnalyzerSim` instead of real camera
- **Arduino Simulation**: Use `ArduinoDigitalSim` instead of real hardware

Enable these in `ModuleConfiguration.py` for development and testing.

## Troubleshooting

### Camera Issues
- Ensure Vimba SDK is properly installed
- Check camera connection and permissions
- Verify camera is detected: `python -c "from vmbpy import *; print(VmbSystem.get_instance().get_all_cameras())"`

### Arduino Communication
- Verify COM port number in GUI matches your system
- Check Arduino is powered and connected
- Test with `Arduino_related_code/ArduinoTest.py`

### Valve Control
- Calibrate valve timing using `ValveCaliberationTest.py`
- Verify valve wiring matches channel assignments in `RewardManager.py`

## Development

### Adding New Opponent Types
1. Create a class inheriting from `PrisonerABC` in `modelling_opponent/`
2. Implement `getDecision()` and `NewTrial()` methods
3. Add opponent type to `OpponentType` enum
4. Update `ExperimentLauncher.py` to instantiate new type

### Adding New Learning Algorithms
1. Create agent class in `models/Learning_agents/`
2. Implement decision-making interface compatible with `PrisonerABC`
3. Add to GUI options in `experimentgui.py`



[Add acknowledgments if applicable]

