import warnings
warnings.filterwarnings("ignore", category=Warning)



import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
# from selenium import webdriver_manager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import datetime

# options = Options()
# options.add_experimental_option('detach', True)

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# driver.get('https://registration.wm.edu/')


# Function to send Telegram message
def send_telegram_message(message):
    bot_token = 'Input_your_bot_token'
    chat_id = 'Input_your_chat_id'
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
    
    response = requests.get(send_text)
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print(f"Failed to send notification: {response.text}")



# Function to check seat availability
def check_seat_availability():
    print(f"{datetime.datetime.now()}: Checking seat availability...")
    url = "https://registration.wm.edu/"
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up the WebDriver (make sure to have the correct path to chromedriver)
    # service = Service('/usr/local/bin/chromedriver')  # Change this to the path of your chromedriver
    # driver = webdriver.Chrome(service=service, opt    ions=chrome_options)
    options = Options()
    options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    
    try:
        driver.get(url)
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Perform interactions
        # Click on the search bar
        search_box = wait.until(EC.element_to_be_clickable((By.ID, 'crit-keyword')))  
        search_box.click()

        # Type 'LING 280' into the search bar
        search_box.send_keys('LING 280') # Example of a class

        # Click on the dropdown menu
        dropdown_element = wait.until(EC.element_to_be_clickable((By.ID, 'crit-srcdb')))
        dropdown_element.click()

        # Click on the "Summer 2024" option, adjust date if needed
        summer_2024_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[text()="Summer 2024"]')))
        summer_2024_option.click()

        # Click on the search button
        search_button = wait.until(EC.element_to_be_clickable((By.ID, 'search-button')))
        search_button.click()

        # Click on the only box that appears
        box_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'result__link')))
        box_element.click()

        # Find the seats available element
        seats_avail_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'seats_avail')))

        seats_available = seats_avail_element.text.strip()
        print(f"{datetime.datetime.now()}: Seats Available: {seats_available}")
    
        if seats_available != "0":
            send_telegram_message(seats_available)
    
    except Exception as e:
        print(f"{datetime.datetime.now()}: An error occurred: {e}")
    
    finally:
        driver.quit()

# Schedule the job to run every 5 minutes
schedule.every(5).minutes.do(check_seat_availability)

# Run the scheduler for 144 hours (6 days)
end_time = time.time() + 144 * 3600
while time.time() < end_time:
    schedule.run_pending()
    print(f"{datetime.datetime.now()}: Scheduler is running...")
    time.sleep(1)

print("Finished scheduling.")
