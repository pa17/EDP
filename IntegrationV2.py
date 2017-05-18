## IMPORTS
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
    global Volume
    tic = millis()
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
        
        toc = millis()
        dt = (toc-tic)/1000
        Volume += dt*VolFlowRate
        tic = millis()
    
    return Volume, VolFlowRate, WindSpeed_MetresPerSecond, (TempCtimes100/100), dt
    

### SETUP

# Gain for ADC
GAIN = 1

## VARIABLES
samplingfrequency = 120 # Hz
samplingperiod = 1 / samplingfrequency 
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
lastMillis = 0
Volume = 0

# Initialise lists for subequent plotting
dtPlot = []
WSPlot = []
VolFlowPlot = []
VolPlot = []
TempPlot = []

# Read all the ADC channel values in a list.
readValues = [0]*4

print ("Integration V2")

### --> SETUP END

### LOOP

pw = pg.plot()

while True:
    # Get values from sensor
    VolRead, VolFlowRead, WSRead, TempRead, dtRead = getValues()
    # Append to plot lists
    dtPlot.append(dtRead)
    TempPlot.append(TempRead)
    VolFlowPlot.append(VolFlowRead)
    VolPlot.append(VolRead)
    WSPlot.append(WSRead)
    pw.plot(dtPlot, WSPlot, clear=True)
    pg.QtGui.QApplication.processEvents()
    
    
    
### --> LOOP END
