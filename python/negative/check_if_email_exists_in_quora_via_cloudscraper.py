#ModuleNotFoundError                
# requires additional modification like exceptions handling, error handling, retries, typehint ...


def check_if_email_exists_in_quora_via_cloudscraper(email):
    import cloudscraper
    url = 'https://de.quora.com/graphql/gql_para_POST?q=SignupEmailForm_validateEmail_Query'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' 
                      '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        # add other necessary headers here
    }
    payload = {
        "queryName": "SignupEmailForm_validateEmail_Query",
        "variables": {
            "email": email.strip() if email else ""
        },
        "extensions": {
            "hash": "1db80096407be846d5581fe1b42b12fd05e0b40a5d3095ed40a0b4bd28f49fe7"
        }
    }
    
    scraper = cloudscraper.create_scraper()  # handles Cloudflare
    response = scraper.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

#Example usage:
#result = check_if_email_exists_in_quora("test@example.com")
#print(result)#{'error': 'Request failed with status code 400'}
