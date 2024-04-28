from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import base64
from utils.helpers import read_config_v1

def login(read_config):
    class ShoonyaApiPy(NorenApi):
        def __init__(self):
            NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
    api = ShoonyaApiPy()
    
    res = api.login(userid=read_config["id"], password=read_config['password'], twoFA=pyotp.TOTP(read_config["encoded_secret"]).now(),
                    vendor_code=read_config['vendor_code'], api_secret=read_config["api_secret"], imei=read_config["imei"])
    with open('session_token.txt', 'w') as file:
        file.write(res['susertoken'])
    return api 

if __name__ == '__main__':

    read_config = read_config_v1("config.ini")['credentials']
    shoonya_obj = login(read_config)