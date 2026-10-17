def get_location_information_dict_by_city_country_via_timeanddate_api(country:str='',city:str='',verbos:bool=False) -> list:
    try: 
        url ='https://www.timeanddate.com/scripts/completion.php'# 
        import requests
        outs = []
        if city:
            p={"query":city}
            req = requests.get(url,params=p)
            raw = req.text
            for line in lines:
                if city.lower() in line.lower():
                    item = line.split('\t')
                    try:
                        lines=raw.split('\n')
                        out_obj = {'clock_data_url':f'https://www.timeanddate.com/scripts/completion.php/{item[0]}','zone_json':f'https://www.timeanddate.com/scripts/completion.php?mode=tzmappos&p1={item[1]}','iso_alpha_2_code':item[2],'country_state_code':item[3],'place':item[4],'sub_region':item[5],'country':item[6],'flag':item[7]}
                        outs.append(out_obj)
                    except Exception as e1:
                         pass
        if country and not city or not out:
            p={"query":country}
            req = requests.get(url,params=p)
            raw = req.text
            lines=raw.split('\n')
            for line in lines:
                try:
                    if country.lower() in line.lower():
                        item = line.split('\t')
                    # uncomment to use with city name , to get the city´s zone_json data
                    #p={"mode":"tzmappos","p1":item[1]}
                    #req1 = requests.get("f'https://www.timeanddate.com/scripts/completion.php?mode=tzmappos&p1={item[1]}",params=p)
                    #{coords:{x:212,y:294},name:"Dallas",state:"Texas",country:"USA",cks:{"c70":{"t":[{"o":-18000,"a":"<a href=\"\/time\/zones\/cdt\" title=\"Central Daylight Time\">CDT<\/a>","d":1}]}}}
                        out_obj =  {'clock_data_url':f'https://www.timeanddate.com/scripts/completion.php/{item[0]}','zone_json':f'https://www.timeanddate.com/scripts/completion.php?mode=tzmappos&p1={item[1]}','iso_alpha_2_code':item[2],'country_state_code':item[3],'place':item[4],'sub_region':item[5],'country':item[6],'flag':item[7]}
                        outs.append(out_obj) 
                except Exception as e2:
                     pass

        output = sorted(set([str(i) for i in outs if i]))
        return [eval(i) for i in output ]
    except Exception as e:
        if verbose:
            print(str(e))
        return []
#example usage:
#flag = get_location_information_dict_by_city_country_via_timeanddate_api('Germany').get('flag','')
#get_location_information_dict_by_city_country_via_timeanddate_api('Germany')
#get_location_information_dict_by_city_country_via_timeanddate_api('Berlin')
#get_location_information_dict_by_city_country_via_timeanddate_api('Stuttgart')# hier exist two Stuttgart one in DE one in US,but we only get the first option
