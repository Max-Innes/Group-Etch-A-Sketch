#Necessary imports 
from page_calibration import move_pen, draw_line
#from Melissa's_code import d, e, f
from inverse_kinematics import inverse_kinematics
#from Group's_code import j, k, l
from servo_translator import translate
from machine import PWM, Pin, ADC
import time
import math


#Setup / variable initialization (Done)
knob1 = ADC(Pin(27))
knob2 = ADC(Pin(26))

buttonN = Pin(12, Pin.IN, Pin.PULL_DOWN)
buttonE = Pin(11, Pin.IN, Pin.PULL_DOWN)
buttonS = Pin(12, Pin.IN, Pin.PULL_DOWN)
buttonW = Pin(11, Pin.IN, Pin.PULL_DOWN)
buttonM = Pin(12, Pin.IN, Pin.PULL_DOWN)




#Page setup (Neyssa)
page_setup()


while True:
    #Read incoming values (Done)
    #Convert via inverse kinematics (James)
    #Get pos + angle (James)
    #Unittest to ensure it doesn't break (Done)
    #Send command (Melissa)
    #if emergency (Melissa)
        #Stop everything and move all servos to origin
    sleep(x)
