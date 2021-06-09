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

def scrape():
    ###################################
    # # Nasa Mars News
    ###################################

    # assign title and paragraph text to variables... manually?
    news_title = "NASA Invites Students to Name Mars 2020 Rover"
    news_p = "Through Nov. 1, K-12 students in the U.S. are encouraged to enter an essay contest to name NASA's next Mars rover."
    #url = "https://redplanetscience.com"
    #response = requests.get(url)
    #soup = BeautifulSoup(response.text,"html.parser")
    #soup
    # how to retrieve dynamic html content using python

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
    
    #print(f'\n\n\n{image_result[0]['src']}\n\n\n')
    image = image_result[0]["src"]
    # create full url and print to verify
    surface_url = url + image

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
    table_df.set_index("attribute")

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
        dd = soup.find_all('dd')
        a = dd[1].find('a')
        image_url = url + a['href']
        
        # add image url to dictionary 'hemi_entries'
        hemi_entries.append({"title": hemi + " Hemisphere Enhanced", "img_url": image_url})

        # go back to original webpage
        browser.links.find_by_partial_text("Back").click()
        

    ###################################
    # create final dictionary to return
    ###################################

    mars_dictionary = {
        "news_title": news_title,
        "news_paragraph" : news_p,
        "surface_url" : surface_url,
        "fact_table" : html_table,
        "hemisphere_data" : hemi_entries
    }

    return(mars_dictionary)

print(scrape())