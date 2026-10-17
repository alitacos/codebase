def check_if_email_exists_already_in_twitter_com( email: str='') -> bool:
    import requests
    if not email:
        email = ''
    url = f'https://api.x.com/i/users/email_available.json?email={email}'
    response = requests.get(url)
    try:
        dict_response =   response.json()
        data = {
            "error": None,
            "status_code": response.status_code,
            "valid": dict_response['valid'],
            "msg":dict_response['msg'],
            "taken":dict_response['taken']}
    except Exception as e:
        data =  {
            "error": str(e),
            "status_code": response.status_code,
            "valid": False,
            "msg":None,
            "taken":None}
    if not data:
        return False
    if data :
        return data.get('taken','') 
     

        
    
#example usage: 
#print(check_if_email_exists_already_in_twitter_com(email='f')) # output:{'error': None, 'status_code': 200, 'valid': False, 'msg': 'Diese E-Mail-Adresse ist ungültig.', 'taken': False}
#print(check_if_email_exists_already_in_twitter_com(email='anon@grr.la'))#out:{'error': None, 'status_code': 200, 'valid': False, 'msg': 'Diese E-Mail-Adresse wird bereits verwendet.', 'taken': True}
# error, not working. always returns None.. except is because of api limit... we need do dubble check before we label this