#ModuleNotFoundError    
# the functions seems not weel constructed and colorama is useless for the main purpose 
import colorama, requests, ScrapeSearchEngine
from ScrapeSearchEngine.SearchEngine import *
from colorama import Fore

def check_username_info_in_pastebin_via_requests(i, email):
	try:
		link = str(i).replace("https://pastebin.com/","https://pastebin.com/raw/")
		r = requests.get(link)
		data = r.text

		if email.lower() in data.lower() or email in data:
			print(Fore.GREEN+"> "+link)

	except:
		print("[!] Your adresse IP has banned, retry tomorrow or change your ip.".replace('!',Fore.RED+'!'+Fore.RESET))

#example usage:
#result = check_username_info_in_pastebin_via_requests('', 'alitakos90')
#print(result)