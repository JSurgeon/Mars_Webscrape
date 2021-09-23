# Mars Webscrape

  This repository contains work related to my first web-scraping project. The repo's Mission_to_Mars folder includes: a jupyter notebook, where the initial scraping was handled and tested; a python script (scrape_mars.py) which is the testing jupyter notebook converted into a python script and turned into a function called scrape(); a python script which runs the web-interface Flask module, and finally a "templates" folder which itself holds the html file used by Flask to render the final webpage.

## Jupyter notebook (mission_to_mars.ipynb) and python (scrape_mars.py) scraping scripts
  The scraping done in these nearly identical scripts is done mainly using the BeautifulSoup and splinter modules. The scripts visit various https using splinter and parse each using BeautifulSoup to grab the essential information. All the scraping was tested in jupyter notebook, and once the scraping was being done successfully I converted the jupyter notebook to the python script and functionalized the entire script. The function that scrape_mars.py calls (scrape()) return a dictionary containing all the scraped info, connected with relevant key names such as "news_title" and "syrtis_image". Note: the python and jupyter notebook differ in how they handle the hemisphere data- jupyter adds the hemisphere data as a single array, while the python script individualized each entry to avoid use of an array.
  
## Python script app.py
  app.py takes advantage of the Flask and flask_pymongo modules to create the app routes for the webpage and to store scraped data via mongo. The index route "/" will show titles to each section on initial render, but will fill in appropriately once scraped (the webpage uses the term "launch" to scrape -- this seemed contextually relevant). The scraping route "/scrape" will be visited when the user hits the launch button from "/"- /scrape then calls scrape_mars.py's function scrape() and stores the data into a Mongo Database (but drops that db if it already exists to avoid appending the same data if someone had already scraped). Then, /scrape returns the user to the index page (/), to which the index page uses the information populated in Mongo to render the page via the index.html page
  
## index.html (exists in templates folder, as Flask's render_template expects)
  index.html is a simple html file that utilizes bootstrap to populate the scraped data onto the user's browser. More could be added to this file to make it more aesthetically pleasing, but gets the job done as is.
  
## Images Folder
  The images folder in this repo contains two pictures depicting the final webpage product. The entire page didnt fit on one screenshot, hence the two images. Again, more could be done to make the webpage more visually pleasing.
