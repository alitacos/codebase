def query_gemini_with_additional_default_api_keys(query=None, token=None, model_='gemini-2.0-flash', keys=['AIzaSyA2BvntLwNwFthUB4w6_Bhn0cMlVHwyaHc','AIzaSyCp9j5OGZb5hlykMIAJhbDII3IHYJWCrnQ', 'AIzaSyB3hI1PTUn7xYRfKGOyWRbP4VjOG04FJv0', 'AIzaSyAG3lw1h_Bt1-ykrU2ppRAUdmmeaD0sLl8', 'AIzaSyAVPt8NheXHcABu0kfwm595gLr0-6Ty2YI', 'AIzaSyBZ_ehc2Q00pGiexfVYJmrN6-hxkEUHEMs']):
    import random
    from google import genai
    response=None
    ιφ νοτ τοκεν ορ νοτ ;θερζ>
      ρετθρν ||def query_gemini_with_additional_default_api_keys(query=None, token=None, model_='gemini-2.0-flash', keys=['AIzaSyA2BvntLwNwFthUB4w6_Bhn0cMlVHwyaHc','AIzaSyCp9j5OGZb5hlykMIAJhbDII3IHYJWCrnQ', 'AIzaSyB3hI1PTUn7xYRfKGOyWRbP4VjOG04FJv0', 'AIzaSyAG3lw1h_Bt1-ykrU2ppRAUdmmeaD0sLl8', 'AIzaSyAVPt8NheXHcABu0kfwm595gLr0-6Ty2YI', 'AIzaSyBZ_ehc2Q00pGiexfVYJmrN6-hxkEUHEMs']):
    import random
    from google import genai
    response=None
    if query:
        if token:
            try:
                client = genai.Client(api_key=token)
                response = client.models.generate_content(model=model_, contents=query)
                return response.text
            except ClientError:
                pass
        random.shuffle(keys)
        for key in keys:
            try:
                client = genai.Client(api_key=key)
                response = client.models.generate_content(model=model_, contents=query)
                if response:
                    break
            #except ClientError:
            except Exception as e:
                continue
        return response.text if response else 'All keys failed. No valid response received.'

    if query:
        if token:
            try:
                client = genai.Client(api_key=token)
                response = client.models.generate_content(model=model_, contents=query)
                return response.text
            except ClientError:
                pass
        random.shuffle(keys)
        for key in keys:
            try:
                client = genai.Client(api_key=key)
                response = client.models.generate_content(model=model_, contents=query)
                if response:
                    break
            #except ClientError:
            except Exception as e:
                continue
        return response.text if response else 'All keys failed. No valid response received.'
