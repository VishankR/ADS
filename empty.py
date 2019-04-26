import RPi.GPIO as gpio
import time
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
    print(diff)
    diff=count