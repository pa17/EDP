# Import time
import time
# Import the ADS1x15 module.
import Adafruit_ADS1x15
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# Gain for ADC
GAIN = 1

zeroWindAdjustment =  .2 # Negative numbers yield smaller wind speeds and vice versa.
TMP_Therm_ADunits = 0    # Temp termistor value from wind sensor
RV_Wind_ADunits = 0.0    # RV output from wind sensor 
RV_Wind_Volts = 0.0
lastMillis = 0
TempCtimes100 = 0
zeroWind_ADunits = 0.0
zeroWind_volts = 0.0
WindSpeed_MPH = 0.0
WindSpeed_MetresPerSecond = 0.0
VolFlowRate = 0.0


print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    scaledvalues = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
        scaledvalues[i] = values[i]*0.01561
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*scaledvalues))
    # Pause for half a second.
    time.sleep(0.5)
