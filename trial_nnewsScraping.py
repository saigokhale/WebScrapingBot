# -- coding: utf-8 --
"""
- module to scrape business news articles from websites :
        "https://www.theguardian.com/business/all",
        "https://www.marketwatch.com/economy-politics?mod=top_nav",
        "https://www.business-standard.com/",
        "https://www.financialexpress.com",
        "https://www.bbc.com/news/world",
- uses beautifulsoup to scrape links for articles from these website pages

"""
import requests
from bs4 import BeautifulSoup

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

result_dict = {}
urls = ("https://www.theguardian.com/business/all",
        "https://www.marketwatch.com/economy-politics?mod=top_nav",
        "https://www.business-standard.com/",
        "https://www.financialexpress.com",
        "https://www.bbc.com/news/world"
        )

def get_business_links() :
    
    soup = get_soup(urls[0])
    result_dict['guardian'] = process_guardian(soup)
    
    soup = get_soup(urls[1])
    result_dict['marketwatch'] = process_marketwatch(soup)
    
    soup = get_soup(urls[2])
    result_dict['business-standard'] = process_business_standard(soup, urls[2])
    
# =============================================================================
#     res_list = []
#     for section in ["/market/", "/money/", "/economy/"] :
#         url = urls[3] + section
#         soup = get_soup(url)     
#         res_list.extend(process_financialexpress(soup, section))
#     result_dict['financialexpress'] = res_list
# =============================================================================
       
    soup = get_soup(urls[4])
    result_dict['bbc'] = process_bbc(soup, urls[4])
    
    return result_dict
    
def get_soup(url) :
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")    
    return soup

def process_guardian(soup):   
    res_list={"links":[],"texts":[]}
    containers = soup.find_all("div", class_= "fc-item__container")
    for container in containers:
        res_list["links"].append(container.find("a", href=True)['href'])
        # print(container['href'], "\n")
        # print(type(container)) # <class 'bs4.element.Tag'>
    for url in res_list["links"]:
        res_list["texts"].append(extract_guardian(url))  
    return res_list

def extract_guardian(url):
    res_list=[]
    soup=get_soup(url)
    
    header=soup.find("h1").text
    res_list.append("Header: "+header+".")
    
    sub_soup=soup.find("div",class_="dcr-1jw1u7l").find_all("p")
    for i in sub_soup:
        res_list.append(i.text.strip())
    return " ".join(res_list)

def process_marketwatch(soup):   
    res_list = {"links":[],"texts":[]}
    
    soup = soup.find("div", class_="column column--primary")
    links = soup.find_all("div", class_= "article__content")
    
    for link in links:
        res_list["links"].append(link.find("a", href = True)['href'])
        # print(link['href'], "\n")
        # print(type(link)) # <class 'bs4.element.Tag'>
    for url in res_list["links"]:
        res_list["texts"].append(extract_marketwatch(url))
        
    return res_list

def extract_marketwatch(url):
    soup=get_soup(url)
    res_list=[]

    header=soup.find_all("h1")[1].text
    res_list.append("Header "+header+".")
    
    sub_soup1=soup.find("div", class_="article__body article-wrap at16-col16 barrons-article-wrap").find_all("p")
    
    for i in sub_soup1:
        res_list.append(i.text.strip())
    return " ".join(res_list).strip()

def process_business_standard(soup, url):   
    res_list={"links":[],"texts":[]}
    
    link = soup.find("div", class_="top-section")
    res_list["links"].append(url + link.find("a", href = True)['href'])
    
    links = soup.find_all("div", class_= "article")
    
    for link in links:
        res_list["links"].append(url + link.find("a", href = True)['href'])
    
    for url in res_list["links"]:
        res_list["texts"].append(extract_business_standard(url))
        
        # print(link['href'], "\n")
        # print(type(link)) # <class 'bs4.element.Tag'>    
    return res_list

def extract_business_standard(url):
    soup=get_soup(url)
    res_list=[]
    
    header=soup.find("h1").text
    res_list.append("Header "+header+".")
    
    sub_soup=soup.find_all("span",class_="p-content")
    
    for i in sub_soup:
        res_list.append(i.text.strip())
    return "".join(res_list).strip()

def process_financialexpress(soup, section):   
    res_list = []
    links = soup.find_all("a", rel= "bookmark")
    for link in links:
        link = link['href']        
        if(link not in res_list and section in link) :            
            res_list.append(link)
        # print(link['href'], "\n")
        # print(type(link)) # <class 'bs4.element.Tag'>
        
        return res_list

#def extract_financialexpress(url):
    

def process_bbc(soup, url):
    res_list = {'links':[],'texts':[]}
    sub_soup=soup.find("div",class_="gel-layout__item gel-1/1 gel-3/5@xxl gs-u-display-none@xl gs-u-display-block@xxl")
    #print(sub_soup)
    links=sub_soup.find_all("div", class_="gel-layout__item gs-u-pb+@m gel-1/3@m gel-1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m")
    for i in links:
        res_list['links'].append("https://www.bbc.com"+i.find("a",href=True)['href'])
    for url in res_list['links']:
        res_list['texts'].append(extract_text_bbc(url)) 
    return res_list

def extract_text_bbc(url):
    soup=get_soup(url)
    res_list=[]
    
    header=soup.find(attrs={"id":"main-heading"}).text        #,class_="ssrcss-s5w35y-HeadingWrapper e1nh2i2l5").text
    res_list.append("Heading: "+header+".")
    
    sub_soup=soup.find_all(attrs={"data-component":"text-block"})
    
    for i in sub_soup:
        res_list.append(i.text)
    return "".join(res_list)



#helper function to check our output
def display_5results(name):
    count=0
    ret1=get_business_links()[name]["links"] #its a dictionary
    ret2=get_business_links()[name]["texts"] #its a dictionary
    
    for i,j in zip(ret1,ret2):
        count+=1
        print(i+"\n"+j)
        if(count==5):
            break

#input parameter= name of website in result dictionary.[guardian, marketwatch, business-insider, bbc]
display_5results("business-standard")
    
    
        
    