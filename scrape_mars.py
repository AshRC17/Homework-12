# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import pymongo
from flask import Flask, render_template

nm_url = "https://mars.nasa.gov/news/"
nm_base_url = "https://mars.nasa.gov"
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
jpl_base_url = "https://www.jpl.nasa.gov"
mf_url = 'https://space-facts.com/mars/'
mh_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
mh_base_url = 'https://astrogeology.usgs.gov'

hem_url = [
    {"title": "Cerberus Hemisphere", "img_url":\
    "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Valles Marineris Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"}
]


nm_response = requests.get(nm_url)

nm_soup = bs(nm_response.text, 'html.parser')

def scrape():

    # Nasa Mars head title
    hl_title = nm_soup.body.find('div', class_="content_title").text.strip()
    print(hl_title.text.strip())

    ts_uri = hl_title.find('a')['href']
    print(ts_uri)
    ts_url = nm_base_url+ts_uri
    print(ts_url)
    ts_resp = requests.get(ts_url)
    ts_soup = bs(ts_resp.text, 'html.parser')
    ts_content = ts_soup.find_all('p')

    for portion in ts_content:
        print(portion.text.strip())

    # Start of JPL Mars Space Images Scraping
    executable_path = {'executable_path': '/usr/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    fi_class = jpl_soup.find('div', class_='carousel_items').find(id='full_image')
    fi_class
    fi_uri = fi_class['data-fancybox-href']
    featured_image_url = jpl_base_url+fi_uri
    featured_image_url

    # Mars Facts Webscraping
    mf_tables = pd.read_html(mf_url)
    mf_ptable = mf_tables[0]
    mf_ptable.rename(columns={0:"Attributes", 1:"Value"}, inplace=True)
    mf_ptable.set_index("Attributes", inplace=True)
    #mf_ptable.to_html('Output_file/mf_table.html', index=False)

app = Flask(__name__)

@app.route('/')
def echo():
    return render_template("index.html", text="Serving up cool text from the Flask server!!")


if __name__== "__main__":
    app.run(debug=True)
