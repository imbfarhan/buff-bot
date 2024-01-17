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
import settings
import json

driver=None

settings_json_rel_path='settings.json'
settings_json_path=os.path.normpath(os.path.join(settings.abs_path, settings_json_rel_path))

# with open(settings_json_path, 'r') as file:
#     data = json.load(file)
#     url = data['LINK']
#     max_float = float(data['FLOAT'])
#     max_price = float(data['MAX_PRICE'])

# max_float=settings.max_float
printed=0
matched_items_list=[] #STRUCTURE [(FLOAT,DIV_ID)]
# max_price=settings.max_price #PRICE IS IN USD

#--FUNCTIONS
def get_cleaned_price(price_string):
    cleaned_price = re.sub(r'[^0-9.,]', '', price_string)
    cleaned_price = cleaned_price.replace(',', '.')
    try:
        price_float = float(cleaned_price)
        return price_float
    except ValueError:
        return float('inf')

def check_for_network_change_message(driver):
    # Checks for the network change message
    try:
        # Wait for a maximum of 2 seconds for the presence of the div
        WebDriverWait(driver, 1.5).until(EC.presence_of_element_located((By.ID, 'main-frame-error')))
        return True  # Return True if the div is found
    except Exception as e:
        return False

def check_for_error_message(driver):
    #Checks for the error message
    try:
        error_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'market_listing_table_message')))
        error_text = "There was an error getting listings for this item. Please try again later."
        return error_text in error_div.text
    except Exception as e:
        return False

# def check_for_no_listing(driver):
#     try:
#         error_div = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'market_listing_table_message')))
#         error_text = "There are no listings for this item."
#         return error_text in error_div.text
#     except Exception as e:
#         return False

def check_for_no_listing(driver):
    try:
        # Find the div with class "market_listing_table_message"
        div_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'market_listing_table_message')))
        # Check if there are any nested elements
        children = div_element.find_elements(By.XPATH, "./*")  # Find all immediate children elements

        # Return True if there are no children, False if there are children
        return len(children) == 0

    except Exception as e:
        # Handle any exceptions or return False
        return False
    
#TODO: ADD VPN RESTART LOGIC
def check_for_too_many_requests(driver):
    try:
        #Checks if too many requests. If too many, we rerun the VPN
        error_div = WebDriverWait(driver, 1.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'error_ctn')))
        error_h3 = error_div.find_element(By.TAG_NAME, 'h3')
        too_many_requests_text = "You've made too many requests recently. Please wait and try your request again later."
        return too_many_requests_text in error_h3.text
    except Exception as e:
        # If there's any exception, return False
        return False



def click_on_ten_items(driver):
    # Wait for the csfloat-utility-belt element to be present
    utility_belt_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'csfloat-utility-belt')))
    # Execute JavaScript to access the shadowRoot of csfloat-utility-belt
    utility_belt_shadow_root_script = 'return arguments[0].shadowRoot;'
    utility_belt_shadow_root = driver.execute_script(utility_belt_shadow_root_script, utility_belt_element)
    # Execute JavaScript to access the shadowRoot of csfloat-page-size inside csfloat-utility-belt
    page_size_script = '''
    var utilityBelt = arguments[0];
    var pageSize = utilityBelt.shadowRoot.querySelector("csfloat-page-size");
    var select = pageSize.shadowRoot.querySelector('select');
    select.value = '10';
    var event = new Event('change', { bubbles: true });
    select.dispatchEvent(event);
    '''
    driver.execute_script(page_size_script, utility_belt_element)
    # Introduce a sleep to wait for potential changes on the page
    time.sleep(5)

def is_dom_updated(driver):
    timeout=30
    try:
        # Store the current page source
        old_page_source = driver.page_source
        print("CHECKING DOM UPDATE")
        # Wait for the DOM to be updated
        WebDriverWait(driver, timeout).until(
            lambda d: d.page_source != old_page_source
        )

        # If the page source has changed, return True
        return True

    except Exception as e:
        # Handle exceptions (e.g., timeout, stale element reference)
        return False



