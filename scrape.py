from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

class ClientConfig:
    def __init__(self, username, password, zone='ai_scraper'):
        if not username or not password:
            raise ValueError("Missing Bright Data credentials.")
        self.username = username
        self.password = password
        self.zone = zone

    def get_auth_url(self, base_url):
        auth = f'brd-customer-{self.username}-zone-{self.zone}:{self.password}'
        return f'https://{auth}@{base_url}'

# Usage in scrape_website
def scrape_website(website):
    base_url = 'brd.superproxy.io:9515'
    username = os.getenv('BRIGHTDATA_USERNAME')
    password = os.getenv('BRIGHTDATA_PASSWORD')
    zone = os.getenv('BRIGHTDATA_ZONE', 'ai_scraper')

    client_config = ClientConfig(username, password, zone)
    sbr_webdriver = client_config.get_auth_url(base_url)

    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(sbr_webdriver, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print('Scraped! Closing connection...')
        return html
    
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Extract the body content
    body_content = soup.find('body')
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    # Remove all script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

        cleaned_content = soup.get_text(separator="\n")
        # Remove leading and trailing whitespace
        cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
)
        return cleaned_content
    
#split batches
def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
