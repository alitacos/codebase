def check_if_email_exists_in_cloudflare(email:str=None, cookies:dict={},headers:dict={},payload:dict={} ):
    #requires javascript -> selenium
    import requests

    url="https://dash.cloudflare.com/api/v4/user/create"

    payload = {
      "email": str(email).strip() if email else "",
      "password": "Bong4life8!",
      "mrk_optin": "false",
      "security_token": "MTc1MDE5MzU2NzJPSW40aUVxbVJTUEg3T0dUS3dsT1NGZllHVUJOeFZF",
      "method": "Onboarding: New_v2",
      "locale": "en-US",
      "mrktCheckboxDisplayed": "true",
      "hCaptchaDisplayed": "false",
      "cf_challenge_response": "0.hhUn4faXQatSi8ECnOELovaU7-NIWQT-5jAJdKt9tZRK_9ptRGAgF_f-aFBfEEDGyHZJuXn63QdWNE0JM9Q5ur9lsptdLp9AOFWlgjLZ3Pp4-pUJHMSToT9ozLxZsUFOqCftHJpxJshHX_hMwE2qT-NEQWG5PDiYYd1MM6lHR_Ksg7sZC-L_ScACN1vH5D7vUrlFy4ohqlfY567SARqXePZPPiZY5uZR6rMh5LtjGWyn7jbvidOwHr107EN9xjqqPduQPkNGaKJ8A510n4DNTVnuhmjyaLFlxSf_9Z9I035vzKCumGGAxVDsVkF-sXHQUpZq0xefxK3FE4qQOoBzbx9tRNUN4_E7aVER7oXZ2hHT0qV8pgmar3Tgc4sNiu8vZlmt1-HJsdtWex61Ttnp6fm3CwPgsHTrXJzOQCVPlgM8DAa4N7I8misB9zAowB2ZnaEAzimwJpzc2nL7MY5vGCBZQXS18d-U3LUadWdQtY0bAriT6ii7wfvxMdPySEKpXng9wPEZkf8NzOZCQAzs0tsQwMgJyM_I1SgIP6rdWfbSXedDtrB1dc1TI1eTHLPIkFNTJ3hNTJ2aQXoKyhbSMWwjJ3bTEdT1vIWsxq0iRduepQ8SvnieWO2yY0YyNhVPm0TuJZrjwMhSRA6zPx-icTHRxUN9QWTHWuE4Mnb0UNcnF7-j0bGECGtmfZXsBKn5__03-_9xDH2WuzM6jwzbip_eFL5NTIpcAltXsVHpJ4K4HuHdI7ypbMMbBOR_RedB04vFzfEDtC96tqW9J8C8pvfWA6LwXc57Nq4Qw7LvcBFVh8aw28jBN-O76PGaudMj-pWDnGJQtXEuCBzPzgfA44Bs6W9AdR5IbTnGaE5kYXyn3g4a4XNjr46uwLEW4GHI0lnttkAuvV0apRWXIwlStQ.rBn0QpM3b_YtgwIe7DEmkw.685fa7a56e7958fd047396d100350582866d5487168dcf51aa305ec7c9003423"
        }
    return  requests.post(url, cookies=cookies,headers=headers, params=payload)# or use data=payload???
response=check_if_email_exists_in_snapchat(email='anony@gmail.com')
response.text