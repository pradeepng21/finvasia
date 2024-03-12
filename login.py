
import logging
from NorenRestApiPy.NorenApi import NorenApi
import pyotp
import config as cf
import base64
from api_helper import ShoonyaApiPy
import logging
from datetime import time

#enable dbug to see request and responses
logging.basicConfig(level=logging.DEBUG)
#start of our program

def login():
    api = ShoonyaApiPy()
    #credentials

    user = 'FA142065'
    u_pwd = 'Pr@d33png21'
    raw_secret = b"960073"  # Replace this with your actual secret
    encoded_secret = base64.b32encode(raw_secret).decode('utf-8')
    factor2 = pyotp.TOTP(encoded_secret).now()
    vc = 'FA142065_U'
    app_key = 's1c9c1ab1fadc5e6320865239da5a20be'
    imei = 'abc1234'
    ret = api.login(userid=user, password=u_pwd, twoFA=factor2, vendor_code=vc,
    api_secret=app_key, imei=imei)
    return ret
exch = 'NSE'
token = '22'
shoonya_obj = login()
while True:
        ret = shoonya_obj.get_quotes(exchange=exch, token=token)
        print(ret)
        time.sleep(2)
# print(ret)