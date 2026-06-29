from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# List of Streamlit apps to wake up
STREAMLIT_URLS = [
    os.environ.get("STREAMLIT_APP_URL", "https://income-classification-ml.streamlit.app/"),
    #"",

]

def wake_up_app(driver, url):
    try:
        print(f"\nOpening: {url}")
        driver.get(url)
        
        wait = WebDriverWait(driver, 15)
        
        try:
            # Look for the wake-up button
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("Wake-up button found. Clicking...")
            button.click()
            
            # Wait for button to disappear
            wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")
            ))
            print("✅ App woke up successfully")
            
        except TimeoutException:
            # No button found = app is already awake
            print("✅ No wake-up button found. App is already awake.")
            
    except Exception as e:
        print(f"❌ Error waking up {url}: {e}")


def main():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for url in STREAMLIT_URLS:
            wake_up_app(driver, url)
    finally:
        driver.quit()
        print("\nScript finished.")


if __name__ == "__main__":
    main()

