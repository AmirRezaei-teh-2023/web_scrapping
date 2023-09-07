# -*- coding: utf-8 -*-
"""Scrapping(phase1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JoacR1rz49HCdjUr7VgzagjLD6F_xhaV

#### Imports
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import re
import urllib.parse
import numpy as np
from tqdm import tqdm
import math
from time import sleep
import random
import sqlite3
from sqlite3 import Error
import os
import random
import time
from IPython.display import display, Audio
import time
import re

header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

url = 'https://www.imdb.com/chart/top'

response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

response.status_code

from http.client import responses
responses[response.status_code]

"""#### Names"""

names = soup.find_all('a', attrs={'class' : 'ipc-title-link-wrapper'})
print('{} links found'.format(len(names)))

names_text = [name.text for name in names]
names_text

new_names_text = names_text[:250]
new_names_text

import re
final_names = []
counter = []
c =0
for i in new_names_text:
  res = re.sub(r'^.*?\s', '',i)
  counter.append(c)
  final_names.append(res)
  c = c+1
print(final_names)

names_df = pd.DataFrame(final_names , columns=['title'])
names_df['film_row_num'] = counter
names_df

"""

#### Film_id

"""

names_url = [name.get('href') for name in names]
names_url

new_names_url = names_url[:250]
new_names_url

import re
final_id = []
for i in new_names_url:
  res = re.split(r'/', i)
  res1 = res[2]
  final_id.append(res1)
print(final_id)

new_final_id = []
for i in final_id:
  new_res = re.sub(r'[^0-9]', '', i)
  new_final_id.append(new_res)
print(new_final_id)

names_id_df = pd.DataFrame(new_final_id , columns=['id'])
names_id_df['film_row_num'] = counter
names_id_df

"""#### URLs"""

urls = []
for i in final_id:
  i = 'https://www.imdb.com/title/' + i
  urls.append(i)
print(urls)

url_fake = urls[:6]
print(url_fake)

"""####year


"""

