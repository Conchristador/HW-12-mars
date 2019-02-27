# Importing Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

# CHROME DRIVER
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_info = {}
    
# MARS NEWS
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at\
    +desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').text
    news_para = soup.find('div', class_='article_teaser_body').text 

# JPL IMAGE
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    image_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = f"https://www.jpl.nasa.gov{image_url}"
    
# WEATHER TWEET
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    tweets = soup.find_all('div', class_="js-tweet-text-container")

    for tweet in tweets:
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else:
            pass

# MARS FACTS
    url_4 = 'https://space-facts.com/mars/'

    mars_data = pd.read_html(url_4)
    mars_df = (mars_data[0])
    mars_df.columns = ['Description', 'Data']
    mars_df = mars_df.set_index('Description')


    mars_html = mars_df.to_html(classes='mars-data')
    mars_html = mars_html.replace('\n', ' ')

    
# Hemispheres
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    images = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    base_url = "https://astrogeology.usgs.gov"
    
    for image in images: 
            title = image.find('h3').text
            img_link = image.find('a')['href']
            full_link = base_url + img_link

            browser.visit(full_link)

            html=browser.html
            soup=BeautifulSoup(html, 'html.parser')

            image_link = soup.find("img", class_="wide-image")["src"]
            img_url = base_url + image_link

            hemisphere_image_urls.append({'title': title, 'img_url': img_url})

    hemisphere_image_urls
        
    mars_info["news_title"] = news_title
    mars_info["news_para"] = news_para
    mars_info["featured_image_url"] = featured_image_url
    mars_info["mars_weather"] = mars_weather
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls
    
    browser.quit()
    
    return mars_info