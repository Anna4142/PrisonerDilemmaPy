import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class RunTimeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Prisoner's Dilemma")
        self.window.geometry("800x700")
        self.window.bind("<MouseWheel>", self.onMouseWheel)

        tk.Label(self.window, text='Time:', font=("Arial", 48)).place(x=50, y=10)
        self.timeDisplay = tk.Label(self.window, text="00:00", font=("Arial", 48))
        self.timeDisplay.place(x=240, y=10)
        tk.Label(self.window, text='Trial:', font=("Arial", 48)).place(x=490, y=10)
        self.trialDisplay = tk.Label(self.window, text="0", font=("Arial", 48))
        self.trialDisplay.place(x=670, y=10)
        self.mainLoopCallback = None
        tk.Label(self.window, text='Decision history:', font=("Arial", 12)).place(x=120, y=120)
        tk.Label(self.window, text='Green = Cooperate.', foreground='green', font=("Arial", 12)).place(x=250, y=120)
        tk.Label(self.window, text='Red = Defect.', foreground='red', font=("Arial", 12)).place(x=400, y=120)
        tk.Label(self.window, text='Mouse 1', font=("Arial", 8)).place(x=30, y=153)
        tk.Label(self.window, text='Mouse 2', font=("Arial", 8)).place(x=30, y=168)
        tk.Label(self.window, text='Timeout history:', font=("Arial", 12)).place(x=120, y=200)
        tk.Label(self.window, text='M1 Center', font=("Arial", 8)).place(x=30, y=233)
        tk.Label(self.window, text='M1 Decision', font=("Arial", 8)).place(x=30, y=248)
        tk.Label(self.window, text='M2 Center', font=("Arial", 8)).place(x=30, y=262)
        tk.Label(self.window, text='M2 Decision', font=("Arial", 8)).place(x=30, y=276)
        self.DPanel = tk.Frame(self.window, width=600, height=50)
        self.DPanel.place(x=100, y=145)
        self.TPanel = tk.Frame(self.window, width=600, height=80)
        self.TPanel.place(x=100, y=225)
        self.DCanvas = tk.Canvas(self.DPanel, width=590, height=40)
        self.DCanvas.place(x=0, y=2)
        self.TCanvas = tk.Canvas(self.TPanel, width=590, height=70)
        self.TCanvas.place(x=0, y=2)
        self.drawTrialSummeryGrid(0)
        self.stop_button = tk.Button(self.window, text="Stop Experiment")
        self.stop_button.place(x = 300, y = 600)
        self.stop_button.config(font=("Arial", 12))

        self.scrollOffset = 0

    def StartMonitoring(self, loopcallback, stopcallback):
        self.mainLoopCallback = loopcallback
        self.stop_button.config(font=("Arial", 12))
        self.stop_button.config(command=stopcallback)
        self.timeDisplay.after(10, self.timerEvent)
        self.window.mainloop()

    def UpdateTrialDisplay(self, trial):
        self.trialDisplay.config(text = f'{trial:02d}')
        if trial % 10 == 0:
            extentionfactor = trial // 10
            self.DCanvas.config(width=590 * (extentionfactor + 1) , height=40)
            self.TCanvas.config(width=590 * (extentionfactor + 1), height=70)
            self.drawTrialSummeryGrid(extentionfactor)

    def UpdateTimeDisplay(self, time):
        minutes = int(time / 60)
        seconds = int(time) % 60
        self.timeDisplay.config(text = f'{minutes:02d}:{seconds:02d}')

    def timerEvent(self):
        if self.mainLoopCallback():
            self.window.destroy()
        else:
            self.timeDisplay.after(10, self.timerEvent)

    def drawTrialSummeryGrid(self, extentionfactor):
        x0 = 5 + extentionfactor * 560
        x1 = 565 + extentionfactor * 560
        for y in range(10, 39, 14):
            self.DCanvas.create_line(x0, y, x1, y, fill="red", width=2)
        for y in range(10, 67, 14):
            self.TCanvas.create_line(x0, y, x1, y, fill="red", width=2)
        for x in range(x0, x1 + 1, 14):
            self.DCanvas.create_line(x, 10, x, 38, fill="red", width=2)
            self.TCanvas.create_line(x, 10, x, 67, fill="red", width=2)

    def updateDecisionHistory(self, trial, mouse, decision):
        if trial == 20:
            self.DCanvas.place(x=-50, y=2)
        if decision == 'C':
            color = 'green'
        else:
            color = 'red'
        self.drawCanvasRectangle(self.DCanvas, mouse, trial, color)

    def updateTimeoutHistory(self, trial, mouse, center, decision):
        if center:
            self.drawCanvasRectangle(self.TCanvas, 1 + (mouse - 1) * 2, trial, 'black')
        if decision:
            self.drawCanvasRectangle(self.TCanvas, 2 + (mouse - 1) * 2, trial, 'black')

    def drawCanvasRectangle(self, canvas, line, trial, color):
        # Define base coordinates for the trial markers
        x0, y0 = 7, 12
        squaresize = 9
        squareOfsset = 14
        x = x0 + squareOfsset * (trial - 1)
        y = y0 + squareOfsset * (line - 1)
        canvas.create_rectangle(x, y, x + squaresize, y + squaresize, fill=color)

    # Function to handle mouse wheel event
    def onMouseWheel(self, event):
        # Determine the direction of the scroll (up or down) and move the canvases
        if event.delta < 0:
            self.scrollOffset -= 1
        else:
            self.scrollOffset += 1
            if self.scrollOffset > 0:
                self.scrollOffset = 0
        delatX = 72 * self.scrollOffset
        self.DCanvas.place(x=delatX, y=2)
        self.TCanvas.place(x=delatX, y=2)

