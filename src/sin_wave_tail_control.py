import time
import math 

# note: python uses radians for trig, but degrees elsewhere

#setup of variables
omega = math.radians(50) #deg/s to rad/s
A_hip = 22; # keep in degrees
A_knee = 18; # keep in degrees
phase_diff = math.radians(90) # phase difference between motors 1 and 2
k = 1 # NOTE: k will be conversion from theta(in deg) to PW values, add in when identified!

# create loop that runs continuously until script is stopped
while True:
    t = time.time()
    theta_hip = k*A_hip*math.sin(omega*t)
    theta_knee = k*A_knee*math.sin(omega*t - phase_diff)
    
    # uncomment to view value outputs
    print(f"Motor 1 Angle: {theta_hip:.2f}, Motor 2 Angle: {theta_knee:.2f}")
    
    time.sleep(0.1) # create delay so signal is not continuous. or do we want continuous idk?? plotted values look better with wait though
    



