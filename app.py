
import requests
import json
import jsonpath
from decimal import *
from methods import *
import schedule
import os
import logging
import time
from datetime import datetime as dt
from slack import WebClient


def send_message():
    logging.basicConfig(level=logging.DEBUG)

    webhook = ''
    rates_url = 'http://tech.money24.kharkov.ua/rates'

    payload = {
    "appVersion": "1.1.0",
    "deviceId": "2D454D85-4CE4-4C09-ABE8-4CBA1D29C6AA",
    }
    # Getting rates info
    response = requests.post(rates_url, data=json.dumps(payload))


    # Getting US dollar rate from the response
    json_response = json.loads(response.text)
    current_us_rate = jsonpath.jsonpath(json_response, 'rates[11].buy')

    # Changing rate type to float for calculating purpose
    current_us_rate_float = float(current_us_rate[0])

    # Reading previous rate from the file
    f = open("us_last_rate.txt", "r")
    old_us_rate = f.read()
    f.close()

    # Changing rate type to float for calculating purpose
    old_us_rate_float = float(old_us_rate)

    if current_us_rate_float == old_us_rate_float:
        print("Nothing changed")
    else:
        f = open("us_last_rate.txt", "w+")
        f.write(current_us_rate[0])
        f.close()

        us_rate_history = open("us_rate_history.txt", "a+")
        us_rate_history.write('\n' + dt.now().strftime("%y-%m-%d, %H:%M") + ' - ' + current_us_rate[0])
        us_rate_history.close()

        if current_us_rate_float < old_us_rate_float:
            # Make 2 number after the point
            getcontext().prec = 2
            # Calculating decreased difference
            dec_difference = (Decimal(old_us_rate_float) - Decimal(current_us_rate_float)) * 100

            # Change type to "int" and format number to get rid off zero
            dec_difference_int = int(dec_difference)
            formatNumber(dec_difference_int)

            message = {
             "text": "Курс доллара уменьшился на " + str(dec_difference_int) + " коп. и составляет: " + current_us_rate[0]}
        else:
            # Make 2 number after the point
            getcontext().prec = 2
            # Calculating increased difference
            inc_difference = (Decimal(current_us_rate_float) - Decimal(old_us_rate_float)) * 100

            # Change type to "int" and format number to get rid off zero
            inc_difference_int = int(inc_difference)
            formatNumber(inc_difference_int)

            message = {
             "text": "Курс доллара увеличился на " + str(inc_difference_int) + " коп. и составляет: " + current_us_rate[0]}
            # Send message to the Slack
        requests.post(webhook, data=json.dumps(message))
# sendMessage()


schedule.every(600).seconds.do(lambda: send_message())

while True:
    schedule.run_pending()
    time.sleep(1)


