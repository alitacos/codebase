import requests
from bs4 import BeautifulSoup
def return_wikipedia_page_bs4_soup_object_without_checking_upper_lower_for_term_by_language_using_requests(term:str='',lancode:str='en',verbose:bool=False)->BeautifulSoup:
    try: # requires additional optimization for lancodes, so it always checks if langcode is really a langcode else find the langcode based on the term´s language . but for now it works
        # also is missing a method to rewrite spaces into valid url´s
        langcode = langcode if langcode and len(langcode) == 2 and isinstance(langcode,str) else 'en'
        if isinstance(term,(bytes,bytearray)):
            term = term.decode(encoding='utf-8',errors='ignore')
        url = f"'https://{langcode}.wikipedia.org/wiki/'{str(term).strip()}"
        req = requests.get(url)
        soup =  BeautifulSoup(req.content,'html.parser')
        return soup 
    except Exception as e:
        if verbose:
            print(str(e))
        return None
        
#example usage:  
#return_wikipedia_page_bs4_soup_object_without_checking_upper_lower_for_term_by_language_using_requests(term='Currency_symbol',lancode='de',verbose=False)
#return_wikipedia_page_bs4_soup_object_without_checking_upper_lower_for_term_by_language_using_requests(term='currency_symbol',lancode='ru',verbose=False)
#return_wikipedia_page_bs4_soup_object_without_checking_upper_lower_for_term_by_language_using_requests(term='Currency symbol',lancode='en',verbose=False)

