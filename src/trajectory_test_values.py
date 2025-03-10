import time
import math # note: python uses radians for trig, but degrees elsewhere
import numpy as np
#import ulab as np # if allowed


# 5TH ORDER SPLINE 
# spline will go here to move from whatever position read previously to then command neutral position which is shown below
# initial position, rad
theta1_0 = math.radians(15)
theta2_0 = math.radians(-10)

# target homing position
theta1_f = math.radians(0) #hip starting with no offset
theta2_f = math.radians(-18) #knee starting due to offset

# Motion Parameters so that t can also be a variable
a_max = math.radians(5)  # Max acceleration [rad/s^2], can change

# Compute v_max and estimated t_f
delta_theta1 = abs(theta1_f - theta1_0)
delta_theta2 = abs(theta2_f - theta2_0)

v_max1 = math.sqrt(2 * a_max * delta_theta1)
v_max2 = math.sqrt(2 * a_max * delta_theta2)

t_accel1 = v_max1 / a_max
t_accel2 = v_max2 / a_max

t_f1 = 2 * t_accel1
t_f2 = 2 * t_accel2

# Use max time for synchronized movement
t_f = max(t_f1, t_f2)

# setup fifth order spline
# Construct A matrix for spline coefficients
A = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0],
    [1, t_f, t_f**2, t_f**3, t_f**4, t_f**5],
    [0, 1, 2*t_f, 3*t_f**2, 4*t_f**3, 5*t_f**4],
    [0, 0, 2, 6*t_f, 12*t_f**2, 20*t_f**3]
])

# NOTE: may need to change b eqs
b_theta1 = np.array([theta1_0, 0, a_max, theta1_f, 0, 0])
b_theta2 = np.array([theta2_0, 0, a_max, theta2_f, 0, 0])

# Function to compute theta at time t
def compute_theta(t, coeffs):
    return sum(c * (t ** i) for i, c in enumerate(coeffs))

k = 1000 # NOTE: k is conversion from theta(in deg) to PWM values
# Convert radians to PWM
def angle_to_pwm(theta_rad):
    theta_deg = math.degrees(theta_rad)
    return (k * theta_deg) + 125000  # Mapping to servo PWM

# Execute Spline Motion
print("-- Moving to Home Position --")
start_time = time.ticks_ms()

while True:
    current_time = (time.ticks_ms() - start_time)* 0.001  # Convert ms to seconds
    
    if current_time >= t_f:
        break  # Stop when motion completes

    theta1 = compute_theta(current_time, coeff_theta1)
    theta2 = compute_theta(current_time, coeff_theta2)

    pwm1 = round(angle_to_pwm(theta1))
    pwm2 = round(angle_to_pwm(theta2))
    
    ch1.pulse_width(pwm1)
    ch2.pulse_width(pwm2)

    time.sleep(0.02)  # Control loop timing
    print(f"theta1 = {theta1:.2f}, theta2 = {theta2:.2f}")

print("-- Reached Home Position --")
time.sleep(0.5) # can take out