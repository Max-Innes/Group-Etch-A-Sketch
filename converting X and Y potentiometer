import machine
import utime

# assign/configure ADC pins for X and Y potentiometers
adc_x = machine.ADC(26)  # ADC pin for X potentiometer =(GPIO 26)
adc_y = machine.ADC(27)  # ADC pin for Y potentiometer =(GPIO 27)

# define a function to read ADC values and map them to servo angles for us to use later on 
def read_potentiometers():
    # read the raw ADC value (range from 0-65535 for 16-bit)
    x_value = adc_x.read_u16()
    y_value = adc_y.read_u16()
    
    # map the raw values to a servo angle to hit all 0 to 180 degrees
    x_angle = int((x_value / 65535) * 180)
    y_angle = int((y_value / 65535) * 180)
    
    return x_angle, y_angle

# main loop(while ture)
while True:
    # read the potentiometer values given by reader and convert it into angles
    x_angle, y_angle = read_potentiometers()
    
    # display/send angles to servos
    print(f"X Angle: {x_angle}, Y Angle: {y_angle}")
    
    # delay for some stability
    utime.sleep(0.3)

"""def read_potentiometers():: this calls the function to read values from both potentiometers and convert them into angles.
x_value = adc_x.read_u16(): read_u16() reads the raw digital value from the ADC pin. The returned value ranges from 0 to 65535 because the Pico’s ADC uses 16 bits (a range of 2^16).
while True:: this is an infinite loop(while loop), so the program keeps running and updating the angles as long as the pico is powered on.
x_angle, y_angle = read_potentiometers(): this calls the read_potentiometers() function we defined earlier and stores the y and x angle values we ."""
