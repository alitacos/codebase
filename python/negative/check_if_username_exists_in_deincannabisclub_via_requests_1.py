import requests
username ='test'

# The URL of the request
url = "https://www.deincannabisclub.com/?vx=1&action=auth.login"

# Headers to be included in the request
headers = {"Accept": "*/*","Accept-Encoding": "gzip, deflate, br, zstd","Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Origin": "https://www.deincannabisclub.com","Referer": "https://www.deincannabisclub.com/login/","Sec-CH-UA": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',"Sec-CH-UA-Mobile": "?0","Sec-CH-UA-Platform": '"Windows"',"Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-origin","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","X-Requested-With": "XMLHttpRequest"}

# Cookies to be included in the request
cookies = {"cmplz_policy_id": "27","age_gate": "18","cmplz_consented_services": "","cmplz_marketing": "allow","wp_consent_marketing": "allow","cmplz_statistics": "allow","wp_consent_statistics": "allow","cmplz_preferences": "allow","wp_consent_preferences": "allow","cmplz_functional": "allow","wp_consent_functional": "allow","cmplz_banner-status": "dismissed","_ga": "GA1.1.1592339776.1764967910","_ga_M6LCYVPKTS": "GS2.1.s1764967909$o1$g1$t1764968027$j47$l0$h0$",}

# Payload to be sent in the POST request
payload = {"username": username,"password": "0123456789","remember": "false","_wpnonce": "6597805ee0","_recaptcha": ""}

# Make the POST request with headers, cookies, and form data
response = requests.post(url, headers=headers, cookies=cookies, data=payload)

# Print the response (or handle it accordingly)
print(response.status_code)
print(response.text)  # This will display the response body
