import pyb #dir(pyb)


# # setup of timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

# feedback
adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1
fdbck_S1 = adc_S1.read()
print(fdbck_S1)

ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=50000) # motor 1
# ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3, pulse_width=200000) # motor 2
# # PWM Tail Servos: 500-2500 microseconds, observed range is 50,000 to 200,000 with about 150 degree range

fdbck_S1 = adc_S1.read()
print(fdbck_S1)

# timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5, pulse_width=40000)
# # 40000 (abt 180 deg), 50000, 90000 (abt 100 deg), 150000 (abt 40 deg), 190000 (abt -10 deg), 200000 (abt -25 deg) 