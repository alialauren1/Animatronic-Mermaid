import pyb #dir(pyb)

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

timerA = pyb.Timer(2, freq=20) #periodic freq of timer [Hz]
chA = timerA.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=100000) # PW in 10s of nano seconds I think

# servoA_min_theta = 0
# servoA_max_theta = 150
# servoB_min_theta = 0
# servoB_max_theta = 150