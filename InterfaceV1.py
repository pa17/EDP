## IMPORTS

from PyQt4 import QtCore, QtGui # PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import pyqtgraph as pg # Pyqtgraph
import time # Import time
import Adafruit_ADS1x15 # Import the ADS1x15 module.
adc = Adafruit_ADS1x15.ADS1115() # Create an ADS1115 ADC (16-bit) instance. Connect TMP to A0 and RV to A1
import MainPage, EditPatient, WelcomePage # Import UI files

## FUNCTIONS

def millis():
    return time.time() * 1000

def getValues():
    # Needed to initialise outside of function to zero otherwise keeps reseting itself
        
    # ADC readings
    for i in range(4):
        readValues[i] = adc.read_adc(i, gain=GAIN)
        readValues[i] = readValues[i]*0.025568 # Values scaled to 10 bit so that Arduino code can be adapted

    # Temp reading / RV reading
    TMP_Therm_ADunits = readValues[0]
    RV_Wind_ADunits = readValues[1]
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
    global Volume
    # Get values from sensor
    VolFlowRead, WSRead, TempRead = getValues()
    # Integrate to find volume
    #toc = millis()
    #dt = (toc-tic)/1000 # Time increment in seconds
    Volume += samplingperiod*VolFlowRead
    #tic = millis() # Measure time from here to toc again --> a complete cycle
    # Append to plot lists
    dtList.append(samplingperiod)
    TempList.append(TempRead)
    VolFlowList.append(VolFlowRead*1000) # CONVERSION: m^3/s to L/s
    VolList.append(Volume) 
    WSList.append(WSRead)
    # Sums of dt is time
    TimeList.append(sum(dtList))

    # Important variables to return
    currVolume = VolList[-1]
    currVolFlow = VolFlowList[-1]
    currWS = WSList[-1]

    # Wind speed plot
    WindSpeedPlot.plot(TimeList, WSList, clear=True, title="Breath speed vs. time")
    WindSpeedPlot.setLabel('left', "Flow speed", units='m/s')
    WindSpeedPlot.setLabel('bottom', "Time", units='s')

    # Volume plot
    VolumePlot.plot(TimeList, VolList, clear=True, title="Volume vs. time")
    VolumePlot.setLabel('left', "Volume", units='m^3')
    VolumePlot.setLabel('bottom', "Time", units='s')

    #  Vol. flow rate plot
    VolFlowPlot.plot(TimeList, VolFlowList, clear=True, title="Volume vs. time")
    VolFlowPlot.setLabel('left', "Volumetric flow rate", units='L/s')
    VolFlowPlot.setLabel('bottom', "Time", units='s')

    pg.QtGui.QApplication.processEvents()
    
    MainPage.Graph_2.insertTab(0, WindSpeedPlot)
    
    return WindSpeedPlot, VolumePlot, VolFlowPlot

### SETUP

# Gain for ADC
GAIN = 1

## VARIABLES
samplingfrequency = 240 # Hz
samplingperiod = 1000 / samplingfrequency # In milliseconds
zeroWindAdjustment =  0.2 # Negative numbers yield smaller wind speeds and vice versa.
TMP_Therm_ADunits = 0    # Temp termistor value from wind sensor
RV_Wind_ADunits = 0.0    # RV output from wind sensor 
RV_Wind_Volts = 0.0
TempCtimes100 = 0
zeroWind_ADunits = 0.0
zeroWind_Volts = 0.0
WindSpeed_MPH = 0.0
WindSpeed_MetresPerSecond = 0.0
VolFlowRate = 0.0
global lastMillis
lastMillis = 0.0
global Volume
Volume = 0

# Initialise lists for subequent plotting
dtList = []
WSList = []
VolFlowList = []
VolList = []
TempList = []
TimeList = []

# Read all the ADC channel values in a list.
readValues = [0]*4

print ("Interface V1")

### --> SETUP END

### UI SETUP

tic = millis() # Need one tic to start with

WindSpeedPlot = pg.plot()
VolumePlot = pg.plot()
VolFlowPlot = pg.plot()

timer = QTimer()
timer.timeout.connect(updatePlot)
timer.start(samplingperiod)

class MainPage(QWidget, MainPage.Ui_SimpleButton):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.setupUi(self)
        
app = QApplication(sys.argv)
form = MainPage()
form.setFocus()
form.setWindowTitle("Main Page")
form.show()
app.exec_()

### --> UI SETUP END 

