
import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request
import datetime
import motor
Motor = motor.MotorDriver()
vertical_speed = 0
horizontal_speed = 0

app=Flask(__name__)
    
@app.route('/')
def index():
    
    #return render_template('rpi_index.html',**templateData)
    return render_template('curseurs.html')

@app.route('/vertical', methods=['POST'])
def change_vertical_value():
    # id = request.form['id']
    value = int(request.form['value'])
    print(f"Received value: {value}")
    global vertical_speed
    global horizontal_speed
    vertical_speed = value*0.5
    Motor.Move(vertical_speed, horizontal_speed)
    return "Value set successfully"

@app.route('/horizontal', methods=['POST'])
def change_horizontal_value():
    # id = request.form['id']
    value = int(request.form['value'])
    print(f"Received value: {value}")
    global horizontal_speed
    global vertical_speed
    horizontal_speed = value*0.5
    Motor.Move(vertical_speed, horizontal_speed)

@app.route('/stop', methods=['POST'])
def stop():
    Motor

    # Ici, vous pouvez ajouter le code pour contrôler les pins GPIO en fonction de la valeur

    return "Value set successfully"
                          
if __name__=='__main__':
    
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
