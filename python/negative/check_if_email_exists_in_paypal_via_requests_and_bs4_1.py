def check_if_email_exists_in_paypal_via_requests_and_bs4(email:str=None, cookies:dict={},headers:dict={},payload:dict={} ):
    #requires javascript -> selenium
    import requests

    url='https://www.paypal.com/welcome/rest/v1/emailExists'

    payload={
      "email": str(email).strip() if email else "",
      # try to run below with empty or any string
         }
    #responses =[{"emailExists":true,"valid":true} , {"emailExists":false,"valid":true}]
   # i forgot the cookies and headers. need to retry, before testing with selenium
      #"fn_sync_data": "%7B%22SC_VERSION%22%3A%222.0.4%22%2C%22syncStatus%22%3A%22data%22%2C%22f%22%3A%22f32adfd04bc111f088f9d3299be41f3c%22%2C%22s%22%3A%22t_s%22%2C%22chk%22%3A%7B%22ts%22%3A1750195685057%2C%22eteid%22%3A%5B4375019100%2C1332321489%2C8337712056%2C3280156111%2C-14419201146%2C13294898848%2C-9011941255%2C-6502331780%5D%2C%22tts%22%3A24%7D%2C%22dc%22%3A%22%7B%5C%22screen%5C%22%3A%7B%5C%22colorDepth%5C%22%3A24%2C%5C%22pixelDepth%5C%22%3A24%2C%5C%22height%5C%22%3A864%2C%5C%22width%5C%22%3A1536%2C%5C%22availHeight%5C%22%3A816%2C%5C%22availWidth%5C%22%3A1536%7D%2C%5C%22ua%5C%22%3A%5C%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F137.0.0.0%20Safari%2F537.36%5C%22%7D%22%2C%22wv%22%3Afalse%2C%22web_integration_type%22%3A%22WEB_REDIRECT%22%2C%22cookie_enabled%22%3Atrue%2C%22d%22%3A%7B%22rDT%22%3A%2247056%2C46262%2C46126%3A6071%2C5286%2C5185%3A26553%2C25786%2C25673%3A16245%2C15554%2C15453%3A46971%2C46293%2C46127%3A11103%2C10432%2C10264%3A26470%2C25801%2C25632%3A46947%2C46293%2C46124%3A26448%2C25801%2C25631%3A52039%2C51416%2C51247%3A36642%2C36046%2C35887%3A46873%2C46292%2C46116%3A46825%2C46291%2C46138%3A10940%2C10427%2C10263%3A41668%2C41163%2C41000%3A21174%2C20669%2C20508%3A10926%2C10423%2C10263%3A16142%2C15995%2C17159%3A31511%2C31361%2C30745%3A36636%2C36468%2C35879%3A18335%2C23%22%7D%7D"
    
    response= requests.post(url, cookies=cookies,headers=headers, params=payload)# 
    return response
#example usage:

#res= check_if_email_exists_in_paypal(email='anonQgmail.com')
#try:
#    print(res.json())
#except Exception as e:
    
#    from bs4 import BeautifulSoup
#    soup= BeautifulSoup(res.content,'html.parser')
#    print( soup.find('body').text)
    