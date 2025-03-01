import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# setup of PWM channels to communicate with motor
# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds
# motor 1
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=neutral)
# motor 2 UPDATE PIN VALUE!
# ch2 = timer2.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=neutral)
    
#setup of variables for Sin wave
omega = math.radians(50) #deg/s to rad/s
A_hip = 22; # keep in degrees
A_knee = 18; # keep in degrees
phase_diff = math.radians(90) # phase difference between motors 1 and 2
k = 1000 # NOTE: k is conversion from theta(in deg) to PWM values

t = 0 # start "i" or "time" at zero

# create loop that runs continuously until script is stopped
while True:
    
    theta_hip = A_hip*math.sin(omega*t)
    theta_knee = A_knee*math.sin(omega*t - phase_diff)
    
    # convert theta values to PWM values
    pwm_hip = k*(theta_hip+75)
    pwm_knee = k*(theta_knee+75)
    
    # update values sent to motor through PWM channel
    ch1.pulse_width(round(pwm_hip)) # round ensures integer going into PWM cmnd
    # ch2.pulse_width(pwm_knee)
    
    t += 0.01 # i found that this works simpler to increment time, if you're ok with it
    
    # uncomment to view value outputs
    print(f"Motor 1 Angle: {theta_hip:.2f}, Motor 2 Angle: {theta_knee:.2f}")
    
    # Unused now but from previous version:
    #t = time.time()
    # time.sleep(0.1) # create delay so signal is not continuous. or do we want continuous idk?? plotted values look better with wait thoug


