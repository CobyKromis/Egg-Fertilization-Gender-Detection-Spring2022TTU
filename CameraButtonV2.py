
from picamera import PiCamera
from time import sleep
from gpiozero import Button,LED,Servo
import sys
import pigpio
import EmailCode as ec

pi = pigpio.pi()

button = Button(17)
led = LED(21)
camera = PiCamera()
camera.rotation = 180

camera.start_preview()
sleep(2.5)
camera.stop_preview()
Egg = 1
pi.set_servo_pulsewidth(18, 0)
pi.set_PWM_frequency(18, 100)
print(pi.get_PWM_frequency(18))

def slowSpeed(cDC, dDC, steps):
    delta = (dDC - cDC) / steps
    while (cDC != dDC):
            
        cDC = cDC + delta
        if (cDC < 500):
            pi.set_servo_pulsewidth(18, 500)
        else:
            pi.set_servo_pulsewidth(18, cDC)
        sleep(.01)

while True:
    try:
        button.wait_for_press()
        led.on()
        camera.capture('/home/pi/Desktop/EggDatabase/Egg%04d.jpg' % Egg)
        Egg += 1
        print(pi.get_servo_pulsewidth(18))
        slowSpeed(pi.get_servo_pulsewidth(18), 2500, 250)
        sleep(1.5)
        print("1")
        camera.capture('/home/pi/Desktop/EggDatabase/Egg%04d.jpg' % Egg)
        Egg += 1
        print(pi.get_servo_pulsewidth(18))
        slowSpeed(pi.get_servo_pulsewidth(18), 2000, 50)
        sleep(1.5)
        print("2")
        camera.capture('/home/pi/Desktop/EggDatabase/Egg%04d.jpg' % Egg)
        Egg += 1
        print(pi.get_servo_pulsewidth(18))
        slowSpeed(pi.get_servo_pulsewidth(18), 1500, 50)
        sleep(1.5)
        print("3")
        camera.capture('/home/pi/Desktop/EggDatabase/Egg%04d.jpg' % Egg)
        Egg += 1
        print(pi.get_servo_pulsewidth(18))
        slowSpeed(pi.get_servo_pulsewidth(18), 1000, 50)
        sleep(1.5)
        print("4")
        Egg += 1
        led.off()
        print(pi.get_servo_pulsewidth(18))
        slowSpeed(pi.get_servo_pulsewidth(18), 0, 100)
        print("finished")
        sleep(3)
        ec.update(ec.RECEIVER,ec.SUBJECT,ec.MAIL_CONTENT)
        
    except KeyboardInterrupt:
        print ("Camera mode closed")
        sys.exit(1)
    


