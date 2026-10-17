def check_ycombinator_userame_via_requests_and_bs4(url: str):
    import requests
    from bs4 import BeautifulSoup
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}

    # Send GET request to the user profile URL
    response = requests.get(url, headers=headers)

    # Check if the response status is 200 (OK)
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for the text that indicates if the user does not exist
        if "No such user." in soup.get_text():
            return {"status": 404,"message": "User does not exist."}
        else:
            return {"status": 200,"message": "User exists."}
    else:
        # If status code is not 200, return unknown
        return {"status": "unknown","message": f"Unexpected status: {response.status_code}"}

# Example usage
if __name__ == "__main__":
    url = "https://news.ycombinator.com/user?id=anonymous"  # Replace with the desired YCombinator user URL
    result = check_ycombinator_userame_via_requests_and_bs4(url)

    # Print the status and message
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
#Message: User does not exist.
#Message: User exists.
