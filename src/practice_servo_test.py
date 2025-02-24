import pyb #dir(pyb)

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

timer = pyb.Timer(2, freq=20) #periodic freq of timer [Hz]
ch2 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=100000)

  

