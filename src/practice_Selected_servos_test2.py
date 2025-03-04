import time
import math # note: python uses radians for trig, but degrees elsewhere
import pyb

# setup of timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
timer2 = pyb.Timer(1, freq=50) #periodic freq of timer [Hz]
timer3 = pyb.Timer(3, freq=50)

# setup in Neutral Position: 1250 microseconds = 1250000ns
neutral = 125000 # 10s of nanoseconds

# setup of PWM channels to communicate with motor
ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=200000) # motor 1
ch2 = timer2.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA8, pulse_width=200000) # motor 2
ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PB4, pulse_width=neutral) 
 
# ch1.pulse_width(round(200000))
# ch2.pulse_width(round(200000))