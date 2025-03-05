import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer, in this case, all have same timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds

# setup of PWM channels to communicate with motor
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=neutral) # hip in tail, joint 2
ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3, pulse_width=neutral) # knee in tail joint 3
ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5, pulse_width=neutral) # hip to body, joint 1
#  
# adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1
# adc_S2 = pyb.ADC(pyb.Pin.board.PA7)# create analog object from a pin for servo 2
    
#setup of variables for Sin wave
omega = math.radians(50) #deg/s to rad/s
A_hip = 22; # keep in degrees
A_knee = 18; # keep in degrees
phase_diff = math.radians(90) # phase difference between motors 1 and 2
k = 1000 # NOTE: k is conversion from theta(in deg) to PWM values

start = (time.ticks_ms()) # starts at arbitrary time

while True: # create loop that runs continuously until script is stopped
    
    current_t = ((time.ticks_ms())-start)*0.001 # converts to seconds
    
    theta_desired_hip = A_hip*math.sin(omega*current_t)
    theta_desired_knee = A_knee*math.sin(omega*current_t - phase_diff)
    
    # convert theta values to PWM values
    pwm_desired_hip = k*(theta_desired_hip+75)
    pwm_desired_knee = k*(theta_desired_knee+75)

    #fdbck_DC_S1 = adc_S1.read() #read feedback for hip servo
    
#     #Theory: P controller = (target - current position otherwise known as feedback pin)*gain
#     PID_theta_err=(theta_knee - fdback_in_theta)*(1)
#     PID_pwm_hip = k*((PID_theta_err+theta_knee)+75)
    
    # update values sent to motor through PWM channel
    ch1.pulse_width(round(pwm_desired_hip)) # round ensures integer going into PWM cmnd
    ch2.pulse_width(round(pwm_desired_knee))
    ch3.pulse_width(round(pwm_desired_hip))
    
    # uncomment to view value outputs
    print(f"Motor 1 Desired Angle: {theta_desired_hip:.2f}, Motor 2 Desired Angle: {theta_desired_knee:.2f}")
#    print(f"Motor 1 Desired PWM: {pwm_desired_hip:.2f}")
#    print(f"Motor 1 Measured PWM: {fdback_PWM_S1:.2f},ADC= {fdbck_DC_S1:.2f}")
    print(current_t)
    