my_lis = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  gross = soup.find_all('ul' , attrs={'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"})
  for i in gross:
    #k = i.find_all('li' , attrs={'class' : "ipc-inline-list__item"})
    try:
      k = i.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.eaRXHu > section > div:nth-child(4) > section > section > div.sc-e226b0e3-3.jJsEuz > div.sc-dffc6c81-0.iwmAVw > ul > li:nth-child(1) > a')
      k2 = [e.text for e in k]
      my_lis.append(k2)
    except:
      my_lis.append('nan')
print(my_lis)

new_my_lis = []
for i in my_lis:
  for j in i:
    year = int(j)
    new_my_lis.append(year)

print(new_my_lis)

year_df = pd.DataFrame(new_my_lis , columns=['year'])
year_df

"""#### runtime"""

my_lis = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  gross = soup.find_all('ul' , attrs={'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"})
  for i in gross:
    #k = i.find_all('li' , attrs={'class' : "ipc-inline-list__item"})
    try:
      k = i.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.eaRXHu > section > div:nth-child(4) > section > section > div.sc-e226b0e3-3.jJsEuz > div.sc-dffc6c81-0.iwmAVw > ul > li:nth-child(3)')
      k2 = [e.text for e in k]
      my_lis.append(k2)
    except:
      my_lis.append('UnTimed')
print(my_lis)

time = []
for i in my_lis:
  if len(i) == 0:
    time.append('Untimed')
  else:
    time.append(i[0])


print(time)

print(len(time))

runtime_df = pd.DataFrame(time, columns=['runtime'])
runtime_df

def get_numbers_before_h(text):
    pattern = r'(\d+)h'
    matches = re.findall(pattern, text)
    if matches:
        return int(matches[-1])
    else:
        return 0
def get_numbers_before_m(text):
    pattern = r'\b(\d+)m\b'
    matches = re.findall(pattern, text)
    if matches:
        return int(matches[-1])
    else:
        return 0

runtime_df['hour'] = runtime_df['runtime'].apply(lambda x : int(get_numbers_before_h(x)))
runtime_df['minute'] = runtime_df['runtime'].apply(lambda x : int(get_numbers_before_m(x)))

runtime_df['runtime'] = runtime_df['hour']*60 + runtime_df['minute']
runtime_df = runtime_df.drop(['hour', 'minute'], axis=1)
runtime_df

"""#### Rate"""

my_lis = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  gross = soup.find_all('ul' , attrs={'class' : "ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt"})
  for i in gross:
    #k = i.find_all('li' , attrs={'class' : "ipc-inline-list__item"})
    try:
      k = i.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.eaRXHu > section > div:nth-child(4) > section > section > div.sc-e226b0e3-3.jJsEuz > div.sc-dffc6c81-0.iwmAVw > ul > li:nth-child(2) > a')
      k2 = [e.text for e in k]
      my_lis.append(k2)
    except:
      my_lis.append('Unrated')
print(my_lis)

print(my_lis)

new = []
for i in my_lis:

    if len(i) == 0:
        new.append('Unrated')
    else:
        new.append(i[0])

q=0
for i in new:
  if i == 'Unrated':
    q=q+1
  else:
    pass
print(q)

new_new = []
for i in new:
  if i == 'Not Rated':
    new_new.append('Unrated')
  else :
    new_new.append(i)

q=0
for i in new_new:
  if i == 'Unrated':
    q=q+1
  else:
    pass
print(q)

rate_df = pd.DataFrame(new_new,columns=['parental_guide'])
rate_df

"""#### Gross


"""

def find_matching_elements(lst, pattern):
    matching_indices = []
    for i, element in enumerate(lst):
        if re.search(pattern, element):
            matching_indices.append(i)
    return matching_indices

my_lis = []
for i in urls:
  lis_1 = []
  lis_2 = []
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  gross = soup.find_all('li' , attrs={'class' : "ipc-metadata-list__item sc-6d4f3f8c-2 byhjlB"})
  for i in gross:
    k = i.find_all('span' , attrs={'class' : "ipc-metadata-list-item__label"})
    k2 = [e.text for e in k]
    v = i.find_all('span' , attrs={'class' : "ipc-metadata-list-item__list-content-item"})
    v2 = [e.text for e in v]
    k3 = str(k2[0])
    v3 = str(v2[0])
    lis_1.append(v3)
    lis_2.append(k3)
  o = find_matching_elements(lis_2, 'Gross US & Canada')
  try:
    my_lis.append(lis_1[(o[0])])
  except:
    my_lis.append('nan')
print(my_lis)

new_my_lis = []
for i in my_lis:
  if i == 'nan':
    new_my_lis.append(float('Nan'))
  else:
    new_res = re.sub(r'[^0-9]', '', i)
    new_my_lis.append(float(new_res))

print(new_my_lis)

price_df = pd.DataFrame(new_my_lis , columns= ['gross_us_canada'])
price_df

"""####Directors"""

directors_name = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('li', attrs={'class' : "ipc-metadata-list__item"})
  wri = crews[0].find_all('a' , attrs={'class' : "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
  Writer = [i.text for i in wri]
  for i in Writer:
    print(c)
    print(i)
    directors_name.append(i)
    counter.append(c)
  c = c+1

directors_df = pd.DataFrame(
    {'name': directors_name,
     'film_row_num':counter
    })
directors_df

directors_id = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('li', attrs={'class' : "ipc-metadata-list__item"})
  wri = crews[0].find_all('a' , attrs={'class' : "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
  Writer = [i.get('href') for i in wri]
  for i in Writer:
    print(c)
    print(i)
    directors_id.append(i)
    counter.append(c)
  c = c+1

new_Directors_id = []
for i in directors_id:
  #print(i)
  res = re.split(r'/', i)
  #print(res)
  res1 = res[2]
  new_res = re.sub(r'[^0-9]', '', res1)

  new_Directors_id.append(new_res)
print(new_Directors_id)
print(len(new_Directors_id))

directors_df['person_id'] = new_Directors_id
directors_df

directors_df_with_role = directors_df.copy()
directors_df_with_role['role'] = 'Director'
directors_df_with_role

"""####Writers"""

writers_name = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('li', attrs={'class' : "ipc-metadata-list__item"})
  wri = crews[1].find_all('a' , attrs={'class' : "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
  Writer = [i.text for i in wri]
  for i in Writer:
    print(c)
    print(i)
    writers_name.append(i)
    counter.append(c)
  c = c+1

writers_df = pd.DataFrame(
    {'name':writers_name,
     'film_row_num':counter
    })
writers_df

writers_id = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('li', attrs={'class' : "ipc-metadata-list__item"})
  wri = crews[1].find_all('a' , attrs={'class' : "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
  Writer = [i.get('href') for i in wri]
  for i in Writer:
    print(c)
    print(i)
    writers_id.append(i)
    counter.append(c)
  c = c+1

new_writers_id = []
for i in writers_id:
  #print(i)
  res = re.split(r'/', i)
  #print(res)
  res1 = res[2]
  new_res = re.sub(r'[^0-9]', '', res1)

  new_writers_id.append(new_res)
print(new_writers_id)
print(len(new_writers_id))

writers_df['person_id'] = new_writers_id
writers_df

writers_df_with_role = writers_df.copy()
writers_df_with_role['role'] = 'Writer'
writers_df_with_role

"""####Stars"""

stars_name = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('li', attrs={'class' : "ipc-metadata-list__item"})
  wri = crews[2].find_all('a' , attrs={'class' : "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
  Writer = [i.text for i in wri]
  for i in Writer:
    print(c)
    print(i)
    stars_name.append(i)
    counter.append(c)
  c = c+1

stars_df = pd.DataFrame(
    {'name':stars_name,
     'film_row_num':counter
    })
stars_df

stars_id = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('li', attrs={'class' : "ipc-metadata-list__item"})
  wri = crews[2].find_all('a' , attrs={'class' : "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})
  Writer = [i.get('href') for i in wri]
  for i in Writer:
    print(c)
    print(i)
    stars_id.append(i)
    counter.append(c)
  c = c+1

new_stars_id = []
for i in stars_id:
  #print(i)
  res = re.split(r'/', i)
  #print(res)
  res1 = res[2]
  new_res = re.sub(r'[^0-9]', '', res1)

  new_stars_id.append(new_res)
print(new_writers_id)
print(len(new_writers_id))

stars_df['person_id'] = new_stars_id
stars_df

stars_df_with_role = stars_df.copy()
stars_df_with_role['role'] = 'Crews'
stars_df_with_role

"""#### genre"""

genre_name = []
c = 0
counter = []
for i in urls:
  response = requests.get(i, headers=header)
  soup = BeautifulSoup(response.text, "html.parser")
  crews = soup.find_all('a', attrs={'class' : "ipc-chip ipc-chip--on-baseAlt"})
  Writer = [i.text for i in crews]
  for i in Writer:
    print(c)
    print(i)
    genre_name.append(i)
    counter.append(c)
  c = c+1

genre_df = pd.DataFrame(
    {'name':genre_name,
     'film_row_num':counter
    })
genre_df

"""#### **movie Table**


"""

movie = pd.concat([names_id_df,names_df, year_df, runtime_df,rate_df, price_df],axis=1)
movie

movie.info()

movie.to_csv('movie.csv', index=False)

"""
#### **person Table**"""

person_df = pd.concat([directors_df,writers_df, stars_df],axis=0)
person_df

person_df.drop(['film_row_num'], axis=1 , inplace=True)

person_df.drop_duplicates(keep='first', inplace=True)
person_df

person_df.reset_index(drop=True, inplace=True)
person_df

person_df.info()

person_df.to_csv('person.csv', index=False)

"""#### **cast Table**"""

cast_df = pd.merge(stars_df, names_id_df,  how='left', left_on='film_row_num', right_on = 'film_row_num')
cast_df

cast_df.drop(['film_row_num','name'], axis=1 , inplace=True)
cast_df

cast_df.rename(columns={'id':'movie_id'} , inplace=True)
cast_df

cast_df.to_csv('cast.csv', index=False)

"""####**crews Table**"""

crew_df = pd.concat([writers_df_with_role,directors_df_with_role],axis=0)
crew_df

crew_df.reset_index(drop=True, inplace=True)
crew_df

new_crew_df = pd.merge(crew_df, names_id_df,  how='left', left_on='film_row_num', right_on = 'film_row_num')
new_crew_df

new_crew_df.drop(['film_row_num','name'], axis=1 , inplace=True)
new_crew_df

new_crew_df.rename(columns={'id':'movie_id'} ,inplace=True)
new_crew_df

new_crew_df.to_csv('crew.csv', index=False)

"""####**genre Table**"""

new_genre_df = pd.merge(genre_df, names_id_df,  how='left', left_on='film_row_num', right_on = 'film_row_num')
new_genre_df

new_genre_df.drop(['film_row_num'], axis=1 , inplace=True)
new_genre_df

new_genre_df.rename(columns={'id':'movie_id'} , inplace=True)
new_genre_df

new_genre_df.to_csv('genre.csv', index=False)