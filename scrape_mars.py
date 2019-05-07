from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape():
     
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = 'https://mars.nasa.gov/news/'

    browser.visit(news_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    news_title = soup.find_all('div', class_="content_title")[0].text
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text

    image_url_root = 'https://www.jpl.nasa.gov'
    image_url_specific ='/spaceimages/?search=&category=Mars'
    
    browser.visit(image_url_root + image_url_specific)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    scraped_url = soup.find('a', class_='button fancybox')["data-fancybox-href"]
    featured_image_url = image_url_root + scraped_url

    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(mars_twitter_url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(mars_facts_url)

    df = tables[0]
    df.columns = ['Measurement', 'Result']
    df.set_index('Measurement', inplace=True)

    html_table = df.to_html()

    html_table_clean = html_table.replace('\n', '')

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemisphere_image_urls = []

    for x in range(0, 4):
        browser.visit(hemispheres_url)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        xpath = '//div[@class="description"]/a'
        results = browser.find_by_xpath(xpath)
        click_url = results[x]
        click_url.click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url = soup.find('a', target='_blank')['href']
        image_title = soup.find('h2', class_='title').text
        dict = {'title':image_title, 'img_url':image_url}
        hemisphere_image_urls.append(dict)

    
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table_clean": html_table_clean,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_dict