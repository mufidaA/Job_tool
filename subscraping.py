import json
import time  # Import the time module
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Load the JSON data
with open("updated_companies.json", "r") as json_file:
    companies_data = json.load(json_file)

# Start a Chrome WebDriver
driver = webdriver.Chrome()

try:
    for company_data in companies_data:
        link = company_data.get("link")

        if link:
            driver.get(link)

            # Handle cookie consent if present
            try:
                cookie_consent_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
                cookie_consent_button.click()
            except:
                pass  # Cookie consent button not found or unable to click
            
            try:
                # Get the HTML content of the page
                page_source = driver.page_source

                # Create a Beautiful Soup object
                soup = BeautifulSoup(page_source, "html.parser")

                # Extract company information using Beautiful Soup
                company_name = soup.find("th", text="Company name").find_next("td").text.strip()
                website = soup.find("th", text="Www").find_next("a").text.strip()
                phone = soup.find("th", text="Phone").find_next("td").text.strip()
                email = soup.find("th", text="Email").find_next("td").text.strip()
                contact = soup.find("th", text="Contact").find_next("td").text.strip()
                business_sector_heading = soup.find("h2", class_="company-card__categories", text="Business sector")
                if business_sector_heading:
                    business_sector_paragraphs = business_sector_heading.find_next_siblings("p")
                    business_sector = " ".join([p.text.strip() for p in business_sector_paragraphs[-2:]])

                else:
                    business_sector = ""

                #Update the company_data dictionary
                company_data["Website"] = website
                company_data["Phone"] = phone
                company_data["Email"] = email
                company_data["Address"] = contact
                company_data["Business Sector"] = business_sector

            except Exception as e:
                print(f"An error occurred while processing {link}: {e}")
                continue  # Skip this company's data and continue with the next one
            
            # Update the JSON file with the updated data
            with open("updated_companies.json", "w") as json_file:
                json.dump(companies_data, json_file, indent=4)
            
            # Introduce a delay of 1 seconds between requests
            time.sleep(0.5)  # You can adjust the delay as needed

finally:
    driver.quit()
