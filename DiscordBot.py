# -*- coding: utf-8 -*-
"""
Created on Sun May 15 23:13:51 2022

@author: Admin
"""

TOKEN = "OTU4MzI4NTIwODIyNjQwNjUx.YkLu_A.Hp3fgou6dyUgLKXr3jlSpOeKlto"
PATH="C:/Users/Admin/Documents/chromedriver.exe"

#pip install discord
#import tmdb_automation
import recipes_scraping
import nest_asyncio
nest_asyncio.apply()

import discord

class MyClient(discord.Client):
    status_flag=""
    
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    #everthing that the user enters in chat is inputted as variable 'message'
    async def on_message(self,message):
        #to make sure that the bot does not respond to itself
        if message.author == client.user:
            return
        
        menu_options=["news","movies","recipes"]
        thread_list=[]
        thread=message.channel.history(limit=10)
        async for threads in thread:
            if (threads.author!=client.user):
                thread_list.append(threads.content)
                 
        
        status_flag=thread_list.pop(1)
        print(status_flag)            #debugging
        
        if(message.content not in menu_options and status_flag not in menu_options):
            await message.channel.send('''
            Menu
            1.News
            2.Recipes
            3.Movies
            ''')

        if(message.content=="news"):
            await message.channel.send('1.business 2.sports')

        if(status_flag=="news"):
            if(message.content=="business"):
                await message.channel.send('Entered News-->Business')
                #call business news scraping method
        
        elif(message.content=="recipes" and status_flag!="news"):
            await message.channel.send('Scraping recipes for you...')
            
        elif(message.content=="movies" and status_flag!="news"):
            await message.channel.send('Enter a genre (Action/Adventure/Horror/History)...')
        
        elif(status_flag=="movies"):
            #scrape movies 
            await message.channel.send('You entered the movie scraping function')
            result, success = recipes_scraping.get_recipes("Cookies",PATH)
            await message.channel.send(str(result))
            
            
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
            return 
'''

1.
    a.Business
    b.
    c.
2.
3.

'''
    
client = MyClient()
client.run(TOKEN)