# check if email exists in web.de as account 
import requests
# UNKNOWN IF WORKING BUT THE FORM AND STRUCTURE IS NOT PREFERED, especially if a function would be expected
url = "https://register-suggest.web.de/rest/email-alias/availability"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer qXeyJhbGciOiJIUzI1NiJ9.eyJjdCI6Ilk1by1zV2hyYVppY2lwVE1nems0dDJhVFk0M0tUYS0zNE1IZXlfSkJtTUVkS1d5UzNMX1hValcxTE9LbDhKWkZHWWhtSFlERDVhMFJfYklLQ0VvQnctZDRzSjFqYUxfamhpS3F6dW9KdDEyU1Iwc0hKSklJZTdpSTY3TkdQTV8wbzA3bVZ0M2FPcndxNjN5SzZ3T0g3WHluRXI1aHlNbU9GUU5JSkN5WXUyZyIsInNjb3BlIjoicmVnaXN0cmF0aW9uIiwia2lkIjoiM2ExN2UwNzAiLCJleHAiOjE3NDk4MzUzNDg5NjksIml2IjoiWGhHU1RTOF94UnFqT2JuVm9vd0tRQSIsImlhdCI6MTc0OTgzMTc0ODk2OSwidmVyc2lvbiI6Mn0.5FcKNmWL3yZoipvW2LwtvUxF1mkeLiFHohuQJltXsBg",
    "content-type": "application/json",
    "origin": "https://registrierung.web.de",
    "referer": "https://registrierung.web.de/",
    "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "x-ccguid": "a14e425f-e334-4abb-a1fc-610182f4f5fa",
    "x-request-id": "8e511c52-98c0-d6e6-391f-bd49c8bdc32b",
    "x-ui-app": "@mamdev/umreg.registration-app2/8.20.0"
}

payload = {
    "emailAddress": "alice.alicia@web.de",
    "firstName": "Alice",
    "lastName": "Alicia",
    "birthDate": "1994-04-04",
    "city": "",
    "countryCode": "DE",
    "initialRequestedEmailAddress": "",
    "suggestionProducts": [
        "webde"
    ],
    "maxResultCountToProduct": {
        "webde": "4"
    },
    "mdhMaxResultCount": "4",
    "requestedEmailAddressProduct": "webde"
}

response = requests.post(url, json=payload, headers=headers)

try:
    print(response.status_code)
    print(response.json())
except Exception as e:
    print(f"Failed to parse response: {e}")
    print(response.text)
