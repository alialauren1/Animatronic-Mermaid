import pyb #dir(pyb)

# FOR PB10, PWM 2/3 means 2 = timer number, 3 = channel

timer = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
ch2 = timer.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10, pulse_width=40000) # PW in 10s of nano seconds I think
# PWM Tail Servos: 500-2500 microseconds, observed range is 50,000 to 200,000 with about 150 degree range
# PWM Hip Servo: Observed range is 40,000 to 200,000 with about 190 degree range

adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1
fdbck_S1 = adc_S1.read()

print(fdbck_S1)
# at 200,000, ADC = 3364
# at 50,000, ADC = 385
# therefore, 