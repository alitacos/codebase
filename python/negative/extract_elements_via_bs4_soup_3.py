# code makes no sence as a snippet. unknown what the use can and source be. Assuming it is related to some code part  using  BeautifulSoup from bs4 
contents = soup.find("ol",{'id':'b_results'})#,{"class":"g"})
#lists =  contents.find_all('div',class_='b_caption')
#lists =  contents.find_all('h2')
lists =  contents.find_all('li',class_='b_ans b_mop')
lists