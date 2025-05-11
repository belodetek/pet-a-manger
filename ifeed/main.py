#!/usr/bin/python3

import asyncio
import logging
import os
import signal
import threading
from datetime import datetime
from functools import partial
from time import sleep

import pytz
import requests
from config import *
from flask import Flask, jsonify, make_response, request, send_from_directory
from RPi import GPIO

app = Flask(__name__)

logging.basicConfig(format="%(asctime)s - %(message)s", encoding="utf-8", level=level)

GPIO.setwarnings(gpio_warnings)

# physical pin numbering scheme: https://i.stack.imgur.com/yHddo.png
GPIO.setmode(GPIO.BOARD)

# button inputs
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# servo motors
GPIO.setup(dispenser1, GPIO.OUT)
GPIO.setup(dispenser2, GPIO.OUT)

PWM1 = GPIO.PWM(dispenser1, pwm_frequency)  # left
PWM2 = GPIO.PWM(dispenser2, pwm_frequency)  # right
PWMS = {"left": PWM1, "right": PWM2}  # both

# https://raspberrypi.stackexchange.com/a/104792/9812
GPIO.add_event_detect(
    button1,
    GPIO.BOTH,
    callback=lambda x: on_gpio_event(button1, PWM1, None),
    bouncetime=bounce_time,
)
GPIO.add_event_detect(
    button2,
    GPIO.BOTH,
    callback=lambda x: on_gpio_event(button2, PWM2, None),
    bouncetime=bounce_time,
)


# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/
def on_gpio_event(button, pwm, edge):
    try:
        if edge is None:
            edge = GPIO.input(button)
        logging.debug("button:{%s} pwm:{%s} edge:{%s}", button, pwm, edge)
        # button released
        if edge == 0:
            pwm.ChangeDutyCycle(0)
            sleep(0.1)
            logging.info("finished dispensing")
        # button pressed
        else:
            logging.info("dispensing...")
            pwm.start(0)
            pwm.ChangeDutyCycle(duty_cycle)
    except:
        logging.exception("catastrophy!")
        pwm.ChangeDutyCycle(0)
        sleep(0.1)
        return False

    return True


def dispenser(pwms, runsecs, signum, frame):
    try:
        signame = signal.Signals(signum).name
    except:
        signame = None
    logging.debug(
        "signame:{%s} signum:{%s} frame:{%s} pwms:{%s} runsecs:{%s}",
        signame,
        signum,
        frame,
        pwms,
        runsecs,
    )
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
                logging.info(
                    "pwm:{%s} signum:{%s} runsecs:{%s} dispensation:{%s} url:{%s} status_code:{%s} headers:{%s} content:{%s} text:{%s}",
                    pwm,
                    signum,
                    runsecs,
                    success,
                    alert_reset_url,
                    r.status_code,
                    r.headers,
                    r.content,
                    r.text,
                )
            sleep(5)
        except:
            logging.exception("catastrophy!")
            pwm.ChangeDutyCycle(0)
            sleep(0.1)


async def main():
    while True:
        utc_time = datetime.now(tz=pytz.utc)
        local_time = utc_time.astimezone(pytz.timezone(tz))
        logging.info(
            "utc_time:%s local_time:%s",
            utc_time.strftime(date_format),
            local_time.strftime(date_format),
        )
        await asyncio.sleep(log_interval)


def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response


@app.after_request
def after_request_func(response):
    return add_cors_headers(response)


@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


@app.route("/dispense", methods=["POST", "OPTIONS"])
def dispense():
    if request.method == "OPTIONS":
        response = make_response("", 200)
        return add_cors_headers(response)

    data = request.get_json(silent=True) or {}

    runsecs = float(data.get("runsecs"))
    if runsecs <= 0:
        return jsonify({"error": f"Invalid runsecs: {runsecs}"}), 400

    sides = data.get("side").split(",")
    pwms = [PWMS[side] for side in sides]
    if not pwms:
        return jsonify({"error": f"Invalid side(s): {sides}"}), 400

    try:
        dispenser(pwms, runsecs, signum=0, frame=None)
        return jsonify({"status": "success", "runsecs": runsecs, "sides": sides})
    except Exception as e:
        logging.exception("Dispensation failed")
        return jsonify({"status": "failure", "error": str(e)}), 500


def run_flask():
    app.run(host="0.0.0.0", port=5000, use_reloader=False)


if __name__ == "__main__":
    try:
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # dispense on SIGUSR signals
        signal.signal(
            signal.SIGUSR1, partial(dispenser, list(PWMS.values()), runsecs_snack)
        )
        signal.signal(
            signal.SIGUSR2, partial(dispenser, list(PWMS.values()), runsecs_meal)
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    except:
        logging.exception("catastrophy!")

    finally:
        GPIO.cleanup()
        if "loop" in locals():
            loop.close()
