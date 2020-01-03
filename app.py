import requests
import json
import jsonpath


webhook = 'https://hooks.slack.com/services/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'
rates_url ='http://tech.money24.kharkov.ua/rates'

payload = {
	"appVersion": "1.1.0",
	"deviceId": "2D454D85-4CE4-4C09-ABE8-4CBA1D29C6AA",
}

response = requests.post(rates_url, data=json.dumps(payload))
print(response.content)

json_response = json.loads(response.text)
us_rate = jsonpath.jsonpath(json_response, 'summary.total_count_days')
