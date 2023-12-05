# -*- coding: utf-8 -*-
"""
Created on Sat May 14 22:05:40 2022

@author: Sai
"""

#Web scraping TMDB movies with selenium, loading data into pandas

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


def load(PATH):
    # =============================================================================
    # Loading website
    # =============================================================================
    search_query="https://www.themoviedb.org/movie"
    browser=webdriver.Chrome("C:/Users/Admin/Documents/chromedriver.exe")
    browser.get(search_query)
    
    # =============================================================================
    # clicking on filter list
    # =============================================================================
    filter_button=browser.find_element_by_xpath('//*[@id="media_v4"]/div/div/div[2]/div[1]/div[2]/div[1]')
    filter_button.click()
    
    return filter_button,browser


# =============================================================================
# function to select genre buttons
# =============================================================================
def select_genre(input_genre, browser, filter_button):
    # sleep is needed so multiple buttons can be clicked
    #choices of genre: Action/Adventure/Comedy/Drama/Histoy/Horror/Mystery
    if("action" in input_genre):
        genre1=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[1]")
        genre1.click()
        time.sleep(3)
    if("adventure" in input_genre):
        genre2=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[2]")
        genre2.click()
        time.sleep(3)
    if("comedy" in input_genre):
        genre3=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[4]")
        genre3.click()
        time.sleep(3)
    if("drama" in input_genre):
        genre4=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[7]")
        genre4.click()
        time.sleep(3)
    if("history" in input_genre):
        genre5=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[10]")
        genre5.click()
        time.sleep(3)
    if("horror" in input_genre):
        genre6=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[11]")
        genre6.click()
        time.sleep(3)
    if("mystery" in input_genre):
        genre7=browser.find_element_by_xpath("//*[@id=\"with_genres\"]/li[13]")
        genre7.click()
        time.sleep(3)

# =============================================================================
# stores all the genres selected by user
# =============================================================================
def get_inputgenre( browser, filter_button):
    input_genre=[]             
    print("Enter your choices of genre: Action/Adventure/Comedy/Drama/Histoy/Horror/Mystery")
    while(True):
        user_genre=input("")
        if(user_genre==''):
            break
        input_genre.append(user_genre.lower())
    return input_genre

# =============================================================================
# applies the filter
# =============================================================================
def display_movies( browser, filter_button):
    search=browser.find_element_by_xpath("//*[@id=\"media_v4\"]/div/div/div[2]/div[3]")
    search.click()

# =============================================================================
# loads the top 10 movies into pandas dataframe and returns the dataframe
# =============================================================================
def store_data( browser, filter_button):
    #retrieve name and release date
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
    return df_movies, df_list

# =============================================================================
# Main Code 
# =============================================================================
def call(input_genre,PATH):
    #input_genre=get_inputgenre()
    filter_button, browser =load(PATH)
    select_genre(input_genre, browser, filter_button)
    display_movies( browser, filter_button)
    movie_df, movie_list=store_data( browser, filter_button)
    print(movie_df)
    return movie_df 











