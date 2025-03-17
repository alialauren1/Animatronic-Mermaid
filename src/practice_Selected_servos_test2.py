import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer3 = pyb.Timer(2, freq=	0.0001, prescaler = 0) #periodic freq of timer [Hz]

#0.0001

# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds

# setup of PWM channels to communicate with motor
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10) # hip in tail, joint 2
ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3) # knee in tail joint 3
ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5) # hip to body, joint 1

# homing
time.sleep(3)
print('commanding')
ch3.pulse_width(125000)

time.sleep(3)
print('homed')
# revert back to residred freq
timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

omega_spin = math.radians(80) #deg/s to rad/s
A_spin = 10;
k = 1000

time.sleep(3)
start = (time.ticks_ms()) 
print("-- running2 --")
while True: # create loop that runs continuously until script is stopped
    
    
    current_t = ((time.ticks_ms())-start)*0.001 # converts to seconds
    
    theta_verticalax = A_spin*math.sin(omega_spin*current_t)
    
    pwm_desired_verticalax = (k*theta_verticalax)+125000 #third servo that rotates at hip abt vertical axis
    
    ch3.pulse_width(round(pwm_desired_verticalax))
    
    
#ch1.pulse_width(round(125000))
#ch2.pulse_width(round(125000))
ch3.pulse_width(round(12000))
time.sleep(2)
print("-- running1 --")
#ch1.pulse_width(round(100000))
#ch2.pulse_width(round(100000))
#ch3.pulse_width(round(100000))
time.sleep(1)

