import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Arm length constants
L1, L2 = 155, 155  # Lengths of the first and second arm segments (in mm)

# Initial aspect ratio
aspect_ratio = 1

# Inverse Kinematics Function
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

# Forward Kinematics Function
def forward_kinematics(q1, q2):
    """
    Compute end-effector position (x, y) based on joint angles q1 and q2.
    Returns x, y coordinates of the end effector.
    """
    x1, y1 = L1 * math.cos(q1), L1 * math.sin(q1)
    x2, y2 = x1 + L2 * math.cos(q1 + q2), y1 + L2 * math.sin(q1 + q2)
    return x1, y1, x2, y2

# Plotting Function
def plot_arm(q1, q2):
    """
    Plot the robotic arm for given joint angles q1 (shoulder) and q2 (elbow).
    """
    ax.clear()
    x1, y1, x2, y2 = forward_kinematics(q1, q2)
    ax.plot([0, x1, x2], [0, y1, y2], 'o-', markersize=8, lw=3, label="Arm", color=arm_color)
    ax.scatter(x2, y2, c='red', s=100, label="End Effector")
    
    # Display coordinates
    ax.text(x2 + 10, y2 + 10, f"({x2:.1f}, {y2:.1f})", fontsize=12, color='blue')
    
    ax.set_xlim(-L1 - L2 - 10, L1 + L2 + 10)
    ax.set_ylim(0, L1 + L2 + 10)  # Adjust ylim to move the shoulder to the bottom center
    ax.set_aspect(aspect_ratio)  # Set aspect ratio to user inputted value
    
    # Plot the out of reach boundary
    circle = plt.Circle((0, 0), L1 + L2, color='gray', fill=False, linestyle='--', linewidth=1.5)
    ax.add_artist(circle)
    
    # Plot the rectangle if both points are set
    if 'point1_x' in globals() and 'point2_x' in globals():
        rect_x = [point1_x, point2_x, point2_x, point1_x, point1_x]
        rect_y = [point1_y, point1_y, point2_y, point2_y, point1_y]
        ax.plot(rect_x, rect_y, 'r--', lw=3)
    
    ax.grid(True)
    ax.set_title("2-Link Arm Interactive Plot")
    ax.legend()
    plt.draw()

# Slider Update Function
def update(val):
    """Update the plot based on slider values."""
    x = slider_x.val
    y = slider_y.val
    
    # Check if inside the rectangle and update slider values accordingly
    if 'point1_x' in globals() and 'point2_x' in globals():
        if not (min(point1_x, point2_x) <= x <= max(point1_x, point2_x) and min(point2_y, point1_y) <= y <= max(point2_y, point1_y)):
            slider_x.eventson = False
            slider_y.eventson = False
            slider_x.set_val(min(max(x, min(point1_x, point2_x)), max(point1_x, point2_x)))
            slider_y.set_val(min(max(y, min(point2_y, point1_y)), max(point2_y, point1_y)))
            slider_x.eventson = True
            slider_y.eventson = True
            return
    
    try:
        q1, q2 = inverse_kinematics(slider_x.val, slider_y.val)
        plot_arm(q1, q2)
    except ValueError:
        ax.clear()
        ax.text(0, 0.5 * (L1 + L2), "Out of Reach", fontsize=20, color='red', ha='center')
        ax.set_xlim(-L1 - L2 - 10, L1 + L2 + 10)
        ax.set_ylim(0, L1 + L2 + 10)  # Adjust ylim to move the shoulder to the bottom center
        ax.set_aspect(aspect_ratio)  # Set aspect ratio to user inputted value
        
        # Plot the out of reach boundary
        circle = plt.Circle((0, 0), L1 + L2, color='gray', fill=False, linestyle='--', linewidth=1.5)
        ax.add_artist(circle)
        
        # Plot the rectangle if both points are set
        if 'point1_x' in globals() and 'point2_x' in globals():
            rect_x = [point1_x, point2_x, point2_x, point1_x, point1_x]
            rect_y = [point1_y, point1_y, point2_y, point2_y, point1_y]
            ax.plot(rect_x, rect_y, 'r--', lw=3)
        
        ax.grid(True)
        ax.set_title("Out of Reach")
        plt.draw()

# Toggle Button Function
def toggle_color(event):
    global arm_color
    
    # Check if inside the rectangle and update color accordingly
    if 'point1_x' in globals() and 'point2_x' in globals():
        if min(point1_x, point2_x) <= slider_x.val <= max(point1_x, point2_x) and min(point2_y, point1_y) <= slider_y.val <= max(point2_y, point1_y):
            arm_color = 'green' if arm_color == 'blue' else 'blue'
            button_color.label.set_text('Color Changed')
            q1, q2 = inverse_kinematics(slider_x.val, slider_y.val)
            plot_arm(q1, q2)
            button_color.disconnect(toggle_color)

# Set Point 1 Function
def set_point1(event):
    global point1_x, point1_y
    point1_x = slider_x.val
    point1_y = slider_y.val
    print(f"Point 1 set to: ({point1_x}, {point1_y})")

# Set Point 2 Function
def set_point2(event):
    global point2_x, point2_y
    point2_x = slider_x.val
    point2_y = slider_y.val
    
    print(f"Point 2 set to: ({point2_x}, {point2_y})")
    
    update(None)

# Initial plot setup with 1x1 aspect ratio
fig, ax = plt.subplots(figsize=(8.5, 8.5))
plt.subplots_adjust(bottom=0.3)
x_init, y_init = 100, 100

# Initial arm color
arm_color = 'blue'

try:
    q1_init, q2_init = inverse_kinematics(x_init, y_init)
    plot_arm(q1_init, q2_init)
except ValueError:
    ax.text(0, 0.5 * (L1 + L2), "Out of Reach", fontsize=20, color='red', ha='center')
    # Plot the out of reach boundary
    circle = plt.Circle((0, 0), L1 + L2, color='gray', fill=False, linestyle='--', linewidth=1.5)
    ax.add_artist(circle)

# Slider setup
ax_x = plt.axes([0.15, 0.15, 0.75, 0.03])
ax_y = plt.axes([0.15, 0.10, 0.75, 0.03])
slider_x = Slider(ax_x, 'X', -L1 - L2, L1 + L2, valinit=x_init)
slider_y = Slider(ax_y, 'Y', 0, L1 + L2, valinit=y_init)  # Adjust slider_y range to match new ylim
slider_x.on_changed(update)
slider_y.on_changed(update)

# Toggle button setup for color change
ax_button_color = plt.axes([0.45, 0.025, 0.15, 0.04])
button_color = Button(ax_button_color, 'Toggle Color')
button_color.on_clicked(toggle_color)

# Button setup for setting point 1
ax_button_point1 = plt.axes([0.05, 0.025, 0.15, 0.04])
button_point1 = Button(ax_button_point1, 'Set Point 1')
button_point1.on_clicked(set_point1)

# Button setup for setting point 2
ax_button_point2 = plt.axes([0.25, 0.025, 0.15, 0.04])
button_point2 = Button(ax_button_point2, 'Set Point 2')
button_point2.on_clicked(set_point2)

plt.show()
