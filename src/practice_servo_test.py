import pyb #dir(pyb)
#import time

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

timer = pyb.Timer(2, freq=2) #periodic freq of timer [Hz]
ch2 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=150000)
# PWM in nano seconds
#100000,150000, 20000
  
# SignalPin = PB_10
# servo1 = pyb.Servo(SignalPin) #
