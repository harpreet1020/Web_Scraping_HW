# Import Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import pymongo



def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Create dictionary for scraped data
    mars_data = {}

    # Visit Nasa page
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Scrape News to BS
    html = browser.html
    soup = bs(html, 'html.parser')

    # Collect latest News Title and Paragraph Text
    article = soup.find('div', class_='list_text')
    news_title = article.find('div', class_='content_title').text
    news_paragraph = article.find('div', class_='article_teaser_body').text


    # Visit JPL page
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    # Scrape page to BS
    html = browser.html
    soup = bs(html, 'html.parser')

    # Collect featured image URL
    article = soup.find('div', class_='carousel_container')
    footer = article.find('footer')
    link = footer.find('a')
    url = link['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov/' + url


    # Collect latest tweet from Mars Weather account
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_3)

    # Scrape page to BS
    html = browser.html
    soup = bs(html, 'html.parser')

    # Save latest Mars Weather Tweet text
    article = soup.find('div', class_='ProfileTimeline')
    content = article.find('div', class_='content')
    tweet = content.find('p').text

    # Scrape https://space-facts.com/mars/ for Mars Facts using Pandas
    url_4 = 'https://space-facts.com/mars/'
    browser.visit(url_4)

    mars_facts_df = pd.read_html(url_4)

    mars_facts_df = (mars_facts_df[0])

    mars_facts_df.columns = ['Description', 'Value']

    mars_facts_df = mars_facts_df.set_index("Description")
    mars_facts_df = mars_facts_df.to_html(classes='Description')
    mars_facts_df = mars_facts_df.replace('\n', ' ')



    # Add Data to dictionary
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph
    # Add Table to dictionary
    mars_data['mars_table'] = mars_facts_df
    # Add featured image URL to mars_data
    mars_data['featured_image_url'] = featured_image_url
    # Add data to mars_data
    mars_data['mars_weather'] = tweet


    return mars_data
