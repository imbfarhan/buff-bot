from bs4 import BeautifulSoup
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Logger
import VPN_COMMANDS
import json
import settings

settings_json_rel_path='settings.json'
settings_json_path=os.path.normpath(os.path.join(settings.abs_path, settings_json_rel_path))

with open(settings_json_path, 'r') as file:
    data = json.load(file)
    ITEM_LINK = data['LINK']
    ITEM_MIN_FLOAT = data['MIN_FLOAT']
    ITEM_MAX_FLOAT=data['MAX_FLOAT']
    ITEM_MAX_PRICE = data['MAX_PRICE']



url_to_buy=f"{ITEM_LINK}#tab=selling&page_num=1&sort_by=paintwear.asc&max_price={ITEM_MAX_PRICE}&min_paintwear={ITEM_MIN_FLOAT}&max_paintwear={ITEM_MAX_FLOAT}"

url="https://buff.163.com/goods/33960"
# print(url_to_buy)
driver=None

def get_cleaned_price(price_string):
    cleaned_price = re.sub(r'[^0-9.,]', '', price_string)
    try:
        price_float = float(cleaned_price)
        return price_float
    except ValueError:
        return float('inf')
    
def saveCookies(driver):
    # Get and store cookies after login
    cookies = driver.get_cookies()

    # Store cookies in a file
    with open(settings.cookies_path, 'w') as file:
        json.dump(cookies, file)
    Logger.LOG('New Cookies saved successfully.')


def loadCookies(driver):
    # Check if cookies file exists
    if(os.path.exists(settings.cookies_path)):

        # Load cookies to a variable from a file
        with open(settings.cookies_path, 'r') as file:
            cookies = json.load(file)

        # Set stored cookies to maintain the session
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        Logger.LOG('No cookies file found')
    
    driver.refresh() # Refresh Browser after login


def initiate_buff_bot():
    Logger.STARTLOG()
    Logger.INITFINDERLOG()
    global driver
    #--DRIVER DEPENDENCIES
    driver_executable_path = settings.driver_path
    os.environ["webdriver.chrome.driver"] = driver_executable_path
    chrome_options = Options()
    chrome_options.add_argument(f'--chromedriver={driver_executable_path}')
    chrome_options.add_experimental_option("detach", True)

    #TODO:CHECK THIS
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--acceptInsecureCerts=true')
    
    # chrome_options.add_argument('headless')

    #TODO: UNCOMMENT THIS LINE TO PREVENT DEBUGGING
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # Create a webdriver instance


# driver = webdriver.Chrome(desired_capabilities=capabilities)
    driver = webdriver.Chrome(options=chrome_options)
    # driver.get(url)


    loginURL = 'https://steamcommunity.com/login/home/'
    driver.get(loginURL)

    # Load old session into the browser
    loadCookies(driver)

    if 'login' in driver.current_url:
        # Ask for login Manually
        Logger.LOG('Please login into Steam in the BUYER BOT')
        Logger.LOG('Press ENTER in terminal after you login')
        input('>: ')
        # After successful login save new session cookies to json file
        saveCookies(driver)
        driver.get(url)

    else:
        Logger.LOG('Previous session loaded')
        driver.get(url)
    

def start_buff_bot():
    global driver
    Logger.LOG("Initialized FINDER BOT")

    driver.refresh()
    try:
        Logger.LOG("Logging into BUFF 163")
        nav_entries = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav.nav_entries")))
        login_register_li = WebDriverWait(nav_entries, 10).until(EC.element_to_be_clickable((By.XPATH, ".//ul/li/a")))
        login_register_li.click()
        login_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'j_popup_login')))
        login_other_link = WebDriverWait(login_popup, 10).until(EC.element_to_be_clickable((By.ID, 'j_login_other')))
        login_other_link.click()
        # Switch to the new window that opened
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        window_handles = driver.window_handles
        child_window_handle = [handle for handle in window_handles if handle != driver.current_window_handle][0]
        driver.switch_to.window(child_window_handle)

        # Now interact with the elements in the child window
        # For example, click on the "Sign In" button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'imageLogin'))
        )
        sign_in_button.click()
        # driver.close()

        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

        Logger.LOG("Successfully logged into BUFF")
        Logger.LOG("Redirecting to BUY URL")
        #Redirect to buying URL
        driver.get(url_to_buy)
        Logger.LOG("Finding items")
        while(1):
            #TODO: UNCOMMENT THIS TO ALLOW LOOP AND REMOVE ELEMENT INTERCEPT ERROR
            driver.refresh()
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'list_tb_csgo')))
            for element in elements:
                # Find all <tr> elements with an ID within the current 'list_tb_csgo' element
                tr_elements_with_id = element.find_elements(By.XPATH, ".//tr[@id]")

                #No items found
                if(len(tr_elements_with_id)==0):
                    Logger.LOG("No item found.")
                    driver.refresh()
                else:
                    #The first row
                    tr_element=tr_elements_with_id[0]
                    t_left_element = tr_element.find_element(By.CLASS_NAME, 't_Left')

                    # Find the 'csgo_value' div within the 't_Left' element
                    csgo_value_div = t_left_element.find_element(By.CLASS_NAME, 'csgo_value')
                    # Find the 'wear-value' div within the 'csgo_value' div
                    float_value_div = csgo_value_div.find_element(By.CLASS_NAME, 'wear-value')
                    # Get and print the contents inside the 'wear-value' div
                    item_float = float_value_div.text

                    # Get and print the contents of the 'f_Strong' element
                    price_element = tr_element.find_element(By.CLASS_NAME, 'f_Strong')
                    item_price = price_element.get_attribute("innerHTML")
                    
                    scroll_value = 1000  # You can adjust this value based on your needs
                    Logger.LOG(f"ITEM FOUND! {item_float} , Price: {item_price}")
                    # Scroll horizontally
                    driver.execute_script(f"window.scrollBy({scroll_value}, 0);")
                    buy_button_td = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '(//td[@class="t_Left"])[5]')))
                    buy_button = buy_button_td.find_element(By.TAG_NAME, 'a')
                    buy_button.click()
                    # time.sleep(4)

                    popup_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'j_popup_epay')))

                    #Fetch available balance
                    balance_div = WebDriverWait(popup_element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pay-item.on h5.f_16px')))
                    alipay_balance = balance_div.text
                    available_balance=get_cleaned_price(alipay_balance)
                    current_price=get_cleaned_price(item_price)
                    Logger.LOG(f"Available Balance: {available_balance}")

                    #TODO: ADD BUY LOGIC HERE
                    if current_price <= available_balance:
                        try:
                            pass
                            # # Wait for the <a> tag inside 't_Center' to be clickable
                            # buy_button = WebDriverWait(popup_element, 10).until(EC.element_to_be_clickable((By.XPATH, './/div[@class="t_Center"]/a')))
                            # # Now you can interact with the <a> tag inside the 't_Center' class within the popup
                            # buy_button.click()
                            
                            # # Wait for the 'ask_seller_button' to be clickable
                            # send_offer_popup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'j_popup_payed')))
                            # ask_seller_button = WebDriverWait(send_offer_popup, 10).until(EC.presence_of_element_located((By.ID, 'ask_seller')))
                            # # Click on the anchor tag
                            # ask_seller_button.click()
                            # time.sleep(4)
                        except Exception as e:
                            Logger.LOG(f"Error during buy operation: {e}")
                    else:
                            Logger.LOG("Not enough balance. Skipping buy operation.")

            
    except Exception as e:
            print(e)

# initiate_buff_bot()
# start_buff_bot()