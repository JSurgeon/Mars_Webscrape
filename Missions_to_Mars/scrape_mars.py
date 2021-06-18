# Mission to Mars jupyter notebook file
# Jonathan Surgeon 6/7/21

#import dependencies

from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 
import time
from pprint import pprint
def scrape():
    ###################################
    # # Nasa Mars News
    ###################################

    # assign title and paragraph text to variables
    flag = 0
    while flag == 0:
        try:
            url = "https://redplanetscience.com"
            executable_path = {'executable_path': ChromeDriverManager().install()}
            browser = Browser('chrome', **executable_path,headless=False)
            browser.visit(url)
            html = browser.html
            soup = BeautifulSoup(html,"html.parser")
            titles = soup.find_all("div", class_="content_title")
            news_title = titles[0].text
            paragraphs = soup.find_all("div", class_="article_teaser_body")
            news_p = paragraphs[0].text
            flag = 1
        except:
            news_title = "No title scraped, try again"
            news_p = "No paragraph scraped, try again"
        browser.quit()
    ###################################
    # # JPL Mars Space Images - Featured Image
    ###################################

    # splinter setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path,headless=False)
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    # click "FULL IMAGE" button 
    browser.links.find_by_partial_text("FULL IMAGE").click()

    # save browser html in variable
    html = browser.html

    # create BeautifulSoup object
    soup = BeautifulSoup(html,'html.parser')
    # use soup object to find specific image, save the image's url
    image_result = soup.find_all("img", {"class":"fancybox-image"})
    
    image = image_result[0]["src"]
    # create full url
    surface_url = url + image
    
    # quit the browser
    browser.quit()

    ###################################
    # # Mars Facts
    ###################################

    # set url appropriately
    url = "https://galaxyfacts-mars.com/"

    # read tables from url
    tables = pd.read_html(url)

    # convert correct table to dataframe
    table_df = pd.DataFrame(tables[1])
    # reassign column names
    table_df.columns = ["attribute","value"]
    # set index of dataframe
    table_df = table_df.set_index("attribute")

    # convert dataframe to html table
    html_table = table_df.to_html()

    ###################################
    # # Mars Hemispheres
    ###################################

    # splinter setup
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path,headless=False)
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]
    hemi_entries = []

    for hemi in hemispheres:
        # click into hemisphere link
        browser.links.find_by_partial_text(hemi + " Hemisphere Enhanced").click()
        # pull html, soupify
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        # find image url
        li = soup.find_all('li')
        a= li[0].find('a')
        image_url = url+a['href']
        
        # add image url to dictionary 'hemi_entries'
        hemi_entries.append({"title": hemi + " Hemisphere Enhanced", "img_url": image_url})

        # go back to original webpage
        browser.links.find_by_partial_text("Back").click()
    
    browser.quit()

    ###################################
    # create final dictionary to return
    ###################################

    mars_dictionary = {
        "news_title": news_title,
        "news_paragraph" : news_p,
        "surface_url" : surface_url,
        "fact_table" : html_table,
        "cerberus_title" : hemi_entries[0]['title'],
        "cerberus_img" : hemi_entries[0]['img_url'],
        "schiap_title" : hemi_entries[1]['title'],
        "schiap_img" : hemi_entries[1]['img_url'],
        "syrtis_title" : hemi_entries[2]['title'],
        "syrtis_img" : hemi_entries[2]['img_url'],
        "valles_title" : hemi_entries[3]['title'],
        "valles_img" : hemi_entries[3]['img_url'],
        }
    
    return(mars_dictionary)
#info = scrape()
#print(f'type of scrape is{type(info)}')
#pprint(info)