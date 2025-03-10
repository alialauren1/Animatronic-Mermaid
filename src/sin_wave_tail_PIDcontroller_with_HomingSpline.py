import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb


# setup of timer, in this case, all have same timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
#timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds


# setup of pins for (1) PWM channels to communicate with motor & (2) ADC to be read
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10) # hip in tail, joint 2
ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3) # knee in tail joint 3
#ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5) # hip to body, joint 1
adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1, on joint 2
adc_S2 = pyb.ADC(pyb.Pin.board.PA7)# create analog object from a pin for servo 2, on joint 3

## Want to read current position before commanding neutral position
fdbck_DC_S1_init = adc_S1.read()
fdbck_DC_S2_init = adc_S2.read()
#print(f"ADC_S1 = {fdbck_DC_S1_init:.2f}")

# convert from ADC to deg
fdbck_theta_S1_init = (-0.048*fdbck_DC_S1_init)+92.28 # position in deg
fdbck_theta_S2_init = (-0.048*fdbck_DC_S2_init)+92.28
print(f"theta1_start = {fdbck_theta_S1_init:.2f},theta2_start = {fdbck_theta_S2_init:.2f} ")
time.sleep(5)

### nEW CODE HERE
# 5TH ORDER SPLINE 

# 5TH ORDER SPLINE 
# spline will go here to move from whatever position read previously to then command neutral position which is shown below
# initial position, rad
theta1_0 = math.radians(fdbck_theta_S1_init)
theta2_0 = math.radians(fdbck_theta_S2_init)

# target homing position
theta1_f = math.radians(0) #hip starting with no offset
theta2_f = math.radians(-18) #knee starting due to offset

# Motion Parameters so that t can also be a variable
a_max = math.radians(15)  # Max acceleration [rad/s^2], can change

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
    
      
    # update values sent to motor through PWM channel
    ch1.pulse_width(pwm1) # round ensures integer going into PWM cmnd
    ch2.pulse_width(pwm2)
    

    print(f"t = {current_time:.2f}, theta1 = {theta1:.2f}, theta2 = {theta2:.2f}, pwm1 = {pwm1}, pwm2 = {pwm2}")

    time.sleep(dt)  # Keep uniform timing

print("-- Reached Home Position --")
time.sleep(3)

print("-- Beginning Sin Trajectory --")


### NEW CODE HERE

# Command neutral PWM position
# print('--Commanding PW neutral position--')
# ch1.pulse_width(neutral)
# ch2.pulse_width(neutral)
# ch3.pulse_width(neutral)

"""
# SIN WAVE CONTROL
#setup of variables for Sin wave
omega = math.radians(50) #deg/s to rad/s
A_hip = 22; # keep in degrees
A_knee = 18; # keep in degrees
phase_diff = math.radians(90) # phase difference between motors 1 and 2

start = (time.ticks_ms()) # starts at arbitrary time

kP = 0.01
kD = .1
err_past = 0
i = 0
ki = .01

print('--Running Loop--')
while True: # create loop that runs continuously until script is stopped
    
    current_t = ((time.ticks_ms())-start)*0.001 # converts to seconds
    
    theta_desired_hip = A_hip*math.sin(omega*current_t)
    theta_desired_knee = A_knee*math.sin(omega*current_t - phase_diff)
    
    fdbck_DC_S1 = adc_S1.read() #read feedback for hip servo
    fdbck_DC_S2 = adc_S2.read() #read feedback for knee servo
    
    fdbck_theta_S1 = (-0.048*fdbck_DC_S1)+92.28
    # fdbck_theta_S2
    
    # PID control
    err = theta_desired_hip - fdbck_theta_S1
    P_theta_S1 = (err)*kP
    I_theta_S1 = i + (ki*err)
    D_theta_S1 = kD*(err-err_past)
    
    err_past = err # saves old err for use in next loop for D control
    i = I_theta_S1
    
    theta_S1_control = theta_desired_hip+P_theta_S1+D_theta_S1
    
    # convert theta values to PWM values
    pwm_desired_hip = (k*(theta_S1_control))+125000
    pwm_desired_knee = (k*theta_desired_knee)+125000
    pwm_desired_verticalax = (k*theta_desired_knee)+125000 #third servo that rotates at hip abt vertical axis
    
    # update values sent to motor through PWM channel
    ch1.pulse_width(round(pwm_desired_hip)) # round ensures integer going into PWM cmnd
    ch2.pulse_width(round(pwm_desired_knee))
    ch3.pulse_width(round(pwm_desired_verticalax))
    
    # uncomment to view value outputs
    print(f"Motor 1 Desired Angle: {theta_desired_hip:.2f}, Motor 2 Desired Angle: {theta_desired_knee:.2f}")
    print(f"Motor 1 Actual Angle: {fdbck_theta_S1:.2f}")
    print(f"Motor 1 Desired PWM: {pwm_desired_hip:.2f}")
    print(f"ADC_S1= {fdbck_DC_S1:.2f}") ## ADC_S2= {fdbck_DC_S2:.2f}"
    print(current_t)
    print('----------------------------------------')
    """