import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

buzzer=40
GPIO.setup( buzzer, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

while True:
    if GPIO.input( buzzer ) == GPIO.HIGH:
        print( 'se presiono el boton' )
    else:
        print( 'no')
