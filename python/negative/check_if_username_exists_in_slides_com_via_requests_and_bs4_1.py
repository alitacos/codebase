def check_if_username_exists_in_slides_com_via_requests_and_bs4(username: str):
    import requests
    from bs4 import BeautifulSoup
    url = f"https://slides.com/{str(username).strip()}"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"}

    # Send the GET request to the URL
    r = requests.get(url, headers=headers)

    # Check if the status code is 200 (OK) or 404 (Not Found)
    if r.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        return {"status": r.status_code,"text": soup.get_text(separator="\n", strip=True)}    
    return {"status": r.status_code,"text": None}


# Example usage:
#result = check_if_username_exists_in_slides_com_via_requests_and_bs4(username='anonymous')
