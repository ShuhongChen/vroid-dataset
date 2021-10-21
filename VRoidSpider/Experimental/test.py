import requests



res = requests.get(
    "https://hub.vroid.com/api/character_models/6056393358183577091/view",
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-api-version": "10"
    }
)


print("\n\n")

print("Status Code:")
print(res.status_code)

print("Response Content:")
print(res.json)

print("\n\n")