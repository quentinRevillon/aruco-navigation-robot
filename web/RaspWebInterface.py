
import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO

import datetime
import motor_manuel
Motor = motor.MotorDriver()
vertical_speed = 0
horizontal_speed = 0

app=Flask(__name__)
socketio = SocketIO(app)
@app.route('/')
def index():
    
    #return render_template('rpi_index.html',**templateData)
    return render_template('curseurs.html')

@socketio.on('connect')
def connect():
    print('someone is  connected')

@socketio.on('vertical')
def change_vertical_value(data):
    # id = request.form['id']
    value = int(data["value"])
    print(f"Received value: {value}")
    global vertical_speed
    global horizontal_speed
    vertical_speed = value
    Motor.Move(vertical_speed, horizontal_speed)
    return "Value set successfully"

@socketio.on('horizontal')
def change_horizontal_value(data):
    # id = request.form['id']
    value = int(data["value"])
    print(f"Received value: {value}")
    global horizontal_speed
    global vertical_speed
    horizontal_speed = value*0.5
    Motor.Move(vertical_speed, horizontal_speed)

@socketio.on('autoPilot')
def launchAutoPilot(mode):
    import automatique
    print('je passe en mode auto')
    # Ici, vous pouvez ajouter le code pour contrôler les pins GPIO en fonction de la valeur

    return "Value set successfully"
                          
if __name__=='__main__':
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/


