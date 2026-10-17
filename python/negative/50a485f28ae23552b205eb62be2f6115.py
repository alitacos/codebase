def check_if_email_exists_in_twitter_as_boolean( email: str='') -> bool:
    import requests
    if not email:
        email = ''
    url = f'https://api.x.com/i/users/email_available.json?email={email}'
    response = requests.get(url)
    try:
        dict_response =   response.json()
        data = { "error": None, "status_code": response.status_code, "valid": dict_response['valid'], "msg":dict_response['msg'], "taken":dict_response['taken']}
    except Exception as e:
        data =  { "error": str(e), "status_code": response.status_code, "valid": False, "msg":None, "taken":None}
    if not data:
        return False
    if data :
        return data.get('taken','') 
     

        
    
#example usage: 
#print(check_if_email_exists_in_twitter_as_boolean(email='f')) # output:{'error': None, 'status_code': 200, 'valid': False, 'msg': 'Diese E-Mail-Adresse ist ungültig.', 'taken': False}
#print(check_if_email_exists_in_twitter_as_boolean(email='anon@grr.la'))#out:{'error': None, 'status_code': 200, 'valid': False, 'msg': 'Diese E-Mail-Adresse wird bereits verwendet.', 'taken': True}
#print(check_if_email_exists_in_twitter_as_boolean(email='alitakos90@gmail.com'))#out: {'error': None, 'status_code': 200, 'valid': True, 'msg': 'Verfügbar!', 'taken': False}
