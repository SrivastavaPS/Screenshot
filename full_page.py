from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from seleniumwire import webdriver as wire
from selenium import webdriver
from PIL import Image
import os
import sys
import errno
from datetime import datetime
import time
import pytz
from calendar import timegm
from alright import WhatsApp

###### making directory according to timestamp

IST = pytz.timezone('Asia/Kolkata')
d = datetime.now(IST)
#todo: why seconds and minutes ? 
d = d.strftime("%Y-%m-%d_%H:%M:%S")
#todo: use relative or config path from args
path = os.path.join("./myss/ss",d)
os.mkdir(path)

##### sleep periods
sleep_period = 2
whatsapp_sleep_period = 2
prom_start_sleep_period = 5

##### define chrome option for whatsapp
# todo: add whatsapp in method name 
def get_chrome_options():
        chrome_options = Options()
        if sys.platform == "win32":
            chrome_options.add_argument('--profile-directory=Default')
            chrome_options.add_argument(
                '--user-data-dir=C:/Temp/ChromeProfile')
        else:
            chrome_options.add_argument('start-maximized')
            chrome_options.add_argument('--headless')
            #chrome_options.add_argument('--no-sandbox')
            #chrome_options.add_argument('--disable-dev-shm-usage')
            #chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_argument('--user-data-dir=./User_Data_Whatsapp')
        return chrome_options

##### define authentication for nagios and pager duty

def interceptor(request):
    del request.headers['Authorization']  # Delete the header first
    request.headers['Authorization'] = 'Basic bmFnaW9zYWRtaW46bmFnaW9z'
    request.headers['Cookie'] = 'pd_referrer=_none_; _ga=GA1.2.412819499.1643701623; remember_user_token=BAhbCFsGaQPs%2F6BJIhkySmJiYUpzRjNoS3BheXlSekh6NAY6BkVUSSIXMTY0MzcwMTY5Ni41NjYxNTExBjsARg%3D%3D--8dc7c896d461f9de092face42ee525168cc62e32; pd_subdomains=BAhbBkkiDWJiYWxlcnRzBjoGRVQ%3D--5e887babbfbdcca383d5566e498e1e7e3e068e30; ajs_user_id=%22PKNNCA8%22; ajs_anonymous_id=%226ac29f28-1252-467b-baa2-2861ae3239b8%22; __zlcmid=18KkfpOleB6gcDi; _gcl_au=1.1.1018960081.1643704631; ajs_group_id=%22PH5Y3YQ%22; _gid=GA1.2.1382337596.1644095705; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Feb+06+2022+02%3A45%3A08+GMT%2B0530+(India+Standard+Time)&version=6.18.0&isIABGlobal=false&hosts=&consentId=d783ba8a-be8f-42fd-b88e-7e7c7ea925cd&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _pagerduty_session=BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJWI2MTg2NjJhYmU0MjUzMjJiMTEyZGY2ZWE4YWYxMWZhBjsAVEkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjsAVFsHWwZpA%2Bz%2FoEkiIiQyYSQxMyRxWEM1TEhUQm5iSGUwMHZWR2JKTUhlBjsAVEkiEnBkX3Nlc3Npb25faWQGOwBUSSIlMDgyZTFkYTcyOTM3Mzk2ZTZiNGYxYzQyZjJlYWZhZDEGOwBGSSIQX2NzcmZfdG9rZW4GOwBGSSIxczRmVUhVZnZwZVl2UFN6dUYybWtlSnhuK0loMi8wYi92YnRoUWNPVjMxWT0GOwBG--eddd8c6412bd4bc8bad649d3182c5639d0b66fe7'
    print(request.headers)

##### define chromiun option for pager duty, prometheus, & nagios

chrome_options = get_chrome_options()
#todo: make another method for basic chrome options 
chromium_options = Options()
chromium_options.add_argument('--start-maximized')
chromium_options.add_argument('--headless')
driver = wire.Chrome(chrome_options=chromium_options,executable_path='./driver/chromedriver')
driver.request_interceptor = interceptor          ##### for pager duty and nagios_automatic login

##### urls

url_pager_duty = "https://bbalerts.pagerduty.com/alerts"
#url_prometheus = "https://bbalerts.pagerduty.com/alerts"
#url_nagios = "https://bbalerts.pagerduty.com/alerts"

url_prometheus = "https://prometheus-prod2.k8s.bankbazaar.com/alerts"
url_nagios = "http://nagios.bankbazaar.com/cgi-bin/nagios3/status.cgi?host=all&servicestatustypes=28&hoststatustypes=3&serviceprops=42&sorttype=2&sortoption=3&sorttype=2&sortoption=3"

##### image names

image_name_1 = 'pager_duty.png'
image_name_4 = 'pager_duty_cropped.png'
image_name_2 = 'Promotheus.png'
image_name_5 = 'Promotheus_cropped.png'
image_name_3 = 'Nagios.png'
image_name_6 = 'Nagios_cropped.png'

##### images to be saved at

