import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer, in this case, all have same timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds

# setup of pins for (1) PWM channels to communicate with motor & (2) ADC to be read
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10) # hip in tail, joint 2
ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3) # knee in tail joint 3
ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5) # hip to body, joint 1
adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1, on joint 2
adc_S2 = pyb.ADC(pyb.Pin.board.PA7)# create analog object from a pin for servo 2, on joint 3

## Want to read current position before commanding position
fdbck_DC_S1_init = adc_S1.read()
fdbck_DC_S2_init = adc_S2.read()
time.sleep(3)

# convert from ADC to theta and/or PWM
fdbck_theta_S1_init = (-0.048*fdbck_DC_S1_init)+92.28 # position in deg
fdbck_theta_S2_init = (-0.048*fdbck_DC_S2_init)+92.28 # position in deg
fdbck_theta_S1_init = (-47.77*fdbck_DC_S1_init)+217195 # PWM
fdbck_theta_S2_init = (-47.77*fdbck_DC_S2_init)+217195 # PWM
print(f"feedback pos S1 = {fdbck_theta_S1_init:.2f}, feedback pos S2 = {fdbck_theta_S2_init:.2f}")

#setup of variables for Sin wave
omega = math.radians(50) #deg/s to rad/s
A_hip = 22; # keep in degrees
A_knee = 18; # keep in degrees
phase_diff = math.radians(90) # phase difference between motors 1 and 2
k = 1000 # NOTE: k is conversion from theta(in deg) to PWM values

start = (time.ticks_ms()) # starts at arbitrary time

print('--Running Loop--')
while True: # create loop that runs continuously until script is stopped
    
    current_t = ((time.ticks_ms())-start)*0.001 # converts to seconds
    
    theta_desired_hip = A_hip*math.sin(omega*current_t)
    theta_desired_knee = A_knee*math.sin(omega*current_t - phase_diff)
    
    
    
    # maybe spline can go here and can use a comparision of feedback and desired to see if need to do spline instead sin wave
    # if u choose this, u can put this section and then the sin wav sections in an "if else" statement so it only does one or the other
    
    
    
    # convert theta values to PWM values
    pwm_desired_hip = (k*theta_desired_hip)+125000
    pwm_desired_knee = (k*theta_desired_knee)+125000
    pwm_desired_verticalax = (k*theta_desired_knee)+125000 #third servo that rotates at hip abt vertical axis

    # nice to see feedback if want:
    fdbck_DC_S1 = adc_S1.read() #read feedback for hip servo
    fdbck_DC_S2 = adc_S2.read() #read feedback for knee servo
    fdbck_theta_S1 = (-0.048*fdbck_DC_S1)+92.28 # position in deg
    fdbck_theta_S2 = (-0.048*fdbck_DC_S2)+92.28 # position in deg
    
    # update values sent to motor through PWM channel
    ch1.pulse_width(round(pwm_desired_hip)) # round ensures integer going into PWM cmnd
    ch2.pulse_width(round(pwm_desired_knee))
    ch3.pulse_width(round(pwm_desired_verticalax))
    
    # uncomment to view value outputs
    print(f"Motor 1 Desired Angle: {theta_desired_hip:.2f}, Motor 2 Desired Angle: {theta_desired_knee:.2f}")
    #print(f"Motor 1 Desired PWM: {pwm_desired_hip:.2f}")
    print(f"feedback theta S1 = {fdbck_theta_S1:.2f}, feedback theta S2 = {fdbck_theta_S2:.2f}") 
    print(current_t)
    print('----------------------------------------')