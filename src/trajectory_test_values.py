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
a_max = math.radians(12)  # Max acceleration [rad/s^2], can change

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
print(f"time_to_home = {t_f:.2f}")

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

# solver for finding coefficients from A and b (A\b in MATLAB)
coeff_theta1 = np.linalg.solve(A, b_theta1)
coeff_theta2 = np.linalg.solve(A, b_theta2)

# Function to compute theta at time t
def compute_theta(t, coeffs):
    return sum(c * (t ** i) for i, c in enumerate(coeffs))

k = 1000 # NOTE: k is conversion from theta(in deg) to PWM values

# Execute Spline Motion
dt = 0.02  # Fixed time step of 20 ms
num_steps = int(t_f / dt)  # Total number of steps

print("-- Moving to Home Position --")

for i in range(num_steps + 1):  
    current_time = i * dt  

    theta1 = math.degrees(compute_theta(current_time, coeff_theta1))
    theta2 = math.degrees(compute_theta(current_time, coeff_theta2))

    pwm1 = round((k*theta1)+125000)
    pwm2 = round((k*theta2)+125000)

    print(f"t = {current_time:.2f}, theta1 = {theta1:.2f}, theta2 = {theta2:.2f}, pwm1 = {pwm1}, pwm2 = {pwm2}")

    time.sleep(dt)  # Keep uniform timing

print("-- Reached Home Position --")
time.sleep(3)

print("-- Beginning Sin Trajectory --")


