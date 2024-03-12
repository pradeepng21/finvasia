from NorenRestApiPy.NorenApi import NorenApi
import config as cf
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz

class ShoonyaApiWrapper:
    def __init__(self):
        self.shoonya_obj = self.login()

    def login(self):
        class ShoonyaApiPy(NorenApi):
            def __init__(self):
                NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        api = ShoonyaApiPy()
        session_token = open("session_token.txt", "r").read()
        api.set_session("useridhere", "passwordhere", session_token)
        return api 

    def get_daily_price_series(self, exchange, trading_symbol, start_date, end_date):
        return self.shoonya_obj.get_daily_price_series(exchange=exchange, tradingsymbol=trading_symbol, startdate=start_date, enddate=end_date)

    def get_time_price_series(self, exchange, token, starttime, endtime, interval):
        return self.shoonya_obj.get_time_price_series(exchange, token, starttime, endtime, interval)

    def parse_json_data(self, data):
        return [json.loads(json_string) for json_string in data]

    def create_df_D(self, data):
        stock_df = pd.DataFrame(data)
        stock_df['time'] = pd.to_datetime(stock_df['time'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')
        stock_df.sort_values("time", ascending=True)
        stock_df = stock_df[::-1]
        return stock_df

    def create_df_T(self, data):
        stock_df = pd.DataFrame(data)
        # stock_df['time'] = pd.to_datetime(stock_df['time'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')
        stock_df.sort_values("time", ascending=True)
        stock_df = stock_df[::-1]
        return stock_df

    def scrip_data_nse(self):
        nse_df = pd.read_csv("https://api.shoonya.com/NSE_symbols.txt.zip")
        return nse_df

    def scrip_data_nfo(self):
        nfo_df = pd.read_csv("https://api.shoonya.com/NFO_symbols.txt.zip")
        return nfo_df

    def token_info_nse(self, nse_df, instrument_name, exchange, instrument_type):
        if instrument_type == "EQ":
            eq_df = nse_df[(nse_df["Exchange"]==exchange)
                            & (nse_df["Symbol"]==instrument_name)
                            & (nse_df["Exchange"]==exchange)]
            return eq_df.iloc[0]
        elif instrument_type == "INDEX":
            idx_df = nse_df[(nse_df["Exchange"]==exchange)
                            & (nse_df["Symbol"]==instrument_name)
                            & (nse_df["Exchange"]==exchange)]
            return idx_df.iloc[0]

    def token_info_nfo(self, nfo_df, instrument_name, exchange, instrument_type, strike=0, otype=""):
        if instrument_type == "OPTSTK":
            opt_stk_df = nfo_df[(nfo_df["Exchange"]==exchange)
                            & (nfo_df["Symbol"]==instrument_name)
                            & (nfo_df["Exchange"]==exchange)
                            & (nfo_df["StrikePrice"]==strike)
                            & (nfo_df["OptionType"]==otype)]
            return opt_stk_df.iloc[0]
        elif instrument_type == "OPTIDX":
            opt_idx_df = nfo_df[(nfo_df["Exchange"]==exchange)
                            & (nfo_df["Symbol"]==instrument_name)
                            & (nfo_df["Exchange"]==exchange)
                            & (nfo_df["StrikePrice"]==strike)
                            & (nfo_df["OptionType"]==otype)]
            return opt_idx_df.iloc[0]
        elif instrument_type == "FUTSTK":
            fut_stk_df = nfo_df[(nfo_df["Exchange"]==exchange)
                            & (nfo_df["Symbol"]==instrument_name)
                            & (nfo_df["Exchange"]==exchange)
                            # & (nfo_df["StrikePrice"]==strike)
                            # & (nfo_df["OptionType"]==otype)
                            ]
            return fut_stk_df.iloc[0]
        elif instrument_type == "FUTIDX":
            fut_idx_df = nfo_df[(nfo_df["Exchange"]==exchange)
                            & (nfo_df["Symbol"]==instrument_name)
                            & (nfo_df["Exchange"]==exchange)
                            # & (nfo_df["StrikePrice"]==strike)
                            # & (nfo_df["OptionType"]==otype)
                            ]
            return fut_idx_df.iloc[0]
    
    def get_previous_four_days():
        # Get the current date
        current_date = datetime.now()

        # Calculate the date of the previous day
        previous_day = current_date - timedelta(days=4)

        # Return the result in a formatted string (optional)
        return previous_day.strftime("%Y-%m-%d")



    def get_epoch_time(date_time: str) -> int:
        """
        Convert the given date_time string to epoch
        time in the Asia/Kolkata timezone.

        Args:
            date_time (str): The date and time string
            in the format "YYYY-MM-DD HH:MM:SS".

        Returns:
            int: The epoch time (seconds since 1970-01-01 00:00:00 UTC)
            for the given date_time.
        """
        # Convert date_time to datetime object
        date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        # date_time_obj = date_time_obj - timedelta(seconds=59)

        # Localize the datetime object to Asia/Kolkata timezone
        kolkata_tz = pytz.timezone("Asia/Calcutta")
        localized_date_time = kolkata_tz.localize(date_time_obj)

        # Return epoch time
        return int(localized_date_time.timestamp())
    
    def get_index_history(self):
        previous_day = self.get_previous_four_days()
        start_time = self.get_epoch_time(f"{previous_day} 09:15:00")
        end_time = self.get_epoch_time(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


    def main(self):
        pass



    


if __name__ == '__main__':
    shoonya_api = ShoonyaApiWrapper()
    
    exch = 'NSE'
    token = '26000'
    trading_symbol = "NIFTY INDEX"
    
    # ret = shoonya_api.get_daily_price_series(exchange=exch, trading_symbol=trading_symbol, start_date="1710128700", end_date="1710151200")
    # data = shoonya_api.parse_json_data(ret)
    # stock_df = shoonya_api.create_df(data)
    # print(stock_df)
    index_data = shoonya_api.get_time_price_series(exchange=exch, token=token, starttime="1710128700", endtime='1710151200', interval=1)
    # data = shoonya_api.parse_json_data(index_data)
    stock_df = shoonya_api.create_df_T(index_data)
    print(stock_df)
    nse_df = shoonya_api.scrip_data_nse()
    nfo_df = shoonya_api.scrip_data_nfo()


    # subscribe to a single token 
    # shoonya_api.shoonya_obj.subscribe('NSE|13')
    # shoonya_api.start_feed(shoonya_api.shoonya_obj, ['NSE|26000'])
    token = shoonya_api.token_info_nfo(nfo_df, "BANKNIFTY", "NFO", "OPTIDX", strike=48000, otype="PE")["Token"]
    print(token)
    # shoonya_api.subscribe("NSE|"+str(token))
    #subscribe to multiple tokens
    # shoonya_api.subscribe(['NSE|22', 'BSE|522032'])
    print(nse_df)
    print(nse_df.columns)

    
    
    