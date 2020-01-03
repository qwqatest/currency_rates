import requests
import json
import jsonpath

# https://hooks.slack.com/services/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

webhook = 'https://hooks.slack.com/services/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'
rates_url ='http://tech.money24.kharkov.ua/rates'

payload = {
	"appVersion": "1.1.0",
	"deviceId": "2D454D85-4CE4-4C09-ABE8-4CBA1D29C6AA",
}
# Getting rates info
response = requests.post(rates_url, data=json.dumps(payload))
# print(response.content)

# Getting US dollar rate from the response
json_response = json.loads(response.text)
current_us_rate = jsonpath.jsonpath(json_response, 'rates[11].buy')
print(current_us_rate[0])

current_us_rate_float = float(current_us_rate[0])
print(type(current_us_rate_float))

f = open("us_rate_history.txt","r")
old_us_rate = f.read()

old_us_rate_float = float(old_us_rate)
print(type(old_us_rate_float))

print("Старый курс: " + old_us_rate)
# print(type(old_us_rate[0]))
# print(type(current_us_rate))

if current_us_rate_float == old_us_rate_float:
	print("Ok")
else:
	f = open("us_rate_history.txt","w+")
	f.write(current_us_rate[0])
	f.close()

	data = {"text": "Курс доллара на сегодня: " + current_us_rate[0]}
	resp = requests.post(webhook, data=json.dumps(data))