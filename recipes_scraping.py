# -*- coding: utf-8 -*-
"""
- module to find recipes based on user-entered keywords from bonappetit, allrecipes, and epicurious
- uses selenium to enter keywords in search bar of the website
- scrapes recipe article links from the search results 
- also scrape title of recipe to display in reponse along with link?

"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
PATH="C:/Users/Admin/Documents/chromedriver.exe"

# SB : search box
# SR : search results

def get_recipes(keyword_string , PATH) :
    
    success = True
    urls = {"bonappetit":"https://www.bonappetit.com/", "allrecipes":"https://www.allrecipes.com/"}
    result_dict = {"bonappetit":[], "allrecipes":[]}
    
    try :
#------------------------------------------------------------------------------
        s = Service(PATH)
        #option = webdriver.ChromeOptions()
        #option.add_argument('headless')
        driver = webdriver.Chrome(service = s)#, options = option)
#------------------------------------------------------------------------------
# enter keyword string in the search bar on bonappetit and get results

        driver.get(urls.get("bonappetit"))
        bonappetit_SB = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.ID, "search-form-text-field-q")))[1]
        bonappetit_SB.click()
        bonappetit_SB.send_keys(Keys.HOME)
        bonappetit_SB.send_keys(keyword_string)
        bonappetit_SB.send_keys(Keys.RETURN)
        
        bonappetit_SR = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "recipe-content-card")))
        
        for card in bonappetit_SR :
            title_desc_link = card.text.splitlines()
            title_desc_link.pop(0)
            
            a = card.find_element(by = By.TAG_NAME, value = 'a')
            link = str(a.get_attribute("href"))    
            title_desc_link.append(link)
            
            result_dict.get("bonappetit").append(tuple(title_desc_link))
            
#------------------------------------------------------------------------------

        driver.get(urls.get("allrecipes"))
        allrecipes_SB = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "search-block")))
        allrecipes_SB.click()
        allrecipes_SB.send_keys(Keys.HOME)
        allrecipes_SB.send_keys("shortbread")
        allrecipes_SB.send_keys(Keys.RETURN)
        
        allrecipes_SR = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card__detailsContainer")))
        
        for card in bonappetit_SR :
            title_desc_link = card.text.splitlines()
            title_desc_link.pop(1)
            title_desc_link.pop(1)
            
            a = card.find_element(by = By.TAG_NAME, value = 'a')
            link = str(a.get_attribute("href"))    
            title_desc_link.append(link)
            
            result_dict.get("allrecipes").append(tuple(title_desc_link))
    
#------------------------------------------------------------------------------
        driver.close()
    
    except Exception as e: 
        print("recipes_scraping :: get_recipes :: ",e)
        success = False
        driver.close() #closes tab
    
    return result_dict, success
