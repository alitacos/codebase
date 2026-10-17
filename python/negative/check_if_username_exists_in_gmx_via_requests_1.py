import requests
import json
username = 'alitakos90'
#username = 'anonymous'

# The URL of the request
url = "https://register-suggest.gmx.net/rest/email-alias/availability"

# Headers to be included in the request
headers = {"Accept": "application/json, text/plain, */*","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7","Authorization": "Bearer qXeyJhbGciOiJIUzI1NiJ9.eyJjdCI6IjJiVGd3SlpJdEhEWWw4LVFRQkRQSThna2lWcTNOblFGcGpabktGSzZqWG9YR1BwWnlfd2tPMkJVRFREY1JWVWpaSkdkWC1aYzlHbkhJUlNjTkxNa2lJYU9EdU1zTi1JUWM5RjdfRTVNNFVyd1ZOMmRkWXpmczNLakdZUnZrS3JBTFZxSzJnTHBfMjBERWQtb2pjeEVWY2ttaWNkeEFzUjdfUTBlZFhDb0Q5ayIsInNjb3BlIjoicmVnaXN0cmF0aW9uIiwia2lkIjoiM2E0Mjg1MDAiLCJleHAiOjE3NjQ5NzI2NTE1NjYsIml2IjoiaWw5V3hVbVBHQU1vejFXVWtBN3lGdyIsImlhdCI6MTc2NDk2OTA1MTU2NiwidmVyc2lvbiI6Mn0.6UehMtd24CrDK0UYGkylHpVO3gvAw00PUaAx6grlnlI","Content-Type": "application/vnd.ui.mam.suggestion.creation-v1+json;charset=utf-8","Origin": "https://registrierung.gmx.net","Referer": "https://registrierung.gmx.net/","Sec-CH-UA": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',"Sec-CH-UA-Mobile": "?0","Sec-CH-UA-Platform": '"Windows"',"Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-site","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","X-CCGUID": "35bf7e55-a172-4b0d-9eae-bf19562ac20f","X-Request-ID": "bfdab3f2-0f87-3461-2f50-13cc0258d346","X-UI-App": "@mamdev/umreg.registration-app2/8.31.0"}
# Payload to be sent in the POST request
payload = {"emailAddress": username.strip()+'@gmx.de',"firstName": "","lastName": "","birthDate": "","city": "","countryCode": "DE","initialRequestedEmailAddress": "","suggestionProducts": ["gmxnetFree", "gmxnetPro"],"maxResultCountToProduct": {"gmxnetFree": "4","gmxnetPro": "4"},"mdhMaxResultCount": "4","requestedEmailAddressProduct": "gmxnetFree"}

# Make the POST request with headers and payload
response = requests.post(url, headers=headers, json=payload)

# Print the response (or handle it accordingly)
print(response.status_code)
print(response.text)  # This will display the response body
