import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ID_CARD = os.environ.get("ID_CARD")
DRIVING_LICENSE = os.environ.get("DRIVING_LICENSE")
E_USLUGI_MVR_URL = os.environ.get("E_USLUGI_MVR")

def extract_section_content(html: str) -> str:
    """
    Extracts content from <div class="section-title"> up to (but not including) <div class="button-bar ...>.
    Returns the extracted HTML as a string, or an empty string if not found.
    """
    pattern = r'(<div class="section-title">.*?)(<div class="button-bar[\s\S]*?$)'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def get_road_fines():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  # Ensures full rendering in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        print("Checking for road fines...")
        driver.get(E_USLUGI_MVR_URL)

        # Handle cookie consent if present
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                lambda d: d.find_element(By.XPATH, '//aside[@id="cookieInfo"]//button')
            )
            cookie_btn.click()
        except Exception:
            pass  # Ignore if not present

        driver.find_element(By.ID, "obligedPersonIdent").send_keys(ID_CARD)
        driver.find_element(By.ID, "drivingLicenceNumber").send_keys(DRIVING_LICENSE)
        driver.find_element(By.XPATH, '//*[@id="ARTICLE-CONTENT"]/div/div[2]/div[1]/button').click()

        # Wait for the result to appear
        WebDriverWait(driver, 20).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="ARTICLE-CONTENT"]/div/div[2]/h2').text.strip() != ""
        )

        search_result_element = driver.find_element(By.ID, "ARTICLE-CONTENT")
        print("Road fines check fetched")
        raw = search_result_element.get_attribute("outerHTML")  # Return raw HTML for reliability
        return extract_section_content(raw)

    except Exception as ex:
        print(ex)
        return None
    finally:
        driver.quit()