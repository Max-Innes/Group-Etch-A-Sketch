import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from machine import PWM

# Arm length constants
L1, L2 = 155, 155  # Lengths of the first and second arm segments (in mm)
PWM_MIN, PWM_MAX = 2300, 7500  # Safe PWM bounds for servos

# Translate Function: Convert angle to servo PWM signal
def translate(angle: float) -> int:
    """Translate angle (degrees) to a 16-bit PWM value."""
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000  # Convert to duty cycle (0-1)
    duty_u16_value = int(duty_cycle * 65535)  # Convert to 16-bit scale
    return max(PWM_MIN, min(PWM_MAX, duty_u16_value))  # Clamp to safe limits

# Inverse Kinematics Function
def inverse_kinematics(x, y):
    """
    Compute shoulder (q1) and elbow (q2) angles for given (x, y) position.
    Returns angles in radians.
    """
    r_squared = x**2 + y**2
    if r_squared > (L1 + L2)**2 or r_squared < (L1 - L2)**2:
        raise ValueError("Target out of reach")

    q2 = -math.acos((r_squared - L1**2 - L2**2) / (2 * L1 * L2))  # Elbow angle
    q1 = math.atan2(y, x) + math.atan2(L2 * math.sin(q2), L1 + L2 * math.cos(q2))  # Shoulder angle

    return q1, q2

# Forward Kinematics Function
def forward_kinematics(q1, q2):
    """
    Compute end-effector position (x, y) based on joint angles q1 and q2.
    Returns x, y coordinates of the end effector.
    """
    x1, y1 = L1 * math.cos(q1), L1 * math.sin(q1)
    x2, y2 = x1 + L2 * math.cos(q1 + q2), y1 + L2 * math.sin(q1 + q2)
    return x1, y1, x2, y2

# Safety Wrapper for Servo Control
def safe_move_to(x, y):
    """
    Safely move the robotic arm to a target position (x, y).
    Includes inverse kinematics calculations and PWM clamping.
    """
    try:
        # Calculate joint angles
        q1, q2 = inverse_kinematics(x, y)

        # Translate to PWM
        q1_pwm = translate(math.degrees(q1))
        q2_pwm = translate(math.degrees(q2))

        print(f"Moving to ({x}, {y}) -> q1: {math.degrees(q1):.2f}°, q2: {math.degrees(q2):.2f}°")
        print(f"PWM Signals -> Shoulder: {q1_pwm}, Elbow: {q2_pwm}")

        # Mock servo control with PWM (replace with actual GPIO control in hardware)
        servo_shoulder.duty_u16(q1_pwm)
        servo_elbow.duty_u16(q2_pwm)

    except ValueError as e:
        print(f"Cannot move to ({x}, {y}): {e}")

# Simulate Movement and Plot Arm
def plot_arm(q1, q2):
    """
    Plot the robotic arm for given joint angles q1 (shoulder) and q2 (elbow).
    """
    ax.clear()
    x1, y1, x2, y2 = forward_kinematics(q1, q2)
    ax.plot([0, x1, x2], [0, y1, y2], 'o-', markersize=8, lw=3, label="Arm")
    ax.scatter(x2, y2, c='red', s=100, label="End Effector")
    ax.set_xlim(-L1 - L2 - 10, L1 + L2 + 10)
    ax.set_ylim(-L1 - L2 - 10, L1 + L2 + 10)
    ax.set_aspect('equal', 'box')
    ax.grid(True)
    plt.draw()

# Initialize Servo Connections (Pico)
servo_shoulder = PWM(Pin(0))  # Replace Pin(0) with actual GPIO pin for shoulder
servo_elbow = PWM(Pin(1))     # Replace Pin(1) with actual GPIO pin for elbow
servo_shoulder.freq(50)  # Set PWM frequency
servo_elbow.freq(50)

# Initialize Plot and Sliders
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.3)

# Slider setup for manual testing
ax_x = plt.axes([0.2, 0.2, 0.65, 0.03])
ax_y = plt.axes([0.2, 0.15, 0.65, 0.03])
slider_x = Slider(ax_x, 'X', -L1 - L2, L1 + L2, valinit=100)
slider_y = Slider(ax_y, 'Y', -L1 - L2, L1 + L2, valinit=100)

# Update function for sliders
def update(val):
    x, y = slider_x.val, slider_y.val
    try:
        q1, q2 = inverse_kinematics(x, y)
        plot_arm(q1, q2)
        safe_move_to(x, y)
    except ValueError:
        print("Target out of reach")

slider_x.on_changed(update)
slider_y.on_changed(update)

plt.show()
