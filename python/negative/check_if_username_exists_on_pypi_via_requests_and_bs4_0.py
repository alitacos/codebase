import requests
from bs4 import BeautifulSoup

def check_if_username_exists_on_pypi_via_requests_and_bs4(url: str):
    # Set custom headers to simulate a real browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}

    # Send GET request to the user profile URL
    response = requests.get(url, headers=headers)

    # Check if the response status is 200 (OK)
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for the presence of text indicating user existence or not
        if "No such user" in soup.get_text():
            return {"status": 404,"message": "User does not exist."}
        else:
            return {"status": 200,"message": "User exists."}
    
    # Check if the status code is 404 (User not found)
    elif response.status_code == 404:
        return {"status": 404,"message": "User does not exist."}

    # If it's neither 200 nor 404, return unknown
    else:
        return {"status": "unknown","message": f"Unexpected status: {response.status_code}"}

# Example usage
if __name__ == "__main__":
    url = "https://pypi.org/user/anonymous/"  # Replace with the desired PyPI user URL
    result = check_if_username_exists_on_pypi_via_requests_and_bs4(url)

    # Print the status and message
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")