def initiate_finder():

    with open(settings_json_path, 'r') as file:
        data = json.load(file)
        url = data['LINK']
    
    Logger.INITFINDERLOG()

    global driver
    #--DRIVER DEPENDENCIES
    driver_executable_path = settings.driver_path
    os.environ["webdriver.chrome.driver"] = driver_executable_path
    chrome_options = Options()
    csfloat_extension=settings.csfloat_path
    chrome_options.add_extension(csfloat_extension)
    chrome_options.add_argument(f'--chromedriver={driver_executable_path}')
    chrome_options.add_experimental_option("detach", True)
    #TODO: UNCOMMENT THIS LINE TO PREVENT DEBUGGING
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Create a webdriver instance
    driver = webdriver.Chrome(options=chrome_options)
    # Load the page
    # url = settings.URL
    driver.get(url)

    #Check for network change error in page
    while(check_for_network_change_message(driver)):
        Logger.LOG("ERROR:NETWORK CHANGE. REINITIALIZING")
        driver.refresh()
        time.sleep(1)

    #Check for too many requests
    while(check_for_too_many_requests(driver)):
        Logger.LOG("ERROR:TOO MANY REQUESTS. Restarting VPN")
        VPN_COMMANDS.RESTART_VPN()
        time.sleep(2)
        driver.refresh()
        time.sleep(2)

    # #Check for error
    # while(check_for_error_message(driver)):
    #     Logger.LOG("ERROR:GET LISTING. REINITIALIZING")
    #     driver.refresh()

    while(check_for_no_listing(driver)):
        Logger.LOG("ERROR:GET LISTING. REINITIALIZING")
        driver.refresh()
        time.sleep(1)

    # while(check_for_nested_elements(driver)):
    #     Logger.LOG("ERROR:NO CHILDREN DIV IN LISTING.REINITIALIZING")
    #     driver.refresh()

    click_on_ten_items(driver)

    Logger.LOG("Initialized FINDER BOT")

