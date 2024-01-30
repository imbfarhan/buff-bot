from datetime import datetime
# import settings

def STARTLOG():
    print("NOTE:START VPN BEFORE STARTING THE BOT")
    # print(f"Starting EZALTS.SHOP STEAM BOT with following parameters:\nItem Link: {settings.URL}\nMax Float: {settings.max_float}\nMax Price: {settings.max_price}")

def INITFINDERLOG():
    LOG("Initializing FINDER BOT")

def INITBUYERLOG():
    LOG("Initializing BUYER BOT")

def LOG(message):
    current_datetime = datetime.now()
    current_time = current_datetime.strftime('%H:%M:%S')
    print(f'[{current_time}] {message}')