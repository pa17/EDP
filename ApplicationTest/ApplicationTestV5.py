## IMPORTS

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, time, Adafruit_ADS1x15, argparse
import pyqtgraph as pg
from templateIter4 import Ui_SimpleButton

### SETUP
pg.setConfigOption('background', None)
adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance. Connect TMP to A0 and RV to A1
GAIN = 1
readValues = [0]*4

## VARIABLES
samplingfrequency = 120 # Hz
samplingperiod = 1000 / samplingfrequency # ms
zeroWindAdjustment =  0.2

global TimeList, WSList, Volume, VolList, TempList, ButtonFlag, tic, InExhales, Breaths, VolFlowList
ButtonFlag = ""
Volume = 0
dtList = []
WSList = []
VolFlowList = []
VolList = []
TempList = []
TimeList = []
InExhales = []
Breaths = [0.0]

## FUNCTIONS

def millis():
    return time.time() * 1000

def getValues():

    for i in range(4):
        readValues[i] = adc.read_adc(i, gain=GAIN)
        readValues[i] = readValues[i]*0.025568 # Values scaled to 10 bit so that Arduino code can be adapted

    TMP_Therm_ADunits = readValues[0] 
    RV_Wind_ADunits = readValues[1]
    RV_Wind_Volts = (RV_Wind_ADunits * 0.0048828125)
    TempCtimes100 = (0.005*TMP_Therm_ADunits*TMP_Therm_ADunits) - 16.862*TMP_Therm_ADunits + 9075.4
    zeroWind_ADunits = -0.0006*TMP_Therm_ADunits*TMP_Therm_ADunits + 1.0727*TMP_Therm_ADunits + 47.172
    zeroWind_Volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment

    if (RV_Wind_Volts >= zeroWind_Volts): 
        WindSpeed_MPH = pow((RV_Wind_Volts - zeroWind_Volts)/0.2300, 2.7265)
    else:
        WindSpeed_MPH = 0.0
        
    
    WindSpeed_MetresPerSecond = WindSpeed_MPH * 0.44704 * 4.2 #VER, Calibration Scaled
    BreathSpeed = WindSpeed_MetresPerSecond * 0.08260301783
    VolFlowRate = 0.5725552611 * BreathSpeed # In L/s
    print VolFlowRate
    ScalingFactor = -14.9732*VolFlowRate+1.6346
    print ScalingFactor
    VolFlowRate = ScalingFactor*VolFlowRate
    return VolFlowRate, BreathSpeed, (TempCtimes100/100)
    
def updatePlot():
    
    global TimeList, WSList, Volume, TempList, VolList, tic, InExhales, Breaths, VolFlowList

    VolFlowRead, WSRead, TempRead = getValues()
       
    toc = millis()
    dt = (toc-tic)/1000 
    Volume += dt*VolFlowRead
    tic = millis() # Measure time from here to toc again --> a complete cycle

    dtList.append(dt) 
    TempList.append(TempRead)
    VolFlowList.append(VolFlowRead)
    VolList.append(round(Volume,2)) # Round it to two dec. for determining breath
    WSList.append(WSRead)
    TimeList.append(sum(dtList))

    currVolume = VolList[-1] # Rounded to two decimals
    if VolList.count(currVolume) > 8 and currVolume not in InExhales:
        InExhales.append(currVolume)
    if len(InExhales) > 1:
        Breaths.append(InExhales[-1]-InExhales[-2])

print ("Application Test V5")

tic = millis()

### --> SETUP END

### UI LOOP

class CustomWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent=parent)
        
        # set up the form class as a `ui` attribute
        self.ui = Ui_SimpleButton()
        self.ui.setupUi(self)
      
        self.connect(self.ui.pushButton, SIGNAL("clicked()"), self.UpdateWSPlot)
        self.connect(self.ui.pushButton_2, SIGNAL("clicked()"), self.UpdateVolFlowPlot)
        self.connect(self.ui.pushButton_3, SIGNAL("clicked()"), self.UpdateVolPlot)
        
        # access your UI elements through the `ui` attribute
        self.ui.plotWidget.plot(TimeList, WSList, clear=True, title="Breath speed vs. time")

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
        global ButtonFlag, Breaths, WSList, VolFlowList, VolList
        updatePlot()
        self.ui.TVDisplay.setText(str(Breaths[-1]))
        self.ui.RVDisplay.setText(str(round(WSList[-1],2)))
        self.ui.ERVDisplay.setText(str(round(VolFlowList[-1],2)))
        self.ui.ICDisplay.setText(str(round(VolList[-1],2)))
      
        if ButtonFlag == "WS":
            self.ui.plotWidget.plot(TimeList, WSList, clear=True, title="Breath speed vs. time",pen='b')
            self.ui.plotWidget.setLabel('left', "Flow speed", units='m/s')
            self.ui.plotWidget.setLabel('bottom', "Time", units='s')

        elif ButtonFlag == "VolFlow":
            self.ui.plotWidget.plot(TimeList, VolFlowList, clear=True, title="Volumetric Flow Rate vs. time",pen='b')
            self.ui.plotWidget.setLabel('left', "Volumetric Flow Rate", units='L/s')
            self.ui.plotWidget.setLabel('bottom', "Time", units='s')
            
        elif ButtonFlag == "Vol":
            self.ui.plotWidget.plot(TimeList, VolList, clear=True, title="Volume vs. time",pen='b')
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
    app.setStyleSheet("Breeze {background: '#FFFFFF';}")
    widget.show()
    app.exec_()

### --> UI LOOP END
