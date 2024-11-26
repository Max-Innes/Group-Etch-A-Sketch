#Necessary imports
from machine import Pin, ADC, PWM
import time

# Set up ADC for the knobs. Also mapped to LEDs so knob 1 corresponds to LED1 (GP16) and knob 2 corresponds to LED2 (GP17)
knob1 = ADC(Pin(27))
knob2 = ADC(Pin(26))

button1 = Pin(12, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(11, Pin.IN, Pin.PULL_DOWN)

# Set up PWM outputs
pwm1 = PWM(Pin(0))
pwm2 = PWM(Pin(1))

# Set PWM frequency
pwm1.freq(1000)
pwm2.freq(1000)

# function to set servo angles
def set_servo_angle(angle):
    '''Input: Angle in degrees (0 to 180)
       Output: Moves the servo to the specified angle'''
    pulse_width =  500 + (2500 - 500) * angle / 180 # Convert angle to duty cycle
    duty = pulse_width / 20000

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

#function to control pen up and down. still not very functional but buttons are gonna be used to control the servo.
def pen_control():
    while True:
        if button2.value() == 1:
            print("Moving servo to UP position (0°)")
            set_servo_angle(0)  # Pen up
            time.sleep(2)       # Wait for 2 seconds
        else:
            button1.value() == 1
            print("Moving servo to DOWN position (90°)")
            set_servo_angle(90)  # Pen down
            time.sleep(2)       # Wait for 2 seconds

pen_control() #this runs the pen_control program above

