from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

driver = webdriver.Chrome()

base_url = "https://codingcollective.com/"
driver.get(base_url)

all_links = driver.find_elements(By.TAG_NAME, "a")

broken_links = []
valid_links = []

print(f"Total links found: {len(all_links)}")

for link in all_links:
    href = link.get_attribute("href")
    
    if href and base_url in href:
        try:
            response = requests.head(href, timeout=5)
            if response.status_code >= 400:
                print(f"Broken Link (Status {response.status_code}): {href}")
                broken_links.append(href)
            else:
                valid_links.append(href)
        except requests.exceptions.RequestException as e:
            print(f"Error checking link {href}: {e}")
            broken_links.append(href)

driver.quit()

print("Test Results")
print(f"Valid links found: {len(valid_links)}")
print(f"Broken links found: {len(broken_links)}")

if broken_links:
    print("List of broken links:")
    for broken_link in broken_links:
        print(f"- {broken_link}")
else:
    print("All internal links are working correctly.")