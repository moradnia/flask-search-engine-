#!/usr/bin/env python
# coding: utf-8

# In[26]:


import time
from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup
from requests import get
es= Elasticsearch(HOST="http://localhost",PORT=9200)
es= Elasticsearch()
es.indices.create(index='imdb', ignore=400)
url = 'http://www.imdb.com/search/title?release_date=2019&sort=num_votes,desc&page=1'

response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-advanced')

for container in movie_containers:
    movie_link=container.select('div > a',class_='lister-item-image float-left')
    for t in movie_link:
        href='https://www.imdb.com'+t['href']
    movie_image=container.select('a >img',class_='loadlate')
    for m in movie_image:
        src_image=m['loadlate']
        

    if container.find('div', class_ = 'ratings-bar') :

        name = container.h3.a.text

        year = container.h3.find('span', class_ = 'lister-item-year').text
        year=year.replace('(','')
        year=year.replace(')','')
   
        imdb_rate = float(container.strong.text)
    
        grade_score = container.find('span', class_ = 'lister-item-index unbold text-primary').text
  
        vote = container.find('span', attrs = {'name':'nv'})['data-value']
        
        budge=container.find('p',class_='sort-num_votes-visible').find_next('span',text='Gross:').find_next('span').text
        plot = container.find('p',class_="text-muted").find_next('p',class_='text-muted').text
        plot = plot.replace('\n','').lstrip()
        director = container.find('p',class_='').find_next('a').text
        stars =container.find('p',class_='').find_all('a')[1:]
        
        doc={
            'name':name,
            'years':year,
            'rate':imdb_rate,
            'vote':int(vote),
            'href':href,
            'src_image':src_image,
            'budge':budge,
            'plot':plot,
            'director':director,
            'stars':[x.text for x in stars]
        }

        res = es.index(index="imdb", doc_type="docs", body=doc)
        time.sleep(0.5)
            

