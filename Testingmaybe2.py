import math
from machine import Pin, PWM, ADC  # Include ADC for analog input (joystick/knobs)

# Servo and Joystick Configuration
L1, L2 = 155, 155  # Arm lengths in mm
PWM_MIN, PWM_MAX = 2300, 7500  # Safe PWM bounds for servos
ANGLE_MIN, ANGLE_MAX = 0, 180  # Minimum and maximum angles for servos

# Initialize PWM for servos
servo_shoulder = PWM(Pin(0))  # GPIO pin for shoulder servo
servo_elbow = PWM(Pin(1))     # GPIO pin for elbow servo
servo_shoulder.freq(50)
servo_elbow.freq(50)

# Initialize ADC for joystick or knobs
joystick_x = ADC(Pin(26))  # Connect joystick X-axis to ADC pin (e.g., GP26)
joystick_y = ADC(Pin(27))  # Connect joystick Y-axis to ADC pin (e.g., GP27)

# Map Joystick Values to Servo Angles
def map_joystick_to_angle(joystick_value):
    """
    Maps joystick ADC value (0-65535) to servo angle (0-180).
    """
    return ANGLE_MIN + (joystick_value / 65535) * (ANGLE_MAX - ANGLE_MIN)

# Translate Servo Angle to PWM Signal
def translate(angle: float) -> int:
    """
    Convert angle (degrees) to a 16-bit PWM signal for servo control.
    """
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000
    return max(PWM_MIN, min(PWM_MAX, int(duty_cycle * 65535)))

# Update Servo Positions Based on Joystick Input
def update_servo_positions():
    """
    Read joystick input and update servo positions accordingly.
    """
    # Read joystick values (0-65535)
    x_value = joystick_x.read_u16()
    y_value = joystick_y.read_u16()

    # Map joystick values to servo angles
    shoulder_angle = map_joystick_to_angle(x_value)
    elbow_angle = map_joystick_to_angle(y_value)

    # Translate angles to PWM signals
    shoulder_pwm = translate(shoulder_angle)
    elbow_pwm = translate(elbow_angle)

    # Print debug information
    print(f"Joystick -> X: {x_value}, Y: {y_value}")
    print(f"Angles -> Shoulder: {shoulder_angle:.2f}°, Elbow: {elbow_angle:.2f}°")
    print(f"PWM -> Shoulder: {shoulder_pwm}, Elbow: {elbow_pwm}")

    # Update servo positions
    servo_shoulder.duty_u16(shoulder_pwm)
    servo_elbow.duty_u16(elbow_pwm)

# Main Loop
while True:
    update_servo_positions()
