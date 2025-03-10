import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds

# setup of PWM channels to communicate with motor
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10) # hip in tail, joint 2
ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3) # knee in tail joint 3
ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5) # hip to body, joint 1
 
print("-- running1 --")
ch1.pulse_width(round(200000))
ch2.pulse_width(round(200000))
time.sleep(1)
print("-- running2 --")
ch1.pulse_width(round(125000))
ch2.pulse_width(round(125000))