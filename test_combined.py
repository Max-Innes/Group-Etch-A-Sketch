from servo_translator import inverse_kinematics, translate

def test_combined():
    # Define arm lengths
    l1, l2 = 15, 10

    # Define test cases
    test_cases = [
        {"x": 10, "y": 10},
        {"x": 5, "y": 5},
        {"x": 20, "y": 0},
    ]

    for case in test_cases:
        try:
            print(f"Testing case: x={case['x']}, y={case['y']}, l1={l1}, l2={l2}")
            alpha, beta = inverse_kinematics(case['x'], case['y'], l1, l2)
            alpha_pwm = translate(alpha)
            beta_pwm = translate(beta)
            print(f"PWM Signals -> Shoulder: {alpha_pwm}, Elbow: {beta_pwm}\n")
        except ValueError as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    test_combined()
