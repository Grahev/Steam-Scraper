from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import pandas as pd
import concurrent.futures
from random import randint


url = 'https://store.steampowered.com/games#p=0'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


s = HTMLSession()

df = pd.DataFrame().reset_index(drop=True)

detail_list = []
links = []
last_page = None


def last_pg(url):
    r = s.get(url, headers=headers)
    r.html.render(sleep=2)
    soup = BeautifulSoup(r.html.html, 'html.parser')

    #page pagination
    last_page = 15 #int(soup.find('div', class_='paged_items_paging').find('span', {'id':'NewReleases_total'}).text)
    print(f'pages to parse {last_page}')
    return last_page


def pagination(last_page):
    for i in range(0,last_page):
        url = f'https://store.steampowered.com/games#p={i}'
        links.append(url)

    print(len(links))
    print('links created')
    #print(links)
    return links


        
def save_data(list,df):
    df = df.append(list)
    df = df.sort_values(by='savings', ascending = False)
    df.to_csv('steam_test.csv')
    return

        

def parse(url):
    #make request
    r = s.get(url, headers=headers)
    r.html.render(sleep=2)
    soup = BeautifulSoup(r.html.html, 'html.parser')


    #get games container
    container = soup.find('div', {'id':'TopSellersRows'})
    #get single game
    games = container.find_all('a', {'class':'tab_item'})

    #parse games data
    for game in games:
        title = game.find('div',{'class':'tab_item_name'}).text
        try:
            discount = game.find('div', {'class':'discount_pct'}).text
        except:
            discount = ''

        try:
            final_price = float(game.find('div', {'class':'discount_final_price'}).text.strip().replace('£',''))
        except:
            final_price = ''
        
        try:
            original_price = float(game.find('div', {'class':'discount_original_price'}).text.strip().replace('£','')) 
        except:
            original_price = ''
        try:
            savings = round(original_price - final_price,2)
        except:
            savings = 0
        link = game['href']
        dict = {
            'title': title,
            'savings': savings,
            'discount': discount,
            'final price': final_price,
            'original price': original_price,
            'link': link
            }
        detail_list.append(dict)
    
    print(len(detail_list))
    print('parse in progress...')

    return detail_list

    
def main():
    last_page = last_pg(url)
    links = pagination(last_page)
    """ with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(parse, links) """

    for link in links:
        ransleep = randint(0,3)
        parse(link)
        last_page = last_page -1
        print(f'pages to parse: {last_page}')
        print(f'sleep for {ransleep} secods')
        time.sleep(ransleep)
    
    save_data(detail_list,df)
    print('df saved')

    


main()