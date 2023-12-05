# -*- coding: utf-8 -*-
"""
- module to display movies based on user-entered keywords for Genres
- uses selenium to interact with website
- scrapes top rate movie names
- also scrape title of recipe to display in reponse along with link?

"""
import selenium
from selenium import webdriver
import time, traceback
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
PATH="C:/Users/Admin/Desktop/chromedriver.exe"

# SB : search box
# SR : search results

def get_movies(PATH) :
    
    input_genre = get_input_genre() #keyword_string.strip().split(",")
    success = True
    #urls = {"bonappetit":"https://www.bonappetit.com/", "allrecipes":"https://www.allrecipes.com/"}
    search_query="https://www.themoviedb.org/movie"
    
    result=[]
    #result_dict = {"bonappetit":[], "allrecipes":[]}
    
    try :
#------------------------------------------------------------------------------
        s = Service(PATH)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome(service = s,options = option)
        #service = s, 
        browser.get(search_query)

        filter_button=WebDriverWait(browser, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id=\"media_v4\"]/div/div/div[2]/div[1]/div[2]/div[1]")))[0]
        filter_button.click()

#------------------------------------------------------------------------------
#       selecting genres by user input

        if("action" in input_genre):
            genre1 = WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[1]")))
            genre1.click()
            time.sleep(1)
        if("adventure" in input_genre):
            genre2 = WebDriverWait(browser, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[2]")))
            genre2.click()
            time.sleep(1)
        if("comedy" in input_genre):
            genre3 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[4]")))
            genre3.click()
            time.sleep(1)
        if("drama" in input_genre):
            genre4 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[7]")))
            #WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located(()))[0]
            genre4.click()
            time.sleep(1)
        if("history" in input_genre):
            genre5 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[10]")))
            genre5.click()
            time.sleep(1)
        if("horror" in input_genre):
            genre6 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[11]")))
            genre6.click()
            time.sleep(1)
        if("mystery" in input_genre):
            genre7 = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"with_genres\"]/li[13]")))
            genre7.click()
            time.sleep(1)

        print("done clicking")
#------------------------------------------------------------------------------
        #loading filtered movies
        search_result=browser.find_element_by_xpath("//*[@id=\"media_v4\"]/div/div/div[2]/div[3]")
        search_result.click()      
        
        print("done loading")
#------------------------------------------------------------------------------
        #storing data form movie cards into dataframe
        
        card=[""]*10                    #store instance of card web element, because Stale exception
        percent=[""]*10                 #store instance of footer of card web element, because Stale exception
    
        df_list=[]                      #store list to create dataframe
    
        for i in range(len(card)):
            time.sleep(3)
            
            print("fetching data...")
            
            card[i]=browser.find_element_by_xpath("//*[@id=\"page_1\"]/div[{}]/div[2]".format(i+1))
            percent[i]=browser.find_element_by_xpath("//*[@id=\"page_1\"]/div[{}]/div[2]/div/div/div".format(i+1))
            
            movie_name=card[i].find_elements_by_tag_name("a")[0].text
            release_date=card[i].find_elements_by_tag_name("p")[0].text
            rating=percent[i].get_attribute("data-percent")
            
            df_list.append((movie_name,release_date,rating))
    
        df_movies = pd.DataFrame(df_list, columns =['Name', 'Date', 'Rating'])
            
#------------------------------------------------------------------------------
    
    except Exception as e: 
        print("movie_scraping :: get_movies :: ",e)
        traceback.print_exc()
        success = False
        browser.close() #closes tab
        return pd.DataFrame([])
    
    browser.close()
    return df_movies, success

def get_input_genre():
    return_genre=[]             
    print("Enter your choices of genre: Action/Adventure/Comedy/Drama/Histoy/Horror/Mystery")
    input_genre=input("")
    for i in input_genre.strip().split(","):
        return_genre.append(i.strip())

    #debugging
    print(return_genre)
    return return_genre

print(get_movies(PATH)[0])