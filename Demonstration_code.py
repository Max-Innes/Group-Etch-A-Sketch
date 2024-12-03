import math
import time
from machine import Pin, PWM, ADC

# Arm length constants
L1, L2 = 155, 155  # Lengths of the first and second arm segments (in mm)

# Initialize Buttons
button_point1 = Pin(13, Pin.IN, Pin.PULL_DOWN)  # Set point 1 (GP13)
button_point2 = Pin(11, Pin.IN, Pin.PULL_DOWN)  # Set point 2 (GP11)
button_updown = Pin(22, Pin.IN, Pin.PULL_DOWN)  # Set pen up/down (GP22)

# Initialize LEDs
led_updown = Pin(20, Pin.OUT)  # Pen up/down state (GP20)
led_pos1 = Pin(16, Pin.OUT)    # Position 1 LED (GP16)
led_pos2 = Pin(17, Pin.OUT)    # Position 2 LED (GP17)
led_updown.off()
led_pos1.off()
led_pos2.off()

# Servo PWM setup
wrist_servo = PWM(Pin(2))  # GP2 for wrist servo
elbow_servo = PWM(Pin(1))  # GP1 for elbow servo
shoulder_servo = PWM(Pin(0))  # GP0 for shoulder servo
wrist_servo.freq(50)
elbow_servo.freq(50)
shoulder_servo.freq(50)

# Setup ADCs for joystick and "sliders" (Potentiometers connected to ADC pins)
joystick_x = ADC(Pin(26))  # X-axis joystick (GP26)
joystick_y = ADC(Pin(27))  # Y-axis joystick (GP27)
knob1 = ADC(Pin(28))  # X-axis knob (GP28)
knob2 = ADC(Pin(29))  # Y-axis knob (GP29)

# Variables to store boundary points
point1_x, point1_y = None, None
point2_x, point2_y = None, None

# Initialize arm color (used for pen up/down)
led_state = False

# Translate Function: Convert angle to PWM signal
def translate(angle: float) -> int:
    """Translate angle (degrees) to a PWM value."""
    PWM_MIN, PWM_MAX = 2300, 7500  # Safe PWM bounds for servos
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000  # Convert to duty cycle (0-1)
    duty_u16_value = int(duty_cycle * 65535)  # Convert to 16-bit scale
    return max(PWM_MIN, min(PWM_MAX, duty_u16_value))  # Clamp to safe limits

# Inverse Kinematics Function (James)
def inverse_kinematics(x, y):
    """
    Compute shoulder (q1) and elbow (q2) angles for given (x, y) position.
    Returns angles in radians.
    """
    r_squared = x**2 + y**2
    if r_squared > (L1 + L2)**2:
        raise ValueError("Target is out of reach")

    q2 = -math.acos((r_squared - L1**2 - L2**2) / (2 * L1 * L2))  # Elbow angle
    q1 = math.atan2(y, x) - math.atan2(L2 * math.sin(q2), L1 + L2 * math.cos(q2))  # Shoulder angle

    return q1, q2

# Forward Kinematics Function (James)
def forward_kinematics(q1, q2):
    """
    Compute end-effector position (x, y) based on joint angles q1 and q2.
    Returns x, y coordinates of the end effector.
    """
    x1, y1 = L1 * math.cos(q1), L1 * math.sin(q1)
    x2, y2 = x1 + L2 * math.cos(q1 + q2), y1 + L2 * math.sin(q1 + q2)
    return x1, y1, x2, y2

# Update the arm's position based on x and y
def update_arm_position(x, y):
    try:
        q1, q2 = inverse_kinematics(x, y)
        print_arm(q1, q2)
        control_servos(q1, q2)
    except ValueError:
        print("Target is out of reach.")

def print_arm(q1, q2):
    """Print the arm's joint angles and end effector position."""
    x1, y1, x2, y2 = forward_kinematics(q1, q2)
    print(f"Arm angles: q1 = {math.degrees(q1):.2f} degrees, q2 = {math.degrees(q2):.2f} degrees")
    print(f"End effector position: ({x2:.2f}, {y2:.2f})")
    print("------------")

# Control the servos to move the arm
def control_servos(q1, q2):
    """Convert joint angles to PWM signals for the servos."""
    # Convert joint angles to PWM pulse widths
    pwm_q1 = translate(math.degrees(q1))
    pwm_q2 = translate(math.degrees(q2))
    
    shoulder_servo.duty_u16(pwm_q1)
    elbow_servo.duty_u16(pwm_q2)
    wrist_servo.duty_u16(pwm_q1)  # Assuming wrist follows shoulder for simplicity

# Button functions to set boundary points (calibration)
def set_point1(pin):
    global point1_x, point1_y
    # Get the current position from the knobs (simulated slider values)
    x = -1*(-310 + 2*(knob1.read_u16() * (L1 + L2)/ 65535))  # Scaling ADC to arm's reach
    y = -1*(knob2.read_u16() * (L1 + L2) / 65535) + 310
    point1_x, point1_y = x, y
    print(f"Point 1 set at: ({point1_x}, {point1_y})")
    led_pos1.on()

def set_point2(pin):
    global point2_x, point2_y
    # Get the current position from the knobs (simulated slider values)
    x = -1*(-310 + 2*(knob1.read_u16() * (L1 + L2)/ 65535))  # Scaling ADC to arm's reach
    y = -1*(knob2.read_u16() * (L1 + L2) / 65535) + 310
    point2_x, point2_y = x, y
    print(f"Point 2 set at: ({point2_x}, {point2_y})")
    led_pos2.on()

    # Update arm position to the new coordinates
    update_arm_position(x, y)

def toggle_led(pin):
    global led_state
    led_state = not led_state
    led_updown.value(led_state)

# Main loop
while True:
    # Read knob values (simulating sliders)
    knob1_value = -1*(-310 + 2*(knob1.read_u16() * (L1 + L2)/ 65535))  # Map ADC to -L1-L2 to L1+L2 range
    knob2_value = -1*(knob2.read_u16() * (L1 + L2) / 65535) + 310
    
    # Read joystick values (0-65535)
    joystick_x_value = joystick_x.read_u16()
    joystick_y_value = joystick_y.read_u16()

    # Map joystick values to servo angles
    shoulder_angle = (joystick_x_value / 65535) * 180  # Map to 0-180 degrees
    elbow_angle = (joystick_y_value / 65535) * 180

    # Update arm position based on joystick or knob values
    update_arm_position(knob1_value, knob2_value)

    # Update servo positions based on joystick
    shoulder_pwm = translate(shoulder_angle)
    elbow_pwm = translate(elbow_angle)

    # Update servo positions for shoulder and elbow servos
    shoulder_servo.duty_u16(shoulder_pwm)
    elbow_servo.duty_u16(elbow_pwm)

    # Simulate pen color and boundary display using LEDs
    if led_state == False:
        led_updown.value(0)  # Pen down
    else:
        led_updown.value(1)  # Pen up

    # Button checks for setting points
    if button_point1.value():
        set_point1(button_point1)
        time.sleep(0.5)  # Debouncing

    if button_point2.value():
        set_point2(button_point2)
        time.sleep(0.5)  # Debouncing

    print(led_state)
    print(f"{point1_x},{point1_y}")
    print(f"{point2_x},{point2_y}")  

    # Small delay to prevent excessive loop cycling
    time.sleep(0.1)