to_save_at_1 = os.path.join(path, image_name_1)
to_save_at_1_cropped = os.path.join(path, image_name_4)
to_save_at_2 = os.path.join(path, image_name_2)
to_save_at_2_cropped = os.path.join(path, image_name_5)
to_save_at_3 = os.path.join(path, image_name_3)
to_save_at_3_cropped = os.path.join(path, image_name_6)

##### images to be sent at
# todo separate test and live 
#group_name = 'SRE Alerts'
group_name = 'Personal'


######################################################### SS Start ###################################################################
######################################################################################################################################

######################################################### PAGER DUTY #################################################################

driver.get(url_pager_duty)
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height'))
time.sleep(sleep_period)

"""
######### Summary_sorting
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[4]/div/div/div/div[1]/div/button')
element.click()
time.sleep(sleep_period)
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[4]/div/div/div/div[2]/div[2]/form/div[1]/input')
element.send_keys("SRE-Pro")
time.sleep(sleep_period)
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[4]/div/div/div/div[2]/div[2]/form/div[2]/button')
element.click()
time.sleep(sleep_period)
"""

######### Created_sorting 
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[5]/div/div/div/div/div/button')
element.click()
time.sleep(sleep_period)
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[5]/div/div/div/div[2]/div[2]/form/div[1]/select')
element.click()
time.sleep(sleep_period)
#### 1 hour
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[5]/div/div/div/div[2]/div[2]/form/div[1]/select/option[2]')
#### 24 hour
#element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[5]/div/div/div/div[2]/div[2]/form/div[1]/select/option[3]')
element.click()
time.sleep(sleep_period)
element = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[3]/table/thead/tr/th[5]/div/div/div/div[2]/div[2]/form/div[2]/button')
element.click()
time.sleep(sleep_period)

#el = driver.find_element_by_class_name('pd-page-content')   ### full page vala ss with Alert and uska background
el = driver.find_element_by_xpath('//*[@id="ember38"]')
#el = driver.find_element_by_xpath('//*[@id="ember9"]/div/div')    ### full page vala ss with Alert (uske phle ka background ni hai)
el.screenshot(to_save_at_1)
screenshot = Image.open(to_save_at_1)


location = el.location
size = el.size
w, h = size['width'], size['height']

#print(location)
#print(size)
#print(w, h)


left = 0 + 280
top = 0
right = w - 360
bottom = h
im = Image.open(to_save_at_1)
im = im.crop((left,top,right,bottom))
im.save(to_save_at_1_cropped) # saves the image
#im.show()




############################################################## Prometheus  ##########################################################

driver.get(url_prometheus)
time.sleep(prom_start_sleep_period)
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height'))

element = driver.find_element_by_css_selector("#inactive-toggler").click()
element = driver.find_element_by_css_selector("#pending-toggler").click()

el = driver.find_element_by_tag_name('body')
el.screenshot(to_save_at_2)
screenshot = Image.open(to_save_at_2)
#screenshot.show()

############################################################## Nagios  ###############################################################


driver.get(url_nagios)
S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height'))

el = driver.find_element_by_xpath('/html/body/table[3]')
el.screenshot(to_save_at_3)
screenshot = Image.open(to_save_at_3)
#screenshot.show()


location = el.location
size = el.size
w, h = size['width'], size['height']

#print(location)
#print(size)
#print(w, h)


left = 0
top = 0
right = w -300
bottom = h
im = Image.open(to_save_at_3)
im = im.crop((left,top,right,bottom))
im.save(to_save_at_3_cropped) # saves the image
#im.show()




############################################################## SS Done ###############################################################
driver.quit()
######################################################################################################################################

##### open whatsapp
"""
options_fire = webdriver.FirefoxOptions()
options_fire.set_preference('profile','/usr/lib/firefox /profile/whatsapp')
#options_fire.add_argument('--headless')
profile = webdriver.FirefoxProfile('/home/user-name-pc/.mozilla/firefox/1kj45idd.default')

browser = webdriver.Firefox(executable_path='./driver_firefox/geckodriver',firefox_profile=profile,options=options_fire)

#browser = webdriver.Chrome(
                #executable_path='./driver/chromedriver',
                #ChromeDriverManager().install(),
                #options=get_chrome_options())
                #options=chrome_options)

messenger = WhatsApp(browser)
messenger.find_by_username(group_name)

messenger.send_picture(to_save_at_1)
time.sleep(whatsapp_sleep_period)

messenger.send_picture(to_save_at_2)
time.sleep(whatsapp_sleep_period)

messenger.send_picture(to_save_at_3)
time.sleep(whatsapp_sleep_period)

messenger.send_picture(to_save_at_4)
time.sleep(whatsapp_sleep_period)

messenger.send_picture(to_save_at_6)
time.sleep(whatsapp_sleep_period)

time.sleep(sleep_period)
time.sleep(sleep_period)
time.sleep(sleep_period)
time.sleep(sleep_period)
time.sleep(sleep_period)
time.sleep(sleep_period)

browser.close()
"""
############################################################### END ##################################################################
