def get_url_of_image_for_flags_of_given_potential_city_and_country_name_via_timeanddate_api(country:str='',city:str='')->str:
    if not country and not city:
        return ''
    try:
        if city:
            url =f'https://www.timeanddate.com/scripts/completion.php?query={str(city).strip()}'# 
        if not city and country:
            url =f'https://www.timeanddate.com/scripts/completion.php?query={str(country).strip()}'# 
        import requests
        req = requests.get(url)
        raw = req.text
        lines = raw.split('\n')
        items = [i.split('\t') for i in lines]
        flags = []
        for item in items:
            if city:
                if str(city).strip().lower() in item.lower():
                    place = item[4]
                    if str(city).strip().lower() == place.strip().lower():
                        country_ = item[-2]
                        flag_url = item[-1]
                        if country_:
                            if country:
                                if country_.strip().lower() == str(country).strip().lower():
                                    if flag_url:
                                        flags.append(flag_url.strip())
                            if not country:
                                if flag_url:
                                    flags.append(flag_url.strip())
            if not city:
                country_ = item[-2]
                flag_url = item[-1]
                if country:
                    if country_.strip().lower() == str(country).strip().lower():
                        if flag_url:
                            flags.append(flag_url.strip())
        if flags:
            flags = sorted(set([str(i).strip() for i in flags if i]))
            if flags:
                return flags
            else:
                return []
    except Exception as e:
        if verbose:
            print(str(e))
        return ''


#example usage:
#get_url_of_image_for_flags_of_given_potential_city_and_country_name_via_timeanddate_api(country='Germany',city='Stuttgart',verbose=False)
#get_url_of_image_for_flags_of_given_potential_city_and_country_name_via_timeanddate_api(country='',city='Waschington, D.C',verbose=False)
#get_url_of_image_for_flags_of_given_potential_city_and_country_name_via_timeanddate_api(country='Italy',city='',verbose=False)

