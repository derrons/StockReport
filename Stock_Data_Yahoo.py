import yfinance as yf
import pandas as pd

# Method will download stocks and return stock data and download status 
# of true if any data is returned and false if no data is gathered
def load_yahoo_stocks(stocks):
    history_list = []
    downloaded = True
    for data in stocks:
        print (f"Downloading {data['Symbol']} data")
        try:
            history = yf.download(data['Symbol'], 
                                start = data['Date'],
                                end = data['End_Date'],
                                group_by="ticker")
            #create column for stock symbol
            history['Symbol'] = data['Symbol']
            history_list.append(history)
        except Exception as e:
            print(f'Error downloading {data["Symbol"]}:  {str(e)}')

        if len(history_list) == 0:
            downloaded = False
    # merge all data pulls together into one dataframe
    results = pd.concat(history_list)
    return results, downloaded

