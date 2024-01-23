import motor
Motor = motor.MotorDriver()
import time as t

h_s = 30
v_s = 30
dt = 0.05
v = 0.2 #en m/s
    
def deplacement(dist):
    Motor.Move(vertical_speed=v_s, horizontal_speed=0)
    t.sleep(dist/v)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    return


def tourne(alpha):
    N = int(alpha/4.7)
    for i in range(N):
        Motor.Move(vertical_speed=0, horizontal_speed=h_s)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
    return

deplacement(1)
tourne(180)
deplacement(1)
tourne(180)
