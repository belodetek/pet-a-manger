import os

date_format = os.getenv('DATE_FORMAT', '%H:%M %Z')
gpio_warnings = bool(int(os.getenv('GPIO_WARNINGS', '0')))
level = os.getenv('LOG_LEVEL', 'INFO')
tz = os.getenv('TZ', 'US/Pacific')

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

# int(signal.SIGUSR2)
alert_reset_signals = [int(s) for s in os.getenv('IFEED_ALERT_RESET_SIGNALS', '12').split(',')]
alert_reset_url = os.getenv('IFEED_HEARTBEAT_URL')
bounce_time = int(os.getenv('IFEED_BOUNCE_TIME', '100'))
button1 = int(os.getenv('IFEED_BUTTON1_GPIO', '16'))
button2 = int(os.getenv('IFEED_BUTTON2_GPIO', '22'))
dispenser1 = int(os.getenv('IFEED_PWM1_GPIO', '3'))
dispenser2 = int(os.getenv('IFEED_PWM2_GPIO', '7'))
log_interval = int(os.getenv('IFEED_LOG_INTERVAL_SECS', '60'))
runsecs_meal = float(os.getenv('IFEED_MEAL_RUNSECS', '1.1'))
runsecs_snack = float(os.getenv('IFEED_SNACK_RUNSECS', '0.2'))
