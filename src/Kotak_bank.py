

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from tqdm import tqdm
import time
import pandas as pd


browser = webdriver.Chrome(executable_path=r"..\res\chromedriver.exe")
browser.get('https://www.kotak.com/en/offers/view-all-offers/most-Popular-offers.html')
lastHeight = browser.execute_script("return document.body.scrollHeight")
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(5)
    newHeight = browser.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight



elems = browser.find_elements_by_partial_link_text('Show')
elems_link =[elem.get_attribute("data-href") for elem in elems]


all_details ={}
all_offers = pd.DataFrame()


for offrs in elems_link:
    all_details ={}
    browser.get(offrs.replace('/content/kotakcl/','https://www.kotak.com/'))
    time.sleep(5)
    all_details['offer_details'] = browser.find_element_by_id('offer_title').text
    all_details['vouchr_dealits'] = browser.find_element_by_id('voucherDetails').text
    paragraph_text = browser.find_elements_by_tag_name('li')
    paragraph_text = [x.text for x in paragraph_text]
    paragraph_text = [x for x in paragraph_text if x]
    all_details['rendeem_text'] = ' '.join(paragraph_text[:-57])

    #browser.find_element_by_partial_link_text('Terms and Conditions').click()
    #term_text = browser.find_elements_by_xpath('//*[@id="terms"]/div/div/div/div/div')
    #term_text = [x.text for x in term_text]
    #term_text = [x for x in paragraph_text if x]
    #all_details['Term_conditions'] = term_text
    all_offers = all_offers.append(pd.DataFrame(all_details,index=[0]))


all_offers.reset_index(inplace=True)
all_offers.to_csv('../res/Citi.csv')
