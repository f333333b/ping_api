import requests

url = "https://api.uptimerobot.com/v2/newMonitor"
api_key = 'u2838980-393716cb75fc7f0f33948ffe'

testing_url = 'https://httpstat.us/502'

payload = f"api_key={api_key}&format=json&type=1&url={testing_url}&friendly_name=error_502"
headers = {
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)