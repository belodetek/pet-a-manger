#!/usr/bin/env python3.10

import os
import sys
import asyncio
import RPi.GPIO as GPIO
from time import sleep

# 1,000,000us / 50Hz = 20,000us
pwm_frequency = int(os.getenv('IFEED_PWM_FREQ', '50'))

# https://raspberrypi.stackexchange.com/a/108115
# https://cnc1.lv/PDF%20FILES/TD-8120MG_Digital_Servo.pdf
# https://www.aliexpress.com/item/1005003256573988.html
#
#   500us / 20,000us = 0.025 or  2.5 % dutycycle
# 1,000us / 20,000us = 0.05  or  5.0 % dutycycle
# 1,500us / 20,000us = 0.075 or  7.5 % dutycycle
# 2,000us / 20,000us = 0.1   or 10.0 % dutycycle
# 2,500us / 20,000us = 0.125 or 12.5 % dutycycle
duty_cycle = int(os.getenv('IFEED_DUTY_CYCLE', '5'))

bounce_time = int(os.getenv('IFEED_BOUNCE_TIME', '100'))
button1 = int(os.getenv('IFEED_BUTTON1_GPIO', '16'))
button2 = int(os.getenv('IFEED_BUTTON2_GPIO', '22'))
dispenser1 = int(os.getenv('IFEED_PWM1_GPIO', '3'))
dispenser2 = int(os.getenv('IFEED_PWM2_GPIO', '7'))

# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
def on_gpio_event(button, pwm):
    try:
        edge = GPIO.input(button)
        print('button: {} edge: {}'.format(button, edge))
        # button released
        if not edge:
            pwm.ChangeDutyCycle(0)
            sleep(0.1)
            print('finished dispensing')
            return
        # button pressed
        else:
            print('dispensing...')
            pwm.start(0)
            pwm.ChangeDutyCycle(duty_cycle)
    except Exception as e:
        print('catastrophy: {}'.format(e))
        print(sys.exc_info()[0])

if __name__ == '__main__':
    try:
        # physical pin numbering scheme: https://i.stack.imgur.com/yHddo.png
        GPIO.setmode(GPIO.BOARD)

        # button inputs
        GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # servo motors
        GPIO.setup(dispenser1, GPIO.OUT)
        GPIO.setup(dispenser2, GPIO.OUT)
        pwm1 = GPIO.PWM(dispenser1, pwm_frequency)
        pwm2 = GPIO.PWM(dispenser2, pwm_frequency)

        # https://raspberrypi.stackexchange.com/a/104792/9812
        GPIO.add_event_detect(button1, GPIO.BOTH, callback=lambda x: on_gpio_event(button1, pwm1), bouncetime=bounce_time)
        GPIO.add_event_detect(button2, GPIO.BOTH, callback=lambda x: on_gpio_event(button2, pwm2), bouncetime=bounce_time)

        loop = asyncio.get_event_loop()
        loop.run_forever()

    except Exception as e:
        print('catastrophy: {}'.format(e))
        print(sys.exc_info()[0])

    finally:
        GPIO.cleanup()
        loop.close()
