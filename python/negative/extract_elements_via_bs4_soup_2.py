# code makes no sence as a snippet. unknown what the use can and source be. Assuming it is related to some code part  using  BeautifulSoup from bs4 
lists =  contents.find_all('li',class_='b_algo')
print('-----')
for a in lists:
    for i in a.find_all('a'):
        if i.get('class') != 'tilk':
            print((i.get('class'), i.text) )
            
        