import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import time
import csv

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table =  soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    with open('sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)

    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def update_csv():
    if not os.path.exists('stock_dfs'):
        save_sp500_tickers()
        get_data_from_yahoo()
    else:
        os.chdir(os.getcwd() + '\\stock_dfs\\')
        for dirc in os.walk(os.getcwd(), topdown=True):
            for comps in dirc[2]:
                last_date_update = open(comps).readlines()[-1][:10]
                s_year, s_month, s_day = last_date_update.split('-')

                e_year, e_month, e_day = str(dt.datetime.now().date()).split('-')

                if(s_year == e_year and s_month == e_day and s_day == e_day):
                    continue
                else:
                    end = dt.datetime(int(e_year), int(e_month), int(e_day))
                    start = dt.datetime(int(s_year), int(s_month), int(s_day))

                    tckr = comps.split('.')[0]
                    df = web.DataReader(tckr, 'yahoo', start, end)
                    to_csv = str(df.to_csv(header=None)).split('\n')[1:-1]

                    with open(comps, 'a') as f:
                        writer = csv.writer(f, delimiter='\n')
                        writer.writerow(to_csv)
                        print(comps,'updated')
                        time.sleep(1)

get_data_from_yahoo()
save_sp500_tickers()
update_csv()

