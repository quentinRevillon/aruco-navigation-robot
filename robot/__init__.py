"""Raspberry Pi robot that navigates between ArUco beacons.

Modules:
    camera      camera access and calibrated intrinsics
    detection   ArUco detection, distance and viewing angle of a beacon
    geometry    heading change between two beacons of the arena
    pca9685     I2C PWM driver of the motor HAT
    motors      differential drive of the two DC motors
    motion      open-loop straight moves and on-the-spot turns
    navigation  visual servoing towards one beacon
    protocol    WebSocket client of the race master server
"""
