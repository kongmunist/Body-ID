import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import copy
import glob
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
from collections import deque
import matplotlib.animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from utils import *

def conv(lst):
    a = [str(x) for x in lst]
    print("".join(a))

class GUI(QMainWindow):
    def __init__(self):
        # Initialize the main window
        super(GUI, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle("Body ID")
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.layout = QVBoxLayout(self._main)
        self.recording = False


        # Get the port from a Dialog menu
        self.data = deque(maxlen=1000)
        self.saveData = []
        self.connect()



        # init layout
        self.hbox = QVBoxLayout()
        self.layout.addLayout(self.hbox)

        # Add Save Button and data display
        display = QVBoxLayout()
        self.dataoutput = QLabel("AHHH")
        saveButton = QPushButton("Save Data") # bind function
        display.addWidget(self.dataoutput)
        display.addWidget(saveButton)
        saveButton.clicked.connect(self.changeText)
        self.hbox.addWidget(saveButton)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.horizontal = QHBoxLayout()
        self.layout.addLayout(self.horizontal)
        self.horizontal.addWidget(self.canvas)

        ax = self.figure.add_subplot(111)
        self.fftplot, = ax.plot([], [], lw=2)
        # ax.set_ylim(-1000, 2000) # Analog
        ax.set_ylim(-1, 2) # Digital
        ax.set_xlim(0, self.data.maxlen)
        ani = matplotlib.animation.FuncAnimation(self.figure, self.updatefig,
                                                 interval=1, blit=True,
                                                 repeat_delay=1)


        self.SerialSendPanel()


    def updatefig(self, *args):
        a = list(self.data)
        self.fftplot.set_data(list(range(len(a))),a)

        return self.fftplot,

    def SerialSendPanel(self):
        # Add Serial send options
        horz = QHBoxLayout()
        self.vert1 = QVBoxLayout()
        self.horiz1 = QHBoxLayout()
        self.textlabel1 = QRadioButton("Recording: Off")
        self.textlabel1.setEnabled(False)



        # self.textlabel1 = QLabel(
        #     "Recording: Off")  # Page 30 of the datasheet
        self.horiz1.addWidget(self.textlabel1)

        self.horiz2 = QHBoxLayout()
        self.textlabel2 = QLabel(
            "")  # Address
        self.horiz2.addWidget(self.textlabel2)

        self.horiz3 = QHBoxLayout()
        self.textlabel3 = QLabel("")  # Data
        self.horiz3.addWidget(self.textlabel3)

        self.horiz4 = QHBoxLayout()
        self.sendButton = QPushButton("Send") # Bind function
        self.horiz4.addWidget(self.sendButton)

        for thing in [self.horiz1, self.horiz2, self.horiz3, self.horiz4]:
            self.vert1.addLayout(thing)
        horz.addLayout(self.vert1)

        buttonholder = QVBoxLayout()
        send2deci = QPushButton("Decimate by two") # Bind function
        dontsend2deci = QPushButton("Undecimate by two") # Bind function
        sendoff = QPushButton("Turn off") # Bind function
        # buttonholder.addWidget(send2deci)
        # buttonholder.addWidget(dontsend2deci)
        # buttonholder.addWidget(sendoff)

        horz.addLayout(buttonholder)
        self.hbox.addLayout(horz)

        self.sendButton.clicked.connect(self.sendSerial)

    def sendSerial(self):
        self.serialThread.RTS = True

    def changeText(self):

        if self.serialThread.recording: # If we're already recording, turn off and save data
            self.saveData = copy.copy(self.serialThread.data)
            with open('output.csv', 'w+') as f:
                f.write(",".join([str(x) for x in self.saveData]))

            for i in range(100):
                self.textlabel1.setText("Recording: Off")
            print('set off')
        else:
            for i in range(100):
                self.textlabel1.setText("Recording: On")
            print('set on')
        self.processEvents()
        self.serialThread.recording = not self.serialThread.recording
        # print(self.serialThread.recording)
        self.serialThread.data = []



    def connect(self):
        connectDialog = Dialog()
        if connectDialog.exec_():
            self.selectedPort = connectDialog.dd.currentText()
            self.serialThread = SerialThread(self.selectedPort,self.data)
            self.serialThread.start()
            # self.active = True
            self.show()
        else:
            sys.exit()




class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        layout = QVBoxLayout()

        # Make dropdown
        dropdownChoices = glob.glob("/dev/tty.*")[::-1]
        self.dd = QComboBox()
        self.dd.addItems(dropdownChoices)
        self.formGroupBox = QGroupBox("")
        formbox = QFormLayout()
        formbox.addRow(QLabel("Available Ports"), self.dd)
        self.formGroupBox.setLayout(formbox)
        layout.addWidget(self.formGroupBox)

        # Create select and cancel button
        buttonHolder = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonHolder.accepted.connect(self.accept)
        buttonHolder.rejected.connect(self.reject)
        layout.addWidget(buttonHolder)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("Select COM Port")


def main():
   app = QApplication(sys.argv)
   ex = GUI()

   sys.exit(app.exec_())

if __name__ == '__main__':
   main()