# calibration python file for the group code.
from machine import Pin
import time

# from inverse kinematics
# assign an origin on a paper.
# make a button that takes a "screenshot" of the current position

'''page calibration code from inverse kinematics'''

def move_pen(alpha: float, beta: float):
    """
    Moves the pen to the calculated joint angles.
    """
    # Convert angles to duty cycles using translate function
    shoulder_duty = translate(alpha)
    elbow_duty = translate(beta)

    # Send signals to servos
    shoulder_servo.duty_u16(shoulder_duty * 65535 // 20000)  # Convert μs to duty_u16
    elbow_servo.duty_u16(elbow_duty * 65535 // 20000)

    print(f"Moving servos: Shoulder = {alpha:.2f}° ({shoulder_duty} μs), Elbow = {beta:.2f}° ({elbow_duty} μs)")

# define the position
# Target coordinates for the pen
x, y = 9, 10  # Replace with the desired position on the page in cms
l1, l2 = 13, 17  # Lengths of the two arm links

try:
    # Calculate joint angles using the inverse kinematics above
    alpha, beta = inverse_kinematics(x, y, l1, l2)

    # Move the pen to the calculated position using the joint angles calculated from the inverse kinematics function
    move_pen(alpha, beta)

    print(f"Pen moved to position: (x={x}, y={y})")
except ValueError as e:
    print(e)

#validating pen movement by drawing a shape
    
def draw_line(x1, y1, x2, y2, steps=10):
    """
    Draws a straight line from (x1, y1) to (x2, y2).
    """
    for i in range(steps + 1):
        # Insert the coordinates
        x = x1 + (x2 - x1) * i / steps
        y = y1 + (y2 - y1) * i / steps

        # Calculate and move to the position
        try:
            alpha, beta = inverse_kinematics(x, y, l1, l2)
            move_pen(alpha, beta)
            time.sleep(0.1)  # Small delay for smooth movement
        except ValueError as e:
            print(e)

# the function being used:
# Draw a line from (5, 5) to (10, 10)
draw_line(5, 5, 10, 10)


# I get the position from the inverse kinematiocs and then defining the position of the pen on the page. 
# make sure that its where it needs to be.

