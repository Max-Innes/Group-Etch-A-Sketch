from machine import Pin, ADC, PWM
import time

'''initializing variables'''
#start with pen down as the default
pen_position = False
servo = None #will be initialized later on in the program

# main is the main function that wil run the entire pen positioning program
def pen_control():
initialize_servo()
read_position()
switch_position()

#function to set up the servo at an initial position.
def initialize_servo():
   
   servo = PWM(Pin(0)) # servo
    

   ''' input: assign servo to a pin and assign initial position
    output: return servo to initial position'''

#function to read the current position
def read_position():
    '''Input: read input to know the current position of the servo
        if current position is False(down) or True(up)'''
    
        '''output : returns boolean value -> the current position of the servo'''
        
#function to switch position
def switch_position():
    '''input : current position is read
        output : program switches current state to opposite state '''

pen_control() #this runs the main program above
