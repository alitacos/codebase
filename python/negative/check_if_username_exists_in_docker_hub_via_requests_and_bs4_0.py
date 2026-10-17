def check_if_username_exists_in_docker_hub_via_requests_and_bs4(username: str='')->dict:
    import requests
    from bs4 import BeautifulSoup
    # Set custom headers to mimic a real browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
    url = f"https://hub.docker.com/u/{str(username).strip()}/"
    # Send the GET request to the Docker Hub user profile URL
    response = requests.get(url, headers=headers)

    # Check for status code 200 (OK) or 404 (Not Found)
    if response.status_code == 200:
        # If user exists, return status 200 and the soup text of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        return {"status": 200,"url": url,"soup_text": soup.get_text(separator="\n", strip=True)}
    elif response.status_code == 404:
        # If page not found, return status 404
        return {"status": 404,"url": url,"soup_text": "User not found."}
    else:
        # If other status codes (e.g., 301, 503, etc.), return the status code
        return {"status": response.status_code,"url": url,"soup_text": f"Unexpected status: {response.status_code}"}

# Example usage
#result = check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='anonymous')
#print(result)