import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer
timer = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# setup of PWM channels to communicate with motor
# setup in Neutral Position: 1500 microseconds = 1500000ns
neutral = 15000000
# motor 1
ch1 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=neutral)
# motor 2 UPDATE PIN VALUE!
ch2 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=neutral)
    
#setup of variables for Sin wave
omega = math.radians(50) #deg/s to rad/s
A_hip = 22; # keep in degrees
A_knee = 18; # keep in degrees
phase_diff = math.radians(90) # phase difference between motors 1 and 2
k = 1 # NOTE: k will be conversion from theta(in deg) to PW values, add in when identified!

# create loop that runs continuously until script is stopped
while True:
    t = time.time()
    theta_hip = A_hip*math.sin(omega*t)
    theta_knee = A_knee*math.sin(omega*t - phase_diff)
    
    # convert theta values to PWM values
    pwm_hip = k*theta_hip
    pwm_knee = k*theta_knee
    
    # update values sent to motor through PWM channel
    ch1.pulse_width(pwm_hip)
    ch2.pulse_width(pwm_knee)

    # uncomment to view value outputs
    print(f"Motor 1 Angle: {theta_hip:.2f}, Motor 2 Angle: {theta_knee:.2f}")
    
    time.sleep(0.1) # create delay so signal is not continuous. or do we want continuous idk?? plotted values look better with wait though
    



