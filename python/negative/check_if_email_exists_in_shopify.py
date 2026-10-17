def check_if_email_exists_in_shopify(email:str=None, driver=None, quit=False):
    #requires javascript -> use selenium
 

    url="https://accounts.shopify.com/lookup"

     
 
    
#send via selenium the email


#if Redirects to signup means that email is available
#if Redirects to Login means unavailable
  