import RPi.GPIO as gpio
bottles=0
check_var = 2
initial_var = 0b10
pin = 11
gpio.setmode(gpio.BOARD)
gpio.setup(pin, gpio.IN)
while True:
    i = gpio.input(pin)
    #print(i)
    n = initial_var | i
    initial_var = initial_var & 0b00
    i = i << 1
    initial_var = initial_var | i
    if n == check_var:
        bottles=bottles+1
    print(bottles)