# Import time
import time
# Import the ADS1x15 module.
import Adafruit_ADS1x15
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
# Connect TMP to A0 and RV to A1

# Gain for ADC
GAIN = 1

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

# Read all the ADC channel values in a list.
readValues = [0]*4
printList = [0]*5
headerList = ["Temp AD", "RV Wind AD", "Temperature", "Windspeed (m/s)", "Volumetric flow rate (m^3/s)"]

print('Reading ADS1x15 values from Wind sensor, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} |'.format(*headerList))
print('-' * 37)
# Main loop.
while True:

    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        readValues[i] = adc.read_adc(i, gain=GAIN)
        readValues[i] = readValues[i]*0.01561 # Values scaled to 10 bit so that Arduino code can be adapted
        
    # Temp reading
    TMP_Therm_ADunits = readValues[0]
    # RV reading
    RV_Wind_ADunits = readValues[1]
    RV_Wind_Volts = (RV_Wind_ADunits * 0.0048828125)
    # Calculate temperature
    TempCtimes100 = (0.005*TMP_Therm_ADunits*TMP_Therm_ADunits) - 16.862*TMP_Therm_ADunits + 9075.4
    # Calculate zero wind
    zeroWind_ADunits = -0.0006*TMP_Therm_ADunits*TMP_Therm_ADunits + 1.0727*TMP_Therm_ADunits + 47.172
    # Zero wind adjustment
    zeroWind_Volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment

    #DEBUG
    #print ("RV Wind")
    #print (RV_Wind_Volts)
    #print ("zero Wind")
    #print (zeroWind_Volts)        
    #print ("Difference")
    #print (RV_Wind_Volts - zeroWind_Volts)

    # Wind speed in MPH
    try:
        WindSpeed_MPH = ((RV_Wind_Volts - zeroWind_Volts)/0.2300)**2.7265
        WindSpeed_MetresPerSecond = WindSpeedMPH * 0.44704
        VolFlowRate = 6.931 * WindSpeed_MetresPerSecond
    except:
        pass

    printList[0] = TMP_Therm_ADunits
    printList[1] = RV_Wind_ADunits
    printList[2] = TempCtimes100/100
    printList[3] = WindSpeed_MetresPerSecond
    printList[4] = VolFlowRate

    
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} | {4:>6} |'.format(*printList))
    #print VolFlowRate
    # Pause for half a second.
    time.sleep(0.5)
