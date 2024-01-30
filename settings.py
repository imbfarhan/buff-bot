import os

abs_path=os.path.dirname(__file__)

VERSION_NO="v1.0 beta"

URL='https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Elite%20Build%20%28Well-Worn%29'


driver_rel_path='assets/driver/chromedriver-win64/chromedriver.exe'
driver_path=os.path.normpath(os.path.join(abs_path, driver_rel_path))


csfloat_rel_path='assets/plugins/CSFloat-Market-Checker.crx'
csfloat_path=os.path.normpath(os.path.join(abs_path, csfloat_rel_path))

cookies_rel_path='cookies.json'
cookies_path=os.path.normpath(os.path.join(abs_path, cookies_rel_path))


# #SET MAX FLOAT AND MAX PRICE HERE
max_float=1
min_float=0
max_price=0 #PRICE IS IN USD