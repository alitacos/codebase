def collect_all_phrack_articles_in_dictionary_via_webdriver_and_store_in_file(driver:object=None,output_path:str='')->dict:
    from bs4 import BeautifulSoup
    from selenium import webdriver
    def process_page(driver:object=None, page_int:int=0, index:int=0)->dict:
        if not page_int or not index:
            return {}
        try:
            driver.get(f"https://phrack.org/issues/{i}/{ii}")

            title = driver.title
            sourcetext = driver.page_source
            soup = BeautifulSoup(sourcetext, 'html.parser').find('body')
            try:
                title1 = soup.find('div',{'id':'article'}).get_text().strip()[5:]
            except Exception as e:
                title1 = 1
            author = soup.find('div',{'class':'opt-bottom'}).get_text().strip()[6:]
            raw = soup.find('div',{'class':'opt-bottom'}).find_next_sibling()
            if title.strip() and title1.strip() and author.strip() and raw.get_text().strip():
                return {'page_title':title.strip().replace('::.','').replace('.::',''),'articleTitle':title1.strip(), 'author':author.strip(), 'raw':raw.get_text().strip() }
            return {}
        except Exception as e:
            #print(e)
            return {}
    def store_json(path:str='',data:dict|list=None)->bool
        import json
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    collection = {}
    for i in range(73):
        for ii in range(21):
            pageinfo = process_page(driver=driver, page_int=i, index=ii)
            if pageinfo:
                if i not in collection.keys():
                    collection[i] = {}
                collection[i][ii] = pageinfo
    if collection and output_path:
        import os
        directory = os.path.dirname(output_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        store_json(path=output_path,data=collection)
        print(f'data successfully stored in {output_path}')
    return collection