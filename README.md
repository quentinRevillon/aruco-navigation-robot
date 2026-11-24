# aruco-navigation-robot — Raspberry Pi robot racing between ArUco beacons

**aruco-navigation-robot** drives a two-wheeled Raspberry Pi robot through a sequence of ArUco
beacons placed around a circular arena, using a calibrated USB camera to measure the distance and
viewing angle of each beacon, and coordinates with other robots through a WebSocket master server.

## Overview

- **Context**: PROJ103, first-year team project at Télécom Paris (Sep 2023 – Feb 2024).
- **Task**: several robots share a 2.5 m radius arena with numbered ArUco beacons on its border. Each
  robot visits its three beacons in order, then the finish beacon, moving only when the master server
  gives it the turn.
- **Approach**: camera calibration on chessboard photos, ArUco pose estimation (OpenCV) for distance
  and viewing angle, visual servoing to approach a beacon, plane geometry to compute the heading to
  the next one, and open-loop motor moves calibrated on the floor (no wheel encoders).

## Results

No race timing or success rate was recorded. The camera calibration can be reproduced from the
original photos:

| Step | Data | Metric | Value |
|---|---|---|---|
| Camera calibration | 23 chessboard photos, 1280x720 (board found in 16) | RMS reprojection error | 0.52 px |

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Python 3.9 or later. The motor code needs a Raspberry Pi with I2C enabled and the
[Waveshare Motor Driver HAT](https://www.waveshare.com/wiki/Motor_Driver_HAT); calibration and
detection also run on a laptop.

## Quick start

Calibrate the camera from chessboard photos (9x6 inner corners, 25 mm squares), then copy the printed
matrix into `robot/camera.py`:

```bash
python calibration/calibrate_camera.py data/calibration_images
```

Check detection with a laptop webcam (prints the distance to the visible marker, `q` to quit):

```bash
python -m robot.detection
```

On the robot, drive to beacon 10, or run the full race once the master server is up:

```bash
python -m robot.navigation 10
python master_server.py                      # on the master Raspberry Pi
python race.py --robot-id 13 --route 4 6 2   # on our robot
python stop_motors.py                        # emergency stop
```

Drive the robot manually from a phone at `http://<robot-ip>:5000`:

```bash
python web_control.py
```

## Repository structure

- `calibration/calibrate_camera.py`: camera intrinsics from chessboard photos.
- `robot/camera.py`: camera access and calibrated intrinsics.
- `robot/detection.py`: ArUco detection, beacon distance (pose estimation) and viewing angle.
- `robot/geometry.py`: heading change from one beacon to the next on the arena circle.
- `robot/navigation.py`: visual servoing towards a beacon, with a search behaviour when it is lost.
- `robot/motion.py`, `robot/motors.py`, `robot/pca9685.py`: calibrated moves, differential drive, PWM driver.
- `robot/protocol.py`, `master_server.py`: WebSocket client and master server coordinating the robots.
- `race.py`: full race sequence.
- `web_control.py`, `templates/teleop.html`: phone remote control with two sliders.
- `hardware/`: laser-cut chassis drawings (SVG, DXF).
- `tests/test_geometry.py`: unit tests of the heading computation (`python -m pytest tests`).

## Method

- **Calibration**: OpenCV `calibrateCamera` on the chessboard corners refined to sub-pixel accuracy.
  The intrinsics were estimated on 1280x720 photos: capture frames at that resolution for metric distances.
- **Distance**: `solvePnP` (IPPE square) on the 4 corners of a 28 mm marker; the robot stops at 0.26 m.
- **Viewing angle**: `acos(width / height)` of the marker in the image, signed by which side looks taller.
- **Heading**: the robot aims at a point 0.2 m in front of the next beacon, computed from the beacon
  positions on the circle, the measured distance and viewing angle.
- **Moves**: 0.33 m/s at 50 % duty cycle for straight lines, 4.6° per 50 ms pulse for rotations,
  both measured on the arena floor.

## Data

The 23 calibration photos are not versioned. Place your own photos in `data/calibration_images/`
(gitignored).

## Team

Quentin Revillon, Manon Strasser, Albane Arifon, Vincent Hekimian (Télécom Paris, PROJ103 2023-2024).
Manon Strasser designed the laser-cut chassis. Commits by `r2d2` were made from the robot's shared
Raspberry Pi account. The PWM driver is adapted from the Waveshare Motor Driver HAT example code.
