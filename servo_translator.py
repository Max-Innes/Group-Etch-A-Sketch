from machine import PWM
import math

def translate(angle: float) -> int:
    """Translate a degree input into a servo PWM signal."""
    pulse_width = 500 + (2500 - 500) * angle / 180  # Pulse width equation
    duty_cycle = pulse_width / 20000  # 20000 microseconds / 20ms
    duty_u16_value = int(duty_cycle * 65535)  # Convert to 16-bit PWM value
    duty_u16_value = max(2300, min(7500, duty_u16_value))  # Clamp value
    return duty_u16_value

def inverse_kinematics(x, y, l1, l2):
    """Calculate the angles for a 2-link robotic arm based on target (x, y)."""
    print(f"Inputs -> Target coordinates: (x={x}, y={y}), Arm lengths: l1={l1}, l2={l2}")
    r = math.sqrt(x**2 + y**2)
    print(f"Distance to target (r): {r:.2f}")

    if r > l1 + l2:
        print("Target is out of reach. Try a closer point.")
        raise ValueError("Target is out of reach.")
    if r < abs(l1 - l2):
        print("Target is too close to the base. Try a farther point.")
        raise ValueError("Target is too close.")

    cos_beta = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    beta = math.acos(cos_beta)
    k1 = l1 + l2 * math.cos(beta)
    k2 = l2 * math.sin(beta)
    alpha = math.atan2(y, x) - math.atan2(k2, k1)

    alpha_deg = math.degrees(alpha)
    beta_deg = math.degrees(beta)
    print(f"Calculated Angles -> Shoulder (alpha): {alpha_deg:.2f}°, Elbow (beta): {beta_deg:.2f}°")
    return alpha_deg, beta_deg
