import motor
Motor = motor.MotorDriver()
import time as t

h_s = 30
v_s = 30
dt = 0.05
v = 0.46 #en m/s
    
def deplacement(dist):
    v_s = 50
    v = 0.33
    Motor.Move(vertical_speed=v_s, horizontal_speed=0)
    t.sleep(dist/v)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    return


def tourne(alpha, sens_rota):
    N = int(alpha/4.6)
    for i in range(N):
        Motor.Move(vertical_speed=0, horizontal_speed=h_s * sens_rota)
        t.sleep(dt)
        Motor.Move(vertical_speed=0, horizontal_speed=0)
        t.sleep(dt)
    return


if __name__ == "__main__":

    deplacement(1)
    tourne(180)
    deplacement(1)
    tourne(180)
    for i in range(6):
        deplacement(0.5)
        tourne(60)
