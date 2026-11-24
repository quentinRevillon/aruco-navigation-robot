"""Remote control of the robot from a phone: two sliders served by Flask-SocketIO.

The vertical slider sets the forward speed, the horizontal slider the turn
speed (halved for smoother steering); both return to 0 when released.

Usage (on the Raspberry Pi), then open http://<robot-ip>:5000 on a phone:
    python web_control.py
"""
from flask import Flask, render_template
from flask_socketio import SocketIO

from robot.motors import MotorDriver

TURN_SCALE = 0.5

app = Flask(__name__)
socketio = SocketIO(app)
motors = MotorDriver()
command = {"forward": 0, "turn": 0}


@app.route("/")
def index():
    """Serve the slider page."""
    return render_template("teleop.html")


@socketio.on("vertical")
def set_forward(data):
    """Update the forward speed (percent) from the vertical slider."""
    command["forward"] = int(data["value"])
    motors.move(**command)


@socketio.on("horizontal")
def set_turn(data):
    """Update the turn speed (percent) from the horizontal slider."""
    command["turn"] = int(data["value"]) * TURN_SCALE
    motors.move(**command)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
