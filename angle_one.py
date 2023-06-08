from smartapi import SmartConnect
import os
from pyotp import TOTP

key_path = r"/Users/vipin/workspace/ai/my_own"
os.chdir(key_path)

key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])

data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())

