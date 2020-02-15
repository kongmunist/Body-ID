# Basic Animation Framework

from tkinter import *
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import glob
from collections import deque
from utils import *

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

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    pass

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):
    # draw in canvas
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

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

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))

    data.data = deque(maxlen=1000)
    data.saveData = []
    connect(data)


    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")



run(400, 200)
