import pyb #dir(pyb)

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

timer = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
ch2 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=200000) # PW in 10s of nano seconds I think
# PWM: 500-2500 microseconds
# Angle Range: 180 degrees
# Neutral Position: 1500 microseconds
  
### comments
### comment 2
# coment 3!
