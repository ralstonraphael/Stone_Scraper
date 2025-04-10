# --- Web scraping and browser automation libraries ---
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By

# --- HTML parsing ---
from bs4 import BeautifulSoup

# --- Environment variable management ---
import os
from dotenv import load_dotenv

# Load environment variables from a .env file for secure credentials
load_dotenv()


# --- ClientConfig class handles authentication with Bright Data's proxy service ---
class ClientConfig:
    def __init__(self, username, password, zone='ai_scraper'):
        # Ensure all credentials are present before continuing
        if not username or not password:
            raise ValueError("Missing Bright Data credentials.")
        self.username = username
        self.password = password
        self.zone = zone  # Bright Data allows multiple zones for different projects

    # Constructs the proxy URL using Bright Data’s formatting requirements
    def get_auth_url(self, base_url):
        auth = f'brd-customer-{self.username}-zone-{self.zone}:{self.password}'
        return f'https://{auth}@{base_url}'


# --- Main web scraping function: launches headless browser, loads page, returns HTML ---
def scrape_website(website):
    base_url = 'brd.superproxy.io:9515'  # Bright Data WebDriver proxy endpoint
    username = os.getenv('BRIGHTDATA_USERNAME')  # Securely loaded from environment
    password = os.getenv('BRIGHTDATA_PASSWORD')
    zone = os.getenv('BRIGHTDATA_ZONE', 'ai_scraper')  # Defaults to 'ai_scraper' if not set

    # Create authenticated proxy config
    client_config = ClientConfig(username, password, zone)
    sbr_webdriver = client_config.get_auth_url(base_url)

    print("Connecting to Scraping Browser...")
    # Establish connection to the remote browser via Bright Data WebDriver
    sbr_connection = ChromiumRemoteConnection(sbr_webdriver, 'goog', 'chrome')
    
    # Launch the browser using Selenium Remote
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get(website)  # Navigate to the target URL

        # Save a screenshot of the page for visual validation/debugging
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')

        print('Navigated! Scraping page content...')
        html = driver.page_source  # Get the full page HTML
        print('Scraped! Closing connection...')
        return html


# --- Extract the <body> content from the HTML (removes header, metadata, etc.) ---
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return str(body_content)  # Return only the <body> HTML as a string
    return ""


# --- Clean the HTML body content by removing scripts/styles and extraneous whitespace ---
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    # Remove all <script> and <style> tags to prevent noise in parsed content
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

        # Get clean text from HTML and normalize line breaks
        cleaned_content = soup.get_text(separator="\n")

        # Remove empty lines and strip leading/trailing whitespace
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )

        return cleaned_content


# --- Break long strings of DOM text into chunks for LLM processing (e.g., for API limits) ---
def split_dom_content(dom_content, max_length=6000):
    # Returns a list of chunks no longer than max_length, preserving character boundaries
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
