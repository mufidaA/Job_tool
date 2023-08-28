from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


if len(sys.argv) != 2:
    print("Usage: python verifycompany.py <company_name>")
    sys.exit(1)

company_title = sys.argv[1]

try:
    driver = webdriver.Chrome()

    if company_title:
            driver.get("https://www.finder.fi/")

            # Handle cookie consent if present
            try:
                cookie_consent_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
                cookie_consent_button.click()
            except:
                pass  # Cookie consent button not found or unable to click

            # Handle user terms approval 
            try:
                user_terms_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                user_terms_button.click()
            except:
                pass  # User terms button not found or unable to click

            search_input = driver.find_element(By.NAME, "search")
            search_input.send_keys(company_title)

            search_button = driver.find_element(By.CLASS_NAME, "SearchBar__Submit")
            search_button.click()

            # Wait for the search results page to load
            wait = WebDriverWait(driver, 10)
            search_results_link = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "SearchResult__ProfileLink"))
            )
            search_results_link.click()


    input("Press Enter to close the browser...")

except Exception as e:
    print("An error occurred:", str(e))
finally:
    driver.quit()
