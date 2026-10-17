def check_email_info_in_pastebin_via_requests_over_google_search(email):
	search = ("site:pastebin.com \"{}\"".format(email))
	try:
		googleText, googleLink = Google(search=search, userAgent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.96 Safari/537.36")
		print(googleLink,googleText)
        #googleLinks = googleText
		
		for i in googleLink:
			pastebin_check(i, email)

	except:
		print("[!] Error or no pastebin link Found.".replace('!',Fore.RED+'!'+Fore.RESET))
#example usage:
#result = check_email_info_in_pastebin_via_requests_over_google_search('anonymous@gmail.com')
#print(result)