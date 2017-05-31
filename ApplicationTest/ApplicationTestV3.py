## IMPORTS

from PyQt4 import QtCore, QtGui # PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import pyqtgraph as pg # Pyqtgraph
import time # Import time
import Adafruit_ADS1x15 # Import the ADS1x15 module.
import argparse
# import the "form class" from your compiled UI
from templateIter3 import Ui_SimpleButton

### SETUP

## ADC 
adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance. Connect TMP to A0 and RV to A1
# Gain for ADC
GAIN = 1
# Read all the ADC channel values in a list.
readValues = [0]*4

## VARIABLES
samplingfrequency = 120 # Hz
samplingperiod = 1000 / samplingfrequency # In milliseconds
zeroWindAdjustment =  0.2 # Negative numbers yield smaller wind speeds and vice versa.
# Initialise lists for subequent plotting
global TimeList, WSList, Volume, VolList, TempList, ButtonFlag, tic
ButtonFlag = ""
Volume = 0
dtList = []
WSList = []
VolFlowList = []
VolList = []
TempList = []
TimeList = []
tic = 0

## FUNCTIONS

def millis():
    return time.time() * 1000

def getValues():
      
    # ADC readings
    for i in range(4):
        readValues[i] = adc.read_adc(i, gain=GAIN)
        readValues[i] = readValues[i]*0.025568 # Values scaled to 10 bit so that Arduino code can be adapted

    # Temp reading / RV reading
    TMP_Therm_ADunits = readValues[0] # Temp termistor value from wind sensor
    RV_Wind_ADunits = readValues[1] # RV output from wind sensor 
    RV_Wind_Volts = (RV_Wind_ADunits * 0.0048828125)
    # Calculate temperature
    TempCtimes100 = (0.005*TMP_Therm_ADunits*TMP_Therm_ADunits) - 16.862*TMP_Therm_ADunits + 9075.4
    # Calculate zero wind
    zeroWind_ADunits = -0.0006*TMP_Therm_ADunits*TMP_Therm_ADunits + 1.0727*TMP_Therm_ADunits + 47.172
    # Zero wind adjustment
    zeroWind_Volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment

    # Wind speed in MPH
    if (RV_Wind_Volts >= zeroWind_Volts): # Otherwise wind speed must be zero
        WindSpeed_MPH = pow((RV_Wind_Volts - zeroWind_Volts)/0.2300, 2.7265)
    else:
        WindSpeed_MPH = 0.0

    WindSpeed_MetresPerSecond = WindSpeed_MPH * 0.44704
    VolFlowRate = 6.931 * WindSpeed_MetresPerSecond
    
    return VolFlowRate, WindSpeed_MetresPerSecond, (TempCtimes100/100)
    
def updatePlot():
    
    global TimeList, WSList, Volume, TempList, VolList, tic
    # Get values from sensor
    VolFlowRead, WSRead, TempRead = getValues()
    # Integrate to find volume
    toc = millis()
    Volume += (tic-toc)*VolFlowRead
    tic = millis()
    dt = tic - toc
    # Append to plot lists
    dtList.append(dt) 
    TempList.append(TempRead)
    VolFlowList.append(VolFlowRead*1000) # CONVERSION: m^3/s to L/s
    VolList.append(Volume) 
    WSList.append(WSRead)
    # Sums of dt is time
    TimeList.append(sum(dtList))

    # Important variables to return
    #currVolume = VolList[-1]
    #currVolFlow = VolFlowList[-1]
    #currWS = WSList[-1]
    
    #return WSList, TimeList, TempList, VolList
    
    #QtGui.QApplication.processEvents()

print ("Application Test V3")

### --> SETUP END

### UI LOOP

class CustomWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent=parent)
        
        # set up the form class as a `ui` attribute
        self.ui = Ui_SimpleButton()
        self.ui.setupUi(self)
      
        # Connect to buttons
        self.connect(self.ui.pushButton, SIGNAL("clicked()"), self.UpdateWSPlot)
        self.connect(self.ui.pushButton_2, SIGNAL("clicked()"), self.UpdateVolFlowPlot)
        self.connect(self.ui.pushButton_3, SIGNAL("clicked()"), self.UpdateVolPlot)
        
        # access your UI elements through the `ui` attribute
        self.ui.plotWidget.plot(TimeList, WSList, clear=True, title="Breath speed vs. time")

        # simple demonstration of pure Qt widgets interacting with pyqtgraph
        self.ui.checkBox.stateChanged.connect(self.toggleMouse)
        self.timer = QTimer()
        self.timer.timeout.connect(self.ClassUpdatePlot)
        self.timer.start(samplingperiod)

    def toggleMouse(self, state):
        if state == QtCore.Qt.Checked:
            enabled = True
        else:
            enabled = False
            
    def ClassUpdatePlot(self):
        global ButtonFlag
        updatePlot()
      
        if ButtonFlag == "WS":
            self.ui.plotWidget.plot(TimeList, WSList, clear=True, title="Breath speed vs. time")
            self.ui.plotWidget.setLabel('left', "Flow speed", units='m/s')
            self.ui.plotWidget.setLabel('bottom', "Time", units='s')

        elif ButtonFlag == "VolFlow":
            self.ui.plotWidget.plot(TimeList, VolFlowList, clear=True, title="Volumetric Flow Rate vs. time")
            self.ui.plotWidget.setLabel('left', "Volumetric Flow Rate", units='L/s')
            self.ui.plotWidget.setLabel('bottom', "Time", units='s')
            
        elif ButtonFlag == "Vol":
            self.ui.plotWidget.plot(TimeList, VolList, clear=True, title="Volume vs. time")
            self.ui.plotWidget.setLabel('left', "Volume", units='L')
            self.ui.plotWidget.setLabel('bottom', "Time", units='s')
            
    def UpdateWSPlot(self):
        global ButtonFlag
        ButtonFlag = "WS"
      
    def UpdateVolFlowPlot(self):
        global ButtonFlag
        ButtonFlag = "VolFlow"
      
    def UpdateVolPlot(self):
        global ButtonFlag
        ButtonFlag = "Vol"


if __name__ == '__main__':

    app = QtGui.QApplication([])
    widget = CustomWidget()

    widget.show()
    app.exec_()

### --> UI LOOP END
