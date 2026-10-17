import requests
from bs4 import BeautifulSoup

def check_if_username_exists_on_flickr_via_requests_and_bs4(url: str):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"}

    r = requests.get(url, headers=headers)

    # Check if status is 200 or 404 and handle accordingly
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        return {"status": r.status_code,"text": soup.get_text(separator="\n", strip=True)}
    else:
        return {"status": r.status_code,"text": None}


# Example:
if __name__ == "__main__":
    url = "https://www.flickr.com/people/anonymousd"
    result = check_if_username_exists_on_flickr_via_requests_and_bs4(url)

    print("Status:", result["status"])
    if result["text"]:
        print(result["text"][:1500])     # Print only the first 1500 chars of the text
    else:
        print("Page not found (status code 404).")