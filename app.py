import requests
import json
import jsonpath
from decimal import *
from methods import *

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
f = open("us_rate_history.txt", "r")
old_us_rate = f.read()

# Changing rate type to float for calculating purpose
old_us_rate_float = float(old_us_rate)

if current_us_rate_float == old_us_rate_float:
    print("Nothing changed")
else:
    f = open("us_rate_history.txt", "w+")
    f.write(current_us_rate[0])
    f.close()
    if current_us_rate_float < old_us_rate_float:
        # Make 2 number after the point
        getcontext().prec = 2
        # Calculating decreased difference
        dec_difference = (Decimal(old_us_rate_float) - Decimal(current_us_rate_float)) * 100

        # Change type to "int" and format number to get rid off zero
        dec_difference_int = int(dec_difference)
        formatNumber(dec_difference_int)

        data = {
            "text": "Курс доллара уменьшился на " + str(dec_difference_int) + " коп. и составляет: " + current_us_rate[0]}
    else:
        # Make 2 number after the point
        getcontext().prec = 2
        # Calculating increased difference
        inc_difference = (Decimal(current_us_rate_float) - Decimal(old_us_rate_float)) * 100

        # Change type to "int" and format number to get rid off zero
        inc_difference_int = int(inc_difference)
        formatNumber(inc_difference_int)

        data = {
            "text": "Курс доллара увеличился на " + str(inc_difference_int) + " коп. и составляет: " + current_us_rate[0]}
    # Send message to the Slack
    resp = requests.post(webhook, data=json.dumps(data))
