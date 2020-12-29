from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time
import pandas as pd

url = 'https://store.steampowered.com/games#p=0'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}


s = HTMLSession()

df = pd.DataFrame().reset_index(drop=True)

detail_list = []



def pagination(url,df):
    r = s.get(url, headers=headers)
    r.html.render(sleep=2)
    soup = BeautifulSoup(r.html.html, 'html.parser')

    #page pagination
    last_page = 10 #int(soup.find('div', class_='paged_items_paging').find('span', {'id':'NewReleases_total'}).text)
    print(f'pages to parse {last_page}')

    for i in range(0,last_page):
        url = f'https://store.steampowered.com/games#p={i}'
        results = parse(url)
        df = df.append(results)
        print('sleep for 20 seconds before parse next page ...')
        print(f'parsed {i +1} page from {last_page} pages' )
        time.sleep(10)
        print(df)
    df.to_csv('steam_test01.csv')
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
            final_price = game.find('div', {'class':'discount_final_price'}).text.strip()
        except:
            final_price = ''
        
        try:
            original_price = game.find('div', {'class':'discount_original_price'}).text.strip() 
        except:
            original_price = ''
        link = game['href']
        dict = {
            'title': title,
            'discount': discount,
            'final price': final_price,
            'original price': original_price,
            'link': link
            }
        detail_list.append(dict)
    
    print(len(detail_list))

    return detail_list

    
   

    


pagination(url,df)