def get_biological_species_dataset_from_gbif_dot_org_api_via_requests()->list:
    """
    Fetches biological species data from the GBIF (Global Biodiversity Information Facility) API.

    The function queries a predefined list of species IDs and collects unique results.

    Returns:
        list: A list of species data dictionaries retrieved from the GBIF API.
    """
    import requests

    species = []

    # Predefined GBIF species IDs to query
    for i in [1, 6, 52, 54, 216, 220, 797, 811, 1470, 7707728]:
        try:
            # Build API request URL
            url = f'https://api.gbif.org/v1/species/{i}'

            # Send HTTP request to GBIF API
            r = requests.get(url, timeout=10)

            # Raise exception for HTTP errors (4xx, 5xx)
            r.raise_for_status()

            # Parse JSON response
            data = r.json()

            # Add only unique results
            for item in data:
                if item not in species:
                    species.append(item)

        except requests.exceptions.RequestException as e:
            # Handle network-related errors (timeouts, connection issues, HTTP errors)
            print(f"Request error for ID {i}: {e}")

        except ValueError as e:
            # Handle JSON decoding errors
            print(f"JSON decode error for ID {i}: {e}")

        except Exception as e:
            # Catch any other unexpected errors without stopping execution
            print(f"Unexpected error for ID {i}: {e}")

    return species