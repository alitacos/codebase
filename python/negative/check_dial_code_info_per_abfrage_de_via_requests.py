def check_dial_code_info_per_abfrage_de_via_requests(postalcode="70197",retries:int=3, delay:int=2)->dict:
    import requests
    from bs4 import BeautifulSoup
    import time
    for _ in range(retries):
        try:
            if not postalcode or not isinstance(postalcode,(str,int)) or not str(postalcode).strip().isdigit() or not len(str(postalcode).strip()) in [4,5]:
                return {"error":'invalid german postalcode',"status":None, "dial_code": None,"postcode": postalcode,"city": None,"bundesland": None}
            url = "https://www.abfragen.de/auskunft4.asp?plz=70197&abfragen.x=15&abfragen.y=18"
            params = {"plz":f'{int(str(postalcode).strip()):05d}'}
            r = requests.get(url, params=params)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content,'html.parser')
                # i need to get now the dialcode, postcode, city and Bundesland. how===
                # find all rows in the table
                rows = soup.find('body').find('div', class_='dienstlayout02').find('table').find_all('tr')
                # the second row contains the data
                data_row = rows[1]
                # get all <td> cells from the data row
                cells = data_row.find_all('td')
                # extract the text from each cell and strip whitespace
                dial_code = cells[0].get_text(strip=True)
                postcode = cells[1].get_text(strip=True)
                city = cells[2].get_text(strip=True)
                bundesland = cells[3].get_text(strip=True)
                # return or print as you want
                return {"error":False,"status":r.status_code,  "dial_code": dial_code,"postcode": postcode,"city": city,"bundesland": bundesland}
            last_error = 'unexpected status code'
            status_code = r.status_code
            time.sleep(delay)
            continue

        except Exception as e:
            last_error = str(e)
            status_code = None
    return {"error":last_error,"status":status_code "dial_code": None,"postcode": postalcode,"city": None,"bundesland": None}

# Example usage:
# result = check_dial_code_info_per_abfrage_de_via_requests("70197")
# print(result)