from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import config as cf
import base64

def login():
    class ShoonyaApiPy(NorenApi):
        def __init__(self):
            NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
    api = ShoonyaApiPy()
    encoded_secret = "4EM55GGH2X4UC427J456XZCLF23CGHNK"
    res = api.login(userid="user_id", password="passwordhere", twoFA=pyotp.TOTP(encoded_secret).now(),
                    vendor_code="___", api_secret="___", imei="abc1234")
    with open('session_token.txt', 'w') as file:
        file.write(res['susertoken'])
    return api 
    
if __name__ == '__main__':
    shoonya_obj = login()