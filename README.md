# aruco-navigation-robot

A Raspberry Pi robot that races through a sequence of ArUco beacons in a circular arena, built for PROJ103, a first-year team project at Télécom Paris (2023-2024).

Several robots share a 2.5 m radius arena with numbered beacons on its border. Each robot visits its three beacons in order, then the finish beacon, and moves only when a WebSocket master server gives it the turn.

## Results

No race timing or success rate was recorded. The camera calibration on 23 chessboard photos (1280x720, board found in 16) gives an RMS reprojection error of 0.52 px.

## Quick start

```bash
pip install -r requirements.txt
python calibration/calibrate_camera.py data/calibration_images   # copy the matrix into robot/camera.py
python master_server.py                                          # on the master Raspberry Pi
python race.py --robot-id 13 --route 4 6 2                       # on the robot
```

The motor code needs a Raspberry Pi with I2C and the [Waveshare Motor Driver HAT](https://www.waveshare.com/wiki/Motor_Driver_HAT). Calibration and detection (`python -m robot.detection`) also run on a laptop. The calibration photos are not versioned.

## Method

- Camera calibration with OpenCV on chessboard photos (9x6 inner corners, 25 mm squares).
- Beacon distance with `solvePnP` on the 4 corners of a 28 mm marker. The robot stops at 0.26 m.
- Viewing angle from the width/height ratio of the marker in the image.
- Visual servoing to approach a beacon, and plane geometry to aim at a point 0.2 m in front of the next one.
- Open-loop moves calibrated on the arena floor (no wheel encoders): 0.33 m/s at 50 % duty cycle, 4.6° per 50 ms rotation pulse.

## Structure

```
calibration/   camera calibration script
robot/         camera, detection, geometry, navigation, motors, protocol
hardware/      laser-cut chassis drawings
templates/     phone remote control page (web_control.py)
tests/         unit tests of the heading computation
```

## Team

Quentin Revillon, Manon Strasser, Albane Arifon, Vincent Hekimian (Télécom Paris, PROJ103 2023-2024).
Manon Strasser designed the laser-cut chassis, Albane Arifon worked on the slider page of the phone remote control, and Vincent Hekimian wrote the meeting notes (removed from the tree, kept in the history). Commits by `r2d2` were made from the robot's shared Raspberry Pi account. `robot/protocol.py` and `master_server.py` are refactored from the race protocol code common to all robots, imported in commit `bc33fc5`. The PWM driver is adapted from the Waveshare Motor Driver HAT example code.
