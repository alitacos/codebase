def get_response_by_query_gemini_via_apiKey(api_key: str='YOUR_NEW_API_KEY_HERE', query: str=None, model='gemini-2.0-flash') -> str:
    from google import genai
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=model, contents=query)
    return response.text