def start_finder():
    with open(settings_json_path, 'r') as file:
        data = json.load(file)
        url = data['LINK']
        max_float = float(data['FLOAT'])
        max_price = float(data['MAX_PRICE'])
    #--DECLARATIONS
    global driver
    driver.refresh()
    # initiate_finder()
    # #--DECLARATIONS
    # max_float=0.28
    # printed=0
    # matched_items_list=[] #STRUCTURE [(FLOAT,DIV_ID)]
    # max_price=2.3 #PRICE IS IN USD

    # #--DRIVER DEPENDENCIES
    # executable_path = "C:\\Users\\Farhan\\Desktop\\chromedriver-win64\\chromedriver.exe"
    # os.environ["webdriver.chrome.driver"] = executable_path
    # chrome_options = Options()
    # chrome_options.add_extension('C:\\Users\\Farhan\\Downloads\\CSFloat-Market-Checker.crx')
    # chrome_options.add_argument(f'--chromedriver={executable_path}')
    # #TODO: UNCOMMENT THIS LINE TO PREVENT DEBUGGING
    # # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # # Create a webdriver instance
    # driver = webdriver.Chrome(options=chrome_options)
    # # Load the page
    # url = 'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20(Field-Tested)'
    # driver.get(url)

    # #Check for error
    # error_message=check_for_error_message(driver)
    # if(error_message):
    #     Logger.LOG("ERROR:GET LISTING. REINITIALIZING")
    #     driver.refresh()

    # #Check for too many requests
    # too_many_requests=check_for_too_many_requests(driver)
    # if(too_many_requests):
    #     Logger.LOG("ERROR:TOO MANY REQUESTS. REINITIALIZING")
    #     VPN_COMMANDS.RESTART_VPN()

    # click_on_ten_items(driver)
    # Logger.LOG("BOT INITIALIZED")
    Logger.LOG("BUYER BOT started")

    while(1):
        try:
            print(f"MAX FLOAT:{max_float} MAX PRICE:{max_price}")
            Logger.LOG("Finding item")
            found=0

            #!!!BOTTLENECK!!!
            #Check for network change error in page
            while(check_for_network_change_message(driver)):
                Logger.LOG("ERROR:NETWORK CHANGE. REINITIALIZING")
                driver.refresh()
                time.sleep(1)
            
            while(check_for_too_many_requests(driver)):
                Logger.LOG("ERROR:TOO MANY REQUESTS. Restarting VPN")
                VPN_COMMANDS.RESTART_VPN()
                driver.refresh()
                time.sleep(2)
            
            while(check_for_no_listing(driver)):
                Logger.LOG("ERROR:GET LISTING. REINITIALIZING")
                driver.refresh()
                time.sleep(1)
        

            page_source = driver.page_source #get entire page

            #logic for clicking 10 from dropdown comes here
            
            # Wait for all csfloat-item-row-wrapper elements to be present
            elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'csfloat-item-row-wrapper')))


            # Iterate through each csfloat-item-row-wrapper element
            for element in elements:
                
                # Execute JavaScript to access the "Float" text content within the Shadow DOM
                float_script = 'return arguments[0].shadowRoot.querySelector("div").textContent;'
                float_value = driver.execute_script(float_script, element)
                item_float=float_value.split()

                # Check if the float value meets a certain condition (replace 'your_condition_value' with the desired condition)
                # Get the parent of the parent of csfloat-item-row-wrapper
                parent_of_parent_script = 'return arguments[0].parentNode.parentNode.outerHTML;'
                parent_of_parent_html = driver.execute_script(parent_of_parent_script, element)   # this is the parent div
                page_source = page_source.replace(element.get_attribute("outerHTML"), float_value)
                
                soup = BeautifulSoup(parent_of_parent_html, 'html.parser')
                div_id = soup.select_one('.market_listing_row')['id']
                specific_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, div_id)))

                price_element = specific_div.find_element(By.CLASS_NAME, 'market_listing_price_with_fee')
                uncleaned_price=price_element.text
                print(f"{item_float[1]} : PRICE {uncleaned_price}")

                try:
                    #Failproof check to prevent incorrect currency conversion
                    if(float(item_float[1])<=max_float):
                        price_element = specific_div.find_element(By.CLASS_NAME, 'market_listing_price_with_fee')
                        uncleaned_price=price_element.text
                        #If sold, continue
                        if(uncleaned_price=='Sold!'):
                            continue
                        elif("USD" not in uncleaned_price): #Price is not in USD
                            price_in_usd=False
                            Logger.LOG(f'ITEM FOUND: FLOAT VALUE:{str(item_float[1])} LISTING NO:{str(div_id)} PRICE: {uncleaned_price} (PRICE NOT IN USD)')
                            Logger.LOG("Stopping FINDER")
                            #TODO: CALL BUYER BOT TO ASK FOR PRICE
                            # driver.quit()
                            from Mediator import call_buyer_bot
                            call_buyer_bot({'FLOAT':str(item_float[1]),"LISTING":str(div_id)})

                        else: #Price is in USD
                            item_price=get_cleaned_price(uncleaned_price)
                            if(item_price<=max_price):
                                price_in_usd=True
                                Logger.LOG(f'ITEM FOUND: FLOAT VALUE:{str(item_float[1])} LISTING NO:{str(div_id)} PRICE: $ {item_price} (PRICE IN USD)')
                                Logger.LOG("Stopping FINDER")
                                #TODO: CALL BUYER BOT AND BUY ENFORCE A CHECK THERE
                                # driver.quit() #tab this
                                from Mediator import call_buyer_bot
                                call_buyer_bot({"FLOAT":str(item_float[1]),"LISTING":str(div_id)})
                            else:
                                continue

                        
                        found=1

       
                except Exception: #Exception here is if float of item didnt load, so we pass it
                    pass

            if(found==0):
                Logger.LOG("No item found")
            else:
                print("Match Found!")

        except Exception as e:
            Logger.LOG(e)
        driver.refresh()

# start_finder()