import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
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
    """
    Updates all csv's to the current date.
    """
    
    #Check to see if the other methods have been run.
    if not os.path.exists('stock_dfs'):
        save_sp500_tickers()
        get_data_from_yahoo()
    else:
        os.chdir(os.getcwd() + '\\stock_dfs\\')
        
        #Make a list of every file in the directory, topdown=True is optional, it just updates the files in alphabetical order.
        for dirc in os.walk(os.getcwd(), topdown=True):
            for comps in dirc[2]:

                """
                Open up the csv and read the last line.
                [-1] accesses the last row of the csv file.
                [:10] gets the first 10 characters at index 0-9 of the last line.
                Should be equivalent to the date YYYY-MM-DD = 10 characters.
                """
                last_update = open(comps).readlines()[-1][:10]

                #Split the string to be put into the datetime class.
                s_year, s_month, s_day = last_update.split('-')

                #Get today's date.
                e_year, e_month, e_day = str(dt.datetime.now().date()).split('-')

                #Check to see if the csv even needs to be updated. If it is move to next file.
                if(s_year == e_year and s_month == e_day and s_day == e_day):
                    continue
                else:

                    #Create an end and start to put into the pandas dataframe.
                    end = dt.datetime(int(e_year), int(e_month), int(e_day))
                    start = dt.datetime(int(s_year), int(s_month), int(s_day))

                    #Get the ticker from the name of the file.
                    tckr = comps.split('.')[0]

                    #Get the daily stock information between last update and today.
                    df = web.DataReader(tckr, 'yahoo', start, end)

                    """
                    Convert the pandas dataframe into a string to be written by csv.
                    [1:] gets rid of first date because that date is already in csv from previous access.
                    The [:-1] gets rid of the last string because it is always empty.
                    header=None removes the column information so we can just take the information we want.
                    """
                    to_csv = str(df.to_csv(header=None)).split('\n')[1:-1]

                    #Write the new string to csv.
                    with open(comps, 'a') as f:
                        writer = csv.writer(f, delimiter='\n')
                        writer.writerow(to_csv)

                        #Confirm that we successfully updated the csv file.
                        print(comps,'updated')

get_data_from_yahoo()
save_sp500_tickers()
update_csv()

