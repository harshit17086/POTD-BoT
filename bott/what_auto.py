import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def send_problem():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,  # Adjust your MySQL port if necessary
            user='root',  # Replace with your MySQL username
            password='',  # Replace with your MySQL password
            database='coding_problems'
        )
        cursor = conn.cursor()

        # Fetch a problem
        cursor.execute('SELECT problem, link FROM problems ORDER BY RAND() LIMIT 1')
        problem = cursor.fetchone()
        conn.close()

        if problem is None:
            print("No problems found in the database.")
            return

        problem_text = f"Problem of the day: {problem[1]}"

        # Automatically download and set up the correct chromedriver version
        service = ChromeService(executable_path=ChromeDriverManager().install())

        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:/Users/harsh/AppData/Local/Google/Chrome/User Data/Default")
        options.add_argument("profile-directory=Default")

        # Initialize the WebDriver with options
        driver = webdriver.Chrome(service=service, options=options)

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com/")
        
        # Wait for WhatsApp Web to load
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        
        # Check if logged in
        if "Click to reload QR code" in driver.page_source:
            print("Please log in to WhatsApp Web and scan the QR code.")
            driver.quit()
            return
        else:
            print("Logged in to WhatsApp Web successfully.")

        # Find the chat you want to send the message to
        contact_name = "Agnihot"
        search_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.click()
        search_box.send_keys(contact_name + Keys.ENTER)
        time.sleep(2)  # Wait for search results to appear

        # Select the contact
        try:
            contact = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]')))
            contact.click()
            print(f"Selected chat: {contact_name}")
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error selecting chat: {e}")
            # Handle the exception (e.g., refresh or retry)

        # Wait for the message box to be visible
        message_box = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="6"]')))
        message_box.click()
        message_box.send_keys(problem_text)
        message_box.send_keys(Keys.ENTER)
        print(f"Sent message: {problem_text}")

        # Keep the browser open for a specific amount of time to ensure the message is sent
        time.sleep(60)

        # Close the browser1
        driver.quit()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function to send the message immediately
send_problem()
