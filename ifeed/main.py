#!/usr/bin/env python3.10

from config import *
from datetime import datetime
from functools import partial
from time import sleep
import asyncio
import logging
import os
import pytz
import requests
import RPi.GPIO as GPIO
import signal
import socket
import struct
import sys

logging.basicConfig(format='%(asctime)s - %(message)s', encoding='utf-8', level=level)

# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
def on_gpio_event(button, pwm, edge):
    try:
        if edge == None: edge = GPIO.input(button)
        logging.debug(f'button:{button} pwm:{pwm} edge:{edge}')
        # button released
        if edge == 0:
            pwm.ChangeDutyCycle(0)
            sleep(0.1)
            logging.info('finished dispensing')
        # button pressed
        else:
            logging.info('dispensing...')
            pwm.start(0)
            pwm.ChangeDutyCycle(duty_cycle)
    except:
        logging.exception('catastrophy!')
        pwm.ChangeDutyCycle(0)
        sleep(0.1)
        return False

    return True

def dispenser(pwms, runsecs, signum, frame):
    signame = signal.Signals(signum).name
    logging.debug(f'signame:{signame} signum:{signum} frame:{frame} pwms:{pwms} runsecs:{runsecs}')
    for pwm in pwms:
        try:
            success = False
            start = on_gpio_event(signum, pwm, 1)
            sleep(runsecs)
            finish = on_gpio_event(signum, pwm, 0)
            success = start and finish
            assert success
            if signum in alert_reset_signals:
                r = requests.get(alert_reset_url)
                logging.info(f'pwm:{pwm} signum:{signum} runsecs:{runsecs} dispensation:{success} url:{alert_reset_url} status_code:{r.status_code} headers:{r.headers} content:{r.content} text:{r.text}')
        except:
            logging.exception('catastrophy!')
            pwm.ChangeDutyCycle(0)
            sleep(0.1)

# https://stackoverflow.com/a/6556951/1559300
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue
            return socket.inet_ntoa(struct.pack("=L", int(fields[2], 16)))

def get_img_avg():
    img_avg = False
    try:
        gw = get_default_gateway_linux()
        r = requests.get(f'http://{gw}/')
        assert r.status_code == 200 and r.url.endswith('.png')
        img = ''.join(r.url.split('/')[-1:])
        r = requests.get(f'http://istream/{img}.json')
        assert r.status_code == 200 and r.json
        img_avg = float(r.json()[0])
        assert float(img_avg)
    except:
        pass
    return img_avg

# FIXME: there has got to be a more elegant way..
def toggle_light(lights):
    status = lights
    # off => on
    if lights in [0]:
        for shift in range(0,2):
            state = bool(int(GPIO.input(light_switch)))
            logging.debug(f'shift: {shift} state: {state}')
            GPIO.output(light_switch, not state)
            sleep(0.1)
        status = 1
    # on => off
    elif lights in [1]:
        for shift in range(0,4):
            state = bool(int(GPIO.input(light_switch)))
            logging.debug(f'shift: {shift} state: {state}')
            GPIO.output(light_switch, not state)
            sleep(0.1)
        status = 0
    # blinking => off
    if lights in [2]:
        for shift in range(0,2):
            state = bool(int(GPIO.input(light_switch)))
            logging.debug(f'shift: {shift} state: {state}')
            GPIO.output(light_switch, not state)
            sleep(0.1)
        status = 0
    else:
        logging.debug(f'lights: {lights} state: {state}')

    # record light state between container restarts
    try:
        file = '/tmp/balena/.pet'
        with open(file, 'w', encoding='utf-8') as f:
            print(status, file=f)
            logging.debug(f'{file}: {status}')
    except:
        pass

    return status

async def main():
    imgs_vector = []
    # https://stackoverflow.com/a/60728911/1559300
    global lights
    while True:
        utc_time = datetime.now(tz=pytz.utc)
        local_time = utc_time.astimezone(pytz.timezone(tz))
        if len(imgs_vector) > max_samples: imgs_vector = imgs_vector[-max_samples:]
        img_avg = get_img_avg()
        if img_avg: imgs_vector.append(img_avg)
        logging.info('utc_time: {} local_time: {} max_samples: {} len(imgs_vector): {} lights: {}'.format(
            utc_time.strftime(date_format),
            local_time.strftime(date_format),
            max_samples,
            len(imgs_vector),
            lights
        ))
        logging.debug('utc_time: {} local_time: {} imgs_vector: {}'.format(
            utc_time.strftime(date_format),
            local_time.strftime(date_format),
            imgs_vector
        ))

        # look at the last few samples to get brightness vector
        if len(imgs_vector) >= max_samples:
            sample_avg = sum(imgs_vector[-max_samples:]) / len(imgs_vector[-max_samples:])
            ambient_light_low = sample_avg < img_avg_low
            ambient_light_high = sample_avg >= img_avg_low
            logging.debug(f'ambient_light_low: {ambient_light_low} ambient_light_high: {ambient_light_high} sample_avg: {sample_avg}')

            if ambient_light_low and lights <= 0:
                lights = toggle_light(lights)

            if ambient_light_high and lights >= 1:
                lights = toggle_light(lights)

        await asyncio.sleep(log_interval)

if __name__ == '__main__':
    try:
        GPIO.setwarnings(gpio_warnings)

        # physical pin numbering scheme: https://i.stack.imgur.com/yHddo.png
        GPIO.setmode(GPIO.BOARD)

        # button inputs
        GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # servo motors
        GPIO.setup(dispenser1, GPIO.OUT)
        GPIO.setup(dispenser2, GPIO.OUT)

        # light trigger
        GPIO.setup(light_switch, GPIO.OUT)

        pwm1 = GPIO.PWM(dispenser1, pwm_frequency)
        pwm2 = GPIO.PWM(dispenser2, pwm_frequency)
        pwms = [pwm1, pwm2]

        # https://raspberrypi.stackexchange.com/a/104792/9812
        GPIO.add_event_detect(button1, GPIO.BOTH, callback=lambda x: on_gpio_event(button1, pwm1, None), bouncetime=bounce_time)
        GPIO.add_event_detect(button2, GPIO.BOTH, callback=lambda x: on_gpio_event(button2, pwm2, None), bouncetime=bounce_time)

        # dispense on SIGUSR signals
        signal.signal(signal.SIGUSR1, partial(dispenser, pwms, runsecs_snack))
        signal.signal(signal.SIGUSR2, partial(dispenser, pwms, runsecs_meal))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    except:
        logging.exception('catastrophy!')

    finally:
        # preserve lights status on exit
        try:
            with open(config_file, 'w', encoding='utf-8') as f: print(lights, file=f)
        except:
            pass

        GPIO.cleanup()
        loop.close()
