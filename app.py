from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as gpio
import time
import threading
import time
import json
gpio.setwarnings(False)
# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO(app)
b = False
pin3=18
gpio.setmode(gpio.BOARD)
gpio.setup(pin3,gpio.OUT)
bottles = 0
t1=True
t2=True
message=""
diff2=0

def bottle_count():
    global bottles
    global t2
    check_var = 0b10
    initial_var = 0b10
    pin = 13
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin, gpio.IN)
    while True:
        if t2:
            i = gpio.input(pin)
            n = initial_var | i
            initial_var = initial_var & 0b00
            i = i << 1
            initial_var = initial_var | i
            if n == check_var:
                bottles=bottles+1
            print(bottles)
        else:
             break;

def counting_number():
    global bottles
    global t1
    global message
    global diff2
    start2=0
    diff=0
    pin1=16
    pin2=15
    count=0
    li=[0,3,1,2,1,1,0,2,3,3,2,0,1,2,1,3,0]
    speed=0
    pstpo=0b00
    count=0
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin1,gpio.IN)
    gpio.setup(pin2,gpio.IN)
    while True:
            if t1:
                start = time.time()
                while((start2-start)<=1):
                     i1=gpio.input(pin1)
                     i1=i1 << 1
                     i3=gpio.input(pin2)
                     cst=i1 | i3
                     if(pstpo != cst):
                         p=(pstpo << 2) | cst
                         count=count + li[p]
                     pstpo=cst
                     start2=time.time()
                diff=count-diff
                diff2=diff
                print(message+" "+str(diff)+" "+str(bottles))
                socketio.emit('my_response_function_from_app.py', {'message': message, 'message2': diff, 'message3':bottles, 'processState': True})
                diff=count
            else:
                socketio.emit('my_response_function_from_app.py', {'message': message, 'message2': 0, 'message3':bottles, 'processState': False})
                break;

@app.route('/')
def hello():
    # result = multiprocessing.Value('d', 0.0)
    return render_template('./ChatApp.html')


@socketio.on('emitEventFromHTML')
def handle_my_custom_event(datainjson):
    global t1
    global t2
    global message
    global diff2
    message=datainjson["message"]
    ps = datainjson.get('processState')
    print('recived my event: ' + str(datainjson))
    if(datainjson["message"]=="Machine Started"):
        gpio.output(pin3,1)
        if(ps == False):
            t1=True
            t2=True
            p1 = threading.Thread(target=counting_number)
            p2 = threading.Thread(target=bottle_count)
            p1.start()
            p2.start()
    if(datainjson["message"]=="Machine Stopped"):
        gpio.output(pin3,0)
        t1=False
        t2=False
        socketio.emit('my_response_function_from_app.py', {'message': message, 'message2': 0, 'message3':bottles, 'processState': False})


if __name__ == '__main__':
    socketio.run(app, port=5000, host='0.0.0.0')
