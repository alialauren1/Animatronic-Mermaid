import pyb #dir(pyb)

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

timerA = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
chA = timerA.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=100000) # PW in 10s of nano seconds I think
# 
# timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3, pulse_width=50000) # BB3 IS D3

# timer3 = pyb.Timer(2, freq=	0.1, prescaler = 0) #periodic freq of timer [Hz]
# ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5) # hip to body, joint 1
# ch3.pulse_width(50000)

# servoA_min = 40000
# servoA_max = 150000