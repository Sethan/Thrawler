import requests
import re
import os
from bs4 import BeautifulSoup
import pandas as pd

os.chdir('C:/Users/ZuraH/AppData/Local/Programs/Python/Python37-32')
r = requests.get('https://www.imdb.com/list/ls058011111/')
soup = BeautifulSoup(r.text,'html.parser')
results = soup.find_all('h3', attrs={'class':'lister-item-header'})
first_result = results[0]
records = []
i=0
for result in results:
    name=result.find('a').text
    name=name.strip()
    result=result.find('a')
    link=result['href']
    print(name)
    r=requests.get('https://www.imdb.com'+link)

    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        result = soup.find(id='filmo-head-actor').text
        t=re.findall(r'\d+',result)
    except:
        result = soup.find(id='filmo-head-actress').text
        t=re.findall(r'\d+',result)
    features=t[0]

    result = soup.find(id='name-born-info').text
    t=re.findall(r'\d+',result)
    age=t[1]
    death=0
    try:
        result = soup.find(id='name-death-info').text
        t=re.findall(r'\d+',result)
        death=t[1]
    except:
        print("Alive")

    result = soup.find(id='details-height').text
    t=re.findall(r'\(([^\)]+)\)',result)
    height=t[0][0:4]

    result = soup.find('span', attrs={"awards-blurb"}).text
    if 'Won' in result:
        t=re.findall(r'\d+',result)
        t=t[0]
    else:
        t=0
    oscars=t

    n=name.replace(" ","-")
    url='https://www.celebritynetworth.com/richest-celebrities/actors/X-net-worth/'
    url=url.replace("X",n)
    networth=0
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find('div',attrs={"meta_row networth"}).text
        t=re.findall(r'\d+',result)
        networth=t[0]
    except:
        print("is not added to networth list")



    i+=1
    records.append((i,name,age,features,oscars,height,networth,death))





    

df = pd.DataFrame(records, columns=['id','name','age','features','oscars','height','networth','death'])
df.to_csv('actorlist.csv', index=False, encoding='utf-8')


    


