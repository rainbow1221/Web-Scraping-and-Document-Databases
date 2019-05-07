# Import dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests

# Create initialize browser function
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info = {}

    # NASA MARS NEWS
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from Mars news
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p


    # FEATURED IMAGE
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_image_url)

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Dictionary entry for featured image
    mars_info['featured_image_url'] = featured_image_url

    # MARS WEATHER

    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets
    tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for tweet in tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    # Dictionary entry
    mars_info['weather_tweet'] = weather_tweet

    # MARS FACTS
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames and assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Save html code 
    mars_data = mars_df.to_html(index=False)

    # Dictionary entry
    mars_info['mars_facts'] = mars_data


    # MARS HEMISPHERES
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for item in items: 
        # Store title
        title = item.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup(partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    # Dictionary entry
    mars_info['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_info
    
