import pyb #dir(pyb)

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

# timer = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# ch2 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=50000) # PW in 10s of nano seconds I think
# # PWM Tail Servos: 500-2500 microseconds, observed range is 50,000 to 200,000 with about 150 degree range
# # PWM Hip Servo: Observed range is 40,000 to 200,000 with about 190 degree range


# # setup of timer
# timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=200000) # motor 1
# ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3, pulse_width=200000) # motor 2

timer3 = pyb.Timer(8, freq=50)
ch3 = timer3.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PC7, pulse_width=100000)
# 50000, 90000, 
# 
# adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1
# fdbck_S1 = adc_S1.read()
# 
# print(fdbck_S1)
# at 200,000, ADC = 3364
# at 50,000, ADC = 385
# therefore, 