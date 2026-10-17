def check_if_email_exists_in_nvidia_via_requests(
    email: str,
    cookies: dict = None,
    headers: dict = None,
    payload: dict = None
):
    import requests
    url = "https://accounts.nvgs.nvidia.com/api/1/frontend/oauth/account/"

    # Default headers if not provided
    if headers is None:
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzZSI6IlFYSUEiLCJ0b2tlbklkIjoiMTM4NDU3NzkwODYzMzgwMDcwNCIsIm90IjoiMTM4NDU3NzkwODY1NDc3MjIyNCIsImV4cCI6MTc1MDI2NTg5NywiaWF0IjoxNzUwMTc5NDk3LCJqdGkiOiIyMjAwMDlhNy0xNGFlLTRhZmEtODJhNy1iMjk4M2E5NmU5MDEifQ.DCy6v3ASjjYs_HreweR2ysbSFBAUFV68YMzIU5YR1F4",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Content-Type": "application/json"
        }

    # Default cookies if not provided
    if cookies is None:
        cookies = {
            "MainAuth_1": "l07fpzqt-ve3q2pEiiGmedYNF1hgdWyw",
            "MainAuth_2": "bm3ysxxFipM7dlb8Nrd5bLClRScNOhBW",
            "at_check": "true",
            # ... (truncate or add all relevant cookies here if needed)
        }

    # Payload (POST data)
    if payload is None:
        payload = {
            "email": str(email).strip() if email else "",
            "rememberLogin": "true",
            "deviceId": "32c04xa42joFm5Bz"  # You can randomize this if needed
        }

    try:
        response = requests.post(url, cookies=cookies, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()       # Return parsed JSON
    except requests.RequestException as e:
        print(f"[Error] Request failed: {e}")
        return None


#example usage:
#check_if_email_exists_in_nvidia_via_requests(email='anonymous@gmail.com')#[Error] Request failed: 404 Client Error: Not Found for url: https://accounts.nvgs.nvidia.com/api/1/frontend/oauth/account/
