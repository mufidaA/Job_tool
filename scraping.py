from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Set up Selenium WebDriver (you need to have the appropriate driver installed)
# For example, for Chrome: https://sites.google.com/chromium.org/driver/
driver = webdriver.Chrome()

url = "https://oulucompanies.fi/en/company-database/"
driver.get(url)

# Initialize an empty list to store company data
data = []
company_count = 0  # Initialize the company count
show_more_clicks = 0  # Initialize the show more clicks counter

max_retries = 10
for _ in range(max_retries):
    try:
        # Wait for the "Show More" button to become clickable
        wait = WebDriverWait(driver, 10)
        show_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fwp-load-more")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Click the "Show More" button
        show_more_button.click()

        show_more_clicks += 1  # Increment the counter
        
        time.sleep(2)  # Add a 2-second delay between clicks

        # Wait for the new content to load (adjust the time according to your needs)
        WebDriverWait(driver, 10).until(EC.staleness_of(show_more_button))
        break
    except:
        # If the "Show More" button is not found, break the loop
        pass


# Once all job items are loaded, get the page source
page_content = driver.page_source

driver.quit()

soup = BeautifulSoup(page_content, "html.parser")

company_items = soup.find_all("div", class_="col-md-4")

# Loop through div elements with class "col-md-4"
for company_item in company_items:
    company_title = company_item.find("h2", class_="company-card__title").get_text(strip=True)
    company_discription = company_item.find("div", class_="entry-summary").get_text(strip=True)
    company_link = company_item.find("a", class_="company-card__cta")['href']
    company_count += 1
    print("Company Title:", company_title)
    print("Company Link:", company_link)
    print("---------------------------------------------------")

    # Append company data to the data list
    data.append({"company": company_title, "summary": company_discription, "link": company_link})
data.append({"total_companies": company_count})
print("Total show more clicks:", show_more_clicks)

# Write the entire data list to the JSON file
with open("companies.json", "w") as json_file:
    json.dump(data, json_file, indent=2)  # Use indent for prettier formatting
