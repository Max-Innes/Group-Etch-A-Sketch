#Necessary imports
from machine import Pin, ADC, PWM
import time

# Set up ADC for the knobs. Also mapped to LEDs so knob 1 corresponds to LED1 (GP16) and knob 2 corresponds to LED2 (GP17)
knob1 = ADC(Pin(27)) #left 
knob2 = ADC(Pin(26)) #right

# Set up PWM outputs 
pwm1 = PWM(Pin(0)) 
pwm2 = PWM(Pin(1))

# Set PWM frequency
pwm1.freq(1000) #maximum
pwm2.freq(1000)


#Main loop 
while True:
    # Read knob values
    try:
        knob1_value = knob1.read_u16() #pwm pin 
        knob2_value = knob2.read_u16()
        knob1_angle = int((knob1_value / 65535) * 180)
        knob2_angle = int((knob2_value / 65535) * 180)
        # display/send angles to servos
        print(f"X Angle: {knob1_angle}, Y Angle: {knob2_angle}")
        print(f"X Value: {knob1_value}, Y Angle: {knob2_value}")
        time.sleep(0.1)
    except:
        print("Error: Could not read values")


#start with pen down as the default 
try:
    pen_position = False
    servo = None #will be initialized later on in the rest of the code
except:
    print("Could not initialize")

def set_servo_angle(angle):
    #Input: Angle in degrees (0 to 180)
    #Output: Moves the servo to the specified angle
    pulse_width =  500 + (2500 - 500) * angle / 180 # Convert angle to duty cycle + Why converting angle to duty cycle when we already have
    duty = pulse_width / 20000 #Why 20000
    servo.duty_u16(int(duty * 65535))
# pen_control is the main function that wil run the entire pen positioning program

#function to set up the servo at an initial position.
def initialize_servo():  
    servo = PWM(Pin(0)) # servo
    servo.freq(50)
    servo.set_servo_angle(0)
    print("Pen Servo initialized at position: Down")

def pen_control():
    initialize_servo()
    set_servo_angle()
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
        servo.set_servo_angle(0)
        pen_position = False
        print("Pen moved to position: Down")
    else:
        servo.set_servo_angle(90)
        pen_position = True
        print("Pen moved to position: Up")
# current position is read
# program switches current state to opposite state '''

pen_control() #this runs the pen_control program above
