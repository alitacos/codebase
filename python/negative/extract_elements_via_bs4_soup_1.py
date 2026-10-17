# code makes no sence as a snippet. unknown what the use can and source be. Assuming it is related to some code part  using  BeautifulSoup from bs4 
lists =  contents.find_all('li',class_='b_algo')
print('-----')
print()

for a in lists:
    i = a.find_all('div',class_='tptt')
    print([(e.get('class'), e.text,e.get('href')) for e in i])
    i = a.find_all('div',class_='b_attribution')
    print([(e.get('class'), e.text,e.get('href')) for e in i])
    i = a.find_all('a',class_='tptxt')
    for e in i:
        print([(a.get('class'), a.text,a.get('href')) for a in e])
    #title
    i = a.find('h2' )
    title = [(e.get('class'), e.text,[a.get('href') for a in e.find_all('a')]) for e in i]
    print(title)

    i = a.find_all('div',class_='b_caption')
    caption = [(e.get('class'), e.text,e.get('href')) for e in i]
    print(caption)
    i = a.find_all('div',class_='cCodeBg')
    b_vPanel = [(e.get('class'), e.text,e.get('href')) for e in i]
    #b_lineclamp2 = [i.get('class'), i.text,[ a.get('href') for a in i] ]
    print(b_vPanel)
    print()
    print('---------')
    print()
lists =  contents.find_all('li',class_='b_algo')
