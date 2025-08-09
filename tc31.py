from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

driver = webdriver.Chrome()

base_url = "https://codingcollective.com/"
driver.get(base_url)

all_links = driver.find_elements(By.TAG_NAME, "a")

broken_external_links = []
valid_external_links = []

print(f"Total links found: {len(all_links)}")

for link in all_links:
    href = link.get_attribute("href")

    if href and not href.startswith(base_url) and href.startswith("http"):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.head(href, headers=headers, timeout=10) # timeout 10 detik

            if response.status_code >= 400:
                print(f"Broken External Link (Status {response.status_code}): {href}")
                broken_external_links.append(href)
            else:
                valid_external_links.append(href)
        except requests.exceptions.RequestException as e:
            print(f"Error checking link {href}: {e}")
            broken_external_links.append(href)

driver.quit()

print("\nTest Results")
print(f"Valid external links found: {len(valid_external_links)}")
print(f"Broken external links found: {len(broken_external_links)}")

if broken_external_links:
    print("\nList of broken external links:")
    for broken_link in broken_external_links:
        print(f"- {broken_link}")
else:
    print("\nAll external links are working correctly.")