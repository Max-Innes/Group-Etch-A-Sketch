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

# Set up the pen control
pen_up = 2300
pen_down = 3000

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


   # logical order : is button pressed ? change the state if up turn light on, if down turn the light off, wait 3sec then start again
    # Set up button and light for pen control
button = Pin(15, Pin.IN, Pin.PULL_DOWN)  # Bouton connecté à GPIO 15
light = Pin(2, Pin.OUT)  # Lumière connectée à GPIO 2


def initialize_servo():  
    servo = PWM(Pin(0)) # servo
    servo.freq(50)
    servo.set_servo_angle(0)
    print("Pen Servo initialized at position: Down")

def pen_control():
    initialize_servo()

    while True: #loop to make sure that the program is running continously
        read_position()
        switch_position()
        time.sleep(0.1)

#function to read the current position
def read_position(current_position):
     return pen_position
# IDK IF WE REALLY NEED THIS
        
#function to switch position
def switch_position():
    if pen_position:
        pen_servo.set_servo_angle(0)
        pen_position = False
        print("Pen moved to position: Down")
    else:
       pen_servo.set_servo_angle(90)
        pen_position = True
        print("Pen moved to position: Up")

# Pen control function
def pen_controlight():
    try:
        if button.value():  # Vérifie si le bouton est pressé
            light.value(1)  # Allume la lumière
            print("Pen is up, light ON") 
        else:
            light.value(0)  # Éteint la lumière
            print("Pen is down, light OFF")
        time.sleep(0.3)  # Pause de 0.3 seconde avant de recommencer
    except Exception as e:
        print(f"Error in pen control: {e}")
    
# Call pen control in the main loop
while True:
    pen_controlight()

#emergency handling
#use a while true fonction that we will return the element to the intial state 0 with a print statement
# Configuration du bouton d'urgence et des éléments à contrôler


