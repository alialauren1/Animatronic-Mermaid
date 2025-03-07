import pyb #dir(pyb)
import time

## -------- servo 1 & 2 testing ---------
# # setup of timer
timer1 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# timer2 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]

ch1 = timer1.channel(3, pyb.Timer.PWM, pin=pyb.Pin.board.PB10) # motor 1
# ch2 = timer2.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3) # motor 2
adc_S1 = pyb.ADC(pyb.Pin.board.PA6)# create analog object from a pin for servo 1, on joint 2
adc_S2 = pyb.ADC(pyb.Pin.board.PA7)# create analog object from a pin for servo 2, on joint 3

# feedback
fdbck_S1 = adc_S1.read()
print(fdbck_S1)
time.sleep(3)

ch1.pulse_width(200000)
time.sleep(3)

fdbck_S1_ = adc_S1.read()
print(fdbck_S1_)

## ----------- servo 3 testing ------
# timer3 = pyb.Timer(2, freq=50) #periodic freq of timer [Hz]
# ch3 = timer3.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PA5, pulse_width=40000)
# # 40000 (abt 180 deg), 50000, 90000 (abt 100 deg), 150000 (abt 40 deg), 190000 (abt -10 deg), 200000 (abt -25 deg)
