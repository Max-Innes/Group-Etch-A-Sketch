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

    #Hey Melissa, you may have to change the time between for the actual thing, I just left it as 1 for now.
    time.sleep(1)

#If you need me to modify my code in any way, let me know!