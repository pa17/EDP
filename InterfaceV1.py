## IMPORTS

# PyQt4
from PyQt4 import QtCore, QtGui
# Pyqtgraph
import pyqtgraph as pg
# Import time
import time
# Import the ADS1x15 module.
import Adafruit_ADS1x15
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
# Connect TMP to A0 and RV to A1

## FUNCTIONS

def millis():
    return time.time() * 1000

def getValues():
    # Needed to initialise outside of function to zero otherwise keeps reseting itself
    global lastMillis
    
    if ((millis() - lastMillis) > samplingperiod):
        
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
    
    # Calculate how much time has passed since last sample
    lastMillis = millis()
    
    return VolFlowRate, WindSpeed_MetresPerSecond, (TempCtimes100/100)
    

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

print ("Integration V3")

### --> SETUP END

### UI SETUP

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SimpleButton(object):
    def setupUi(self, SimpleButton):
        SimpleButton.setObjectName(_fromUtf8("SimpleButton"))
        SimpleButton.resize(858, 701)
        self.verticalLayoutWidget_2 = QtGui.QWidget(SimpleButton)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(720, 410, 121, 151))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.CalibrateButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.CalibrateButton.setObjectName(_fromUtf8("CalibrateButton"))
        self.verticalLayout_2.addWidget(self.CalibrateButton)
        self.StartButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.StartButton.setObjectName(_fromUtf8("StartButton"))
        self.verticalLayout_2.addWidget(self.StartButton)
        self.StopButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.StopButton.setObjectName(_fromUtf8("StopButton"))
        self.verticalLayout_2.addWidget(self.StopButton)
        self.CancelButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.CancelButton.setObjectName(_fromUtf8("CancelButton"))
        self.verticalLayout_2.addWidget(self.CancelButton)
        self.BREEZETitle = QtGui.QLabel(SimpleButton)
        self.BREEZETitle.setGeometry(QtCore.QRect(340, 0, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.BREEZETitle.setFont(font)
        self.BREEZETitle.setObjectName(_fromUtf8("BREEZETitle"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(SimpleButton)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(70, 70, 721, 84))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.horizontalLayoutWidget_2.setFont(font)
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.PatientIDLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.PatientIDLabel.setFont(font)
        self.PatientIDLabel.setObjectName(_fromUtf8("PatientIDLabel"))
        self.verticalLayout_5.addWidget(self.PatientIDLabel)
        self.FirstNameLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FirstNameLabel.setFont(font)
        self.FirstNameLabel.setObjectName(_fromUtf8("FirstNameLabel"))
        self.verticalLayout_5.addWidget(self.FirstNameLabel)
        self.LastNameLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.LastNameLabel.setFont(font)
        self.LastNameLabel.setObjectName(_fromUtf8("LastNameLabel"))
        self.verticalLayout_5.addWidget(self.LastNameLabel)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.PatientIDDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.PatientIDDisplay.setObjectName(_fromUtf8("PatientIDDisplay"))
        self.verticalLayout_7.addWidget(self.PatientIDDisplay)
        self.FirstNameDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.FirstNameDisplay.setObjectName(_fromUtf8("FirstNameDisplay"))
        self.verticalLayout_7.addWidget(self.FirstNameDisplay)
        self.LastNameDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.LastNameDisplay.setObjectName(_fromUtf8("LastNameDisplay"))
        self.verticalLayout_7.addWidget(self.LastNameDisplay)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.GenderLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.GenderLabel.setFont(font)
        self.GenderLabel.setObjectName(_fromUtf8("GenderLabel"))
        self.verticalLayout_6.addWidget(self.GenderLabel)
        self.WeightLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.WeightLabel.setFont(font)
        self.WeightLabel.setObjectName(_fromUtf8("WeightLabel"))
        self.verticalLayout_6.addWidget(self.WeightLabel)
        self.HeightLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.HeightLabel.setFont(font)
        self.HeightLabel.setObjectName(_fromUtf8("HeightLabel"))
        self.verticalLayout_6.addWidget(self.HeightLabel)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.GenderDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.GenderDisplay.setObjectName(_fromUtf8("GenderDisplay"))
        self.verticalLayout_8.addWidget(self.GenderDisplay)
        self.WeightDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.WeightDisplay.setObjectName(_fromUtf8("WeightDisplay"))
        self.verticalLayout_8.addWidget(self.WeightDisplay)
        self.HeightDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.HeightDisplay.setObjectName(_fromUtf8("HeightDisplay"))
        self.verticalLayout_8.addWidget(self.HeightDisplay)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.DOBLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.DOBLabel.setFont(font)
        self.DOBLabel.setObjectName(_fromUtf8("DOBLabel"))
        self.verticalLayout.addWidget(self.DOBLabel)
        self.EthnicGroupLabel = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.EthnicGroupLabel.setFont(font)
        self.EthnicGroupLabel.setObjectName(_fromUtf8("EthnicGroupLabel"))
        self.verticalLayout.addWidget(self.EthnicGroupLabel)
        self.EthnicGroupLabel_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.EthnicGroupLabel_2.setFont(font)
        self.EthnicGroupLabel_2.setObjectName(_fromUtf8("EthnicGroupLabel_2"))
        self.verticalLayout.addWidget(self.EthnicGroupLabel_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.DOBDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.DOBDisplay.setObjectName(_fromUtf8("DOBDisplay"))
        self.verticalLayout_9.addWidget(self.DOBDisplay)
        self.EthnicGroupDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.EthnicGroupDisplay.setObjectName(_fromUtf8("EthnicGroupDisplay"))
        self.verticalLayout_9.addWidget(self.EthnicGroupDisplay)
        self.EthnicGroupDisplay_2 = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.EthnicGroupDisplay_2.setObjectName(_fromUtf8("EthnicGroupDisplay_2"))
        self.verticalLayout_9.addWidget(self.EthnicGroupDisplay_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_9)
        self.horizontalLayoutWidget = QtGui.QWidget(SimpleButton)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 260, 171, 321))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.horizontalLayoutWidget.setFont(font)
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.FCVLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FCVLabel.setFont(font)
        self.FCVLabel.setObjectName(_fromUtf8("FCVLabel"))
        self.verticalLayout_3.addWidget(self.FCVLabel)
        self.FEV1Label = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FEV1Label.setFont(font)
        self.FEV1Label.setObjectName(_fromUtf8("FEV1Label"))
        self.verticalLayout_3.addWidget(self.FEV1Label)
        self.FEV1FVCLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.FEV1FVCLabel.setFont(font)
        self.FEV1FVCLabel.setObjectName(_fromUtf8("FEV1FVCLabel"))
        self.verticalLayout_3.addWidget(self.FEV1FVCLabel)
        self.PEFRLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.PEFRLabel.setFont(font)
        self.PEFRLabel.setObjectName(_fromUtf8("PEFRLabel"))
        self.verticalLayout_3.addWidget(self.PEFRLabel)
        self.TVLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.TVLabel.setFont(font)
        self.TVLabel.setObjectName(_fromUtf8("TVLabel"))
        self.verticalLayout_3.addWidget(self.TVLabel)
        self.RVLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RVLabel.setFont(font)
        self.RVLabel.setObjectName(_fromUtf8("RVLabel"))
        self.verticalLayout_3.addWidget(self.RVLabel)
        self.ERVLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ERVLabel.setFont(font)
        self.ERVLabel.setObjectName(_fromUtf8("ERVLabel"))
        self.verticalLayout_3.addWidget(self.ERVLabel)
        self.ICLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ICLabel.setFont(font)
        self.ICLabel.setObjectName(_fromUtf8("ICLabel"))
        self.verticalLayout_3.addWidget(self.ICLabel)
        self.VCLabel = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.VCLabel.setFont(font)
        self.VCLabel.setObjectName(_fromUtf8("VCLabel"))
        self.verticalLayout_3.addWidget(self.VCLabel)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.FVCDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.FVCDisplay.setObjectName(_fromUtf8("FVCDisplay"))
        self.verticalLayout_4.addWidget(self.FVCDisplay)
        self.FEV1Display = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.FEV1Display.setObjectName(_fromUtf8("FEV1Display"))
        self.verticalLayout_4.addWidget(self.FEV1Display)
        self.FEV1FVCDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.FEV1FVCDisplay.setObjectName(_fromUtf8("FEV1FVCDisplay"))
        self.verticalLayout_4.addWidget(self.FEV1FVCDisplay)
        self.PEFRDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.PEFRDisplay.setObjectName(_fromUtf8("PEFRDisplay"))
        self.verticalLayout_4.addWidget(self.PEFRDisplay)
        self.FRCDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.FRCDisplay.setObjectName(_fromUtf8("FRCDisplay"))
        self.verticalLayout_4.addWidget(self.FRCDisplay)
        self.RVDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.RVDisplay.setObjectName(_fromUtf8("RVDisplay"))
        self.verticalLayout_4.addWidget(self.RVDisplay)
        self.ERVDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.ERVDisplay.setObjectName(_fromUtf8("ERVDisplay"))
        self.verticalLayout_4.addWidget(self.ERVDisplay)
        self.ICDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.ICDisplay.setObjectName(_fromUtf8("ICDisplay"))
        self.verticalLayout_4.addWidget(self.ICDisplay)
        self.VCDisplay = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.VCDisplay.setObjectName(_fromUtf8("VCDisplay"))
        self.verticalLayout_4.addWidget(self.VCDisplay)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.EditPatientButton = QtGui.QPushButton(SimpleButton)
        self.EditPatientButton.setGeometry(QtCore.QRect(360, 160, 161, 32))
        self.EditPatientButton.setObjectName(_fromUtf8("EditPatientButton"))
        self.Graph_2 = QtGui.QTabWidget(SimpleButton)
        self.Graph_2.setGeometry(QtCore.QRect(230, 230, 451, 371))
        self.Graph_2.setObjectName(_fromUtf8("Graph_2"))
        self.FlowvsVolumePlot = QtGui.QWidget()
        self.FlowvsVolumePlot.setObjectName(_fromUtf8("FlowvsVolumePlot"))
        self.Graph_2.addTab(self.FlowvsVolumePlot, _fromUtf8(""))
        self.VoumevsTimePlot = QtGui.QWidget()
        self.VoumevsTimePlot.setObjectName(_fromUtf8("VoumevsTimePlot"))
        self.Graph_2.addTab(self.VoumevsTimePlot, _fromUtf8(""))
        self.FlowvsTimePlot = QtGui.QWidget()
        self.FlowvsTimePlot.setObjectName(_fromUtf8("FlowvsTimePlot"))
        self.Graph_2.addTab(self.FlowvsTimePlot, _fromUtf8(""))

        self.retranslateUi(SimpleButton)
        self.Graph_2.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(SimpleButton)

    def retranslateUi(self, SimpleButton):
        SimpleButton.setWindowTitle(_translate("SimpleButton", "Simple Form", None))
        self.CalibrateButton.setText(_translate("SimpleButton", "Calibrate", None))
        self.StartButton.setText(_translate("SimpleButton", "Start", None))
        self.StopButton.setText(_translate("SimpleButton", "Stop", None))
        self.CancelButton.setText(_translate("SimpleButton", "Cancel", None))
        self.BREEZETitle.setText(_translate("SimpleButton", "TEST RESULTS", None))
        self.PatientIDLabel.setText(_translate("SimpleButton", "Patient ID", None))
        self.FirstNameLabel.setText(_translate("SimpleButton", "First Name", None))
        self.LastNameLabel.setText(_translate("SimpleButton", "Last Name", None))
        self.GenderLabel.setText(_translate("SimpleButton", "Gender", None))
        self.WeightLabel.setText(_translate("SimpleButton", "Weight (kg)", None))
        self.HeightLabel.setText(_translate("SimpleButton", "Height (cm)", None))
        self.DOBLabel.setText(_translate("SimpleButton", "Date of Birth", None))
        self.EthnicGroupLabel.setText(_translate("SimpleButton", "Ethnic Group", None))
        self.EthnicGroupLabel_2.setText(_translate("SimpleButton", "Current Diagnosis", None))
        self.FCVLabel.setText(_translate("SimpleButton", "FVC (L)", None))
        self.FEV1Label.setText(_translate("SimpleButton", "FEV1 (L)", None))
        self.FEV1FVCLabel.setText(_translate("SimpleButton", "FEV1/FVC (%)", None))
        self.PEFRLabel.setText(_translate("SimpleButton", "PEFR (L/s)", None))
        self.TVLabel.setText(_translate("SimpleButton", "TV (L)", None))
        self.RVLabel.setText(_translate("SimpleButton", "RV (L)", None))
        self.ERVLabel.setText(_translate("SimpleButton", "ERV (L)", None))
        self.ICLabel.setText(_translate("SimpleButton", "IC (L)", None))
        self.VCLabel.setText(_translate("SimpleButton", "TC (L)", None))
        self.EditPatientButton.setText(_translate("SimpleButton", "Edit Patient Details", None))
        self.Graph_2.setTabText(self.Graph_2.indexOf(self.FlowvsVolumePlot), _translate("SimpleButton", "Flow vs Volume", None))
        self.Graph_2.setTabText(self.Graph_2.indexOf(self.VoumevsTimePlot), _translate("SimpleButton", "Volume vs Time", None))
        self.Graph_2.setTabText(self.Graph_2.indexOf(self.FlowvsTimePlot), _translate("SimpleButton", "Flow vs Time", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SimpleButton = QtGui.QWidget()
    ui = Ui_SimpleButton()
    ui.setupUi(SimpleButton)
    SimpleButton.show()
    sys.exit(app.exec_())

### --> UI SETUP END 

### LOOP

WindSpeedPlot = pg.plot()
VolumePlot = pg.plot()
VolFlowPlot = pg.plot()

# Need one tic to start with
tic = millis()

while True:
    # Get values from sensor
    VolFlowRead, WSRead, TempRead = getValues()
    # Integrate to find volume
    toc = millis()
    dt = (toc-tic)/1000 # Time increment in seconds
    Volume += dt*VolFlowRead
    tic = millis() # Measure time from here to toc again --> a complete cycle
    # Append to plot lists
    dtList.append(dt)
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
    
    
    
### --> LOOP END
