from machine import Pin, ADC, PWM
import time

'''initializing variables'''
#start with pen down as the default
pen_position = False
servo = None #will be initialized later on in the rest of the code

# main is the main function that wil run the entire pen positioning program
def pen_control():
    initialize_servo()
    while True: #loop to make sure that the program is running continously
        read_position()
        switch_position()
        time.sleep(2)

def set_servo_angle(angle):
    '''Input: Angle in degrees (0 to 180)
       Output: Moves the servo to the specified angle'''
    pulse_width =  500 + (2500 - 500) * angle / 180 # Convert angle to duty cycle
    duty = pulse_width / 20000
    servo.duty_u16(int(duty * 65535))


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
