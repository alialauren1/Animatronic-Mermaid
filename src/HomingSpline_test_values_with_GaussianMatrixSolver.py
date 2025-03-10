import time
import math # note: python uses radians for trig, but degrees elsewhere


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
# Solve matrix manually since libraries with linear algebra not installed on nucleo board
# Construct A matrix manually
A = [
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 0],
    [1, t_f, t_f**2, t_f**3, t_f**4, t_f**5],
    [0, 1, 2*t_f, 3*t_f**2, 4*t_f**3, 5*t_f**4],
    [0, 0, 2, 6*t_f, 12*t_f**2, 20*t_f**3]
]

# Define the b vectors
b_theta1 = [theta1_0, 0, a_max, theta1_f, 0, 0]
b_theta2 = [theta2_0, 0, a_max, theta2_f, 0, 0]

# Function to compute theta at time t using polynomial coefficients
def compute_theta(t, coeffs):
    return sum(c * (t ** i) for i, c in enumerate(coeffs))

# Function for solving linear equations (Gaussian Elimination method)
def solve_gaussian(A, b):
    # Augment the matrix A with b to form [A|b]
    n = len(A)
    Augmented = [row + [b[i]] for i, row in enumerate(A)]
    
    # Perform Gaussian elimination
    for i in range(n):
        # Make the diagonal contain all 1s
        if Augmented[i][i] == 0:
            for j in range(i + 1, n):
                if Augmented[j][i] != 0:
                    Augmented[i], Augmented[j] = Augmented[j], Augmented[i]
                    break
        
        # Normalize the pivot row
        pivot = Augmented[i][i]
        for j in range(i, n + 1):
            Augmented[i][j] /= pivot
        
        # Eliminate the column entries below the pivot
        for j in range(i + 1, n):
            factor = Augmented[j][i]
            for k in range(i, n + 1):
                Augmented[j][k] -= factor * Augmented[i][k]
    
    # Back substitution
    coeffs = [0] * n
    for i in range(n - 1, -1, -1):
        coeffs[i] = Augmented[i][n]
        for j in range(i + 1, n):
            coeffs[i] -= Augmented[i][j] * coeffs[j]
    
    return coeffs

# Solve for the coefficients of the splines
coeff_theta1 = solve_gaussian(A, b_theta1)
coeff_theta2 = solve_gaussian(A, b_theta2)


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
