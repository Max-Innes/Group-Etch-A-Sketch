#Necessary imports
from machine import Pin, ADC, PWM
import time

# Set up ADC for the knobs. Also mapped to LEDs so knob 1 corresponds to LED1 (GP16) and knob 2 corresponds to LED2 (GP17)
knob1 = ADC(Pin(27))
knob2 = ADC(Pin(26))

# Set up PWM outputs
pwm1 = PWM(Pin(0))
pwm2 = PWM(Pin(1))

# Set PWM frequency
pwm1.freq(1000)
pwm2.freq(1000)

#Main loop
while True:
    # Read knob values
    try:
        knob1_value = knob1.read_u16()
        knob2_value = knob2.read_u16()
    except:
        print("Error: Could not read values")

    # Map knob values to PWM duty cycle (0-65535)
    pwm1.duty_u16(knob1_value)
    pwm2.duty_u16(knob2_value)

    #For testing purposes, prints the result
    print(knob1_value)
    print(knob2_value)

    time.sleep(1) 


# assign/configure ADC pins for X and Y potentiometers
knob1 = machine.ADC(26)  # ADC pin for X potentiometer =(GPIO 26)
knob2 = machine.ADC(27)  # ADC pin for Y potentiometer =(GPIO 27)

# define a function to read ADC values and map them to servo angles for us to use later on 
def read_potentiometers():
    # read the raw ADC value (range from 0-65535 for 16-bit)
    knob1_value = knob1.read_u16()
    knob2_value = knob2.read_u16()
    
    # map the raw values to a servo angle to hit all 0 to 180 degrees
    knob1_angle = int((knob1_value / 65535) * 180)
    knob2_angle = int((knob2_value / 65535) * 180)
    
    return knob1_angle, knob2_angle

# main loop(while ture)
while True:
    # read the potentiometer values given by reader and convert it into angles
    knob1_angle, knob2_angle = read_potentiometers()
    
    # display/send angles to servos
    print(f"X Angle: {knob1_angle}, Y Angle: {knob2_angle}")
    
    # delay for some stability
    time.sleep(0.3)

#Neyssa you may need to make some changes with your code
'''initializing variables'''
#start with pen down as the default
pen_position = False
servo = None #will be initialized later on in the rest of the code

# main is the main function that wil run the entire pen positioning program
def pen_control():
    initialize_servo()
    read_position() 
    switch_position() 

#function to set up the servo at an initial position.
def initialize_servo():  
    servo = PWM(Pin(0)) # servo
    servo.freq(50)
    servo.set_servo_angle(0)
    print("Pen Servo initialized at position: Down")
''' input: assign servo to a pin and assign initial position
output: return servo to initial position'''

#function to read the current position
def read_position(current_position):
     return pen_position

'''Input: read input to know the current position of the servo
if current position is False(down) or True(up)'''
    
'''output : returns boolean value -> the current position of the servo'''
        
#function to switch position
def switch_position():
    if pen_position:
        servo.set_servo_angle(0)
        pen_position = False
        print("Pen moved to position: Down")
    else:
        servo.set_servo_angle(90)
        pen_position = True
        print("Pen moved to position: Up")
'''input : current position is read
output : program switches current state to opposite state '''

pen_control() #this runs the main program above
