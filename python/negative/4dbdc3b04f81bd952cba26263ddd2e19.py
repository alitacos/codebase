import requests
def get_google_learn_codelabs_metadata_and_contents_via_requests_and_bs4(url:str='')->requests.models.Response:
  
  try:
      return requests.get(url)
  except Exception as e:
      return None
