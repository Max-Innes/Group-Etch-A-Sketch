import math
from machine import PWM

def translate(angle: float) -> int:
#your code here 
pulse_widh = 500 + (2500)
    

def inverse_kinematics(x, y, l1, l2):
    """
    Calculates the angles for a 2-link robotic arm based on the target (x, y).
    Prints key values for debugging to ensure calculations are correct.
    """
    print(f"Inputs -> Target coordinates: (x={x}, y={y}), Arm lengths: l1={l1}, l2={l2}")
    
    # Calculate the distance from the base to the target point
    r = math.sqrt(x**2 + y**2)
    print(f"Distance to target (r): {r:.2f}")
    
    # Check if the target is reachable
    if r > l1 + l2:
        print("Target is out of reach. Try a closer point.")
        raise ValueError("Target is out of reach.")
    if r < abs(l1 - l2):
        print("Target is too close to the base. Try a farther point.")
        raise ValueError("Target is too close.")

    # Calculate the elbow angle (beta) using the cosine rule
    cos_beta = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    print(f"cos(beta): {cos_beta:.2f}")
    beta = math.acos(cos_beta)
    print(f"Elbow angle (beta): {math.degrees(beta):.2f}°")

    # Calculate the shoulder angle (alpha)
    k1 = l1 + l2 * math.cos(beta)
    k2 = l2 * math.sin(beta)
    print(f"Intermediate values -> k1: {k1:.2f}, k2: {k2:.2f}")

    alpha = math.atan2(y, x) - math.atan2(k2, k1)
    print(f"Shoulder angle (alpha): {math.degrees(alpha):.2f}°")

    # Convert radians to degrees
    alpha_deg = math.degrees(alpha)
    beta_deg = math.degrees(beta)

    # Print final results
    print(f"Calculated Angles -> Shoulder (alpha): {alpha_deg:.2f}°, Elbow (beta): {beta_deg:.2f}°")
    print("Calculation complete. Ready for servo input.")

    return alpha_deg, beta_deg

# Example 
try:
    alpha, beta = inverse_kinematics(9, 10, 15, 10)
    print(f"Output -> Shoulder angle: {alpha:.2f}°, Elbow angle: {beta:.2f}°")
except ValueError as e:
    print(e)

#calling of fonction 