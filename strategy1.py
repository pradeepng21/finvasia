from NorenRestApiPy.NorenApi import NorenApi
import config as cf
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
import pandas_ta as ta
from utils.helpers import read_config_v1

class ShoonyaApiWrapper:
    def __init__(self):
        self.read_config = read_config_v1("config.ini")["credentials"]
        self.shoonya_obj = self.login()

    def login(self):
        class ShoonyaApiPy(NorenApi):
            def __init__(self):
                NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        api = ShoonyaApiPy()
        session_token = open("session_token.txt", "r").read()
        api.set_session(self.read_config["id"],self.read_config["password"], session_token)
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
        stock_df.sort_values("time")
        stock_df = stock_df[::-1]
        columns_to_drop = ['stat', 'intvwap', 'intv', 'intoi', 'v', 'oi']
        stock_df = stock_df.drop(columns_to_drop, axis=1)
        stock_df["intc"] = stock_df["intc"].astype(float)
        # macd = ta.macd(stock_df["intc"])
        # stock_df["macd"] = macd.iloc[:, 0]
        # stock_df["histogram"] = macd.iloc[:, 1]
        # stock_df['rsi'] = ta.rsi(stock_df["intc"], length=14)
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
    
    def get_previous_four_days(self):
        # Get the current date
        current_date = datetime.now()

        # Calculate the date of the previous day
        previous_day = current_date - timedelta(days=4)

        # Return the result in a formatted string (optional)
        return previous_day.strftime("%Y-%m-%d")

    def get_epoch_time(self, date_time: str) -> int:
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
        date_time_obj = date_time_obj.replace(second=0)
        # date_time_obj = date_time_obj - timedelta(seconds=59)

        # Localize the datetime object to Asia/Kolkata timezone
        kolkata_tz = pytz.timezone("Asia/Calcutta")
        localized_date_time = kolkata_tz.localize(date_time_obj)

        # Return epoch time
        return int(localized_date_time.timestamp())

    def get_index_history(self, exch, token, interval):
        previous_day = self.get_previous_four_days()
        start_time = self.get_epoch_time(f"{previous_day} 09:15:00")
        end_time = self.get_epoch_time(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        index_data = self.get_time_price_series(exchange=exch, token=token, starttime=start_time, endtime=end_time, interval=interval)
        stock_df = self.create_df_T(index_data)
        return stock_df
    
    def get_index_live(self, exch, token, interval):
        current_time = datetime.now()
        next_min = current_time + timedelta(minutes=1)
        start_time = self.get_epoch_time(str(current_time.strftime("%Y-%m-%d %H:%M:%S")))
        end_time = self.get_epoch_time(str(next_min.strftime("%Y-%m-%d %H:%M:%S")))
        index_data = self.get_time_price_series(exchange=exch, token=token, starttime=start_time, endtime=end_time, interval=interval)
        stock_df = self.create_df_T(index_data)
        return stock_df


    def main(self):
        nifty_hist_df = self.get_index_history("NSE", "26000", 1)
        banknifty_hist_df = self.get_index_history("NSE", "26009", 1)
        finnifty_hist_df = self.get_index_history("NSE", "26037", 1)
        midcap_hist_nf = self.get_index_history("NSE", "26074", 1)
        # indiavix_df = self.get_index_history("NSE", "26017", 15)
        print(nifty_hist_df)
        while True:
            current_time = datetime.now()
            if current_time.second == 0:
                nifty_df = self.get_index_live("NSE", "26000", 1)
                nifty_df = pd.concat([nifty_hist_df, nifty_df])


if __name__ == '__main__':
    shoonya_api = ShoonyaApiWrapper()
    
    exch = 'NSE'
    token = '26000'
    trading_symbol = "NIFTY INDEX"
    
    # ret = shoonya_api.get_daily_price_series(exchange=exch, trading_symbol=trading_symbol, start_date="1710128700", end_date="1710151200")
    # data = shoonya_api.parse_json_data(ret)
    # stock_df = shoonya_api.create_df(data)
    # print(stock_df)
    # index_data = shoonya_api.get_time_price_series(exchange=exch, token=token, starttime=1709955900, endtime=1710302520, interval=1)
    # print(index_data)
    # data = shoonya_api.parse_json_data(index_data)
    
    # print(stock_df)
    nse_df = shoonya_api.scrip_data_nse()
    nfo_df = shoonya_api.scrip_data_nfo()

    # print(nse_df)
    # print(nse_df.columns)
    print(datetime.now())
    shoonya_api.main()
    print(datetime.now())
    # nifty_quote = shoonya_api.shoonya_obj.get_quotes("NSE", "26000")
    # print(nifty_quote)
