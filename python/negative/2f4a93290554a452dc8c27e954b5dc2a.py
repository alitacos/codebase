def get_biological_species_dataset_from_gbif_dot_org_api_via_requests_simple_method()->list:
    import requests

    species = []

    for i in [1,6,52,54,216,220,797,811,1470, 7707728]:
        try:
            url = f'https://api.gbif.org/v1/species/{i}'
            r = requests.get(url, timeout=10)
            r.raise_for_status()

            data = r.json()

            # FIXED LOGIC: no unnecessary loop over dict
            if data not in species:
                species.append(data)

        except requests.exceptions.RequestException as e:
            print(f"Request error for ID {i}: {e}")

        except ValueError as e:
            print(f"JSON decode error for ID {i}: {e}")

        except Exception as e:
            print(f"Unexpected error for ID {i}: {e}")

    return species