import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# Configure logging
logging.basicConfig(filename='execution_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log messages
logging.info("Execution started.")

# Launch the browser
driver = webdriver.Chrome()

try:
    # Opening URL - http://www.google.com
    driver.get("http://www.google.com")
    logging.info("Google website opened successfully.")

    # Entering the keyword "amazon" in the search bar
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("amazon")
    search_box.send_keys(Keys.RETURN)
    logging.info("Search keyword 'amazon' entered and submitted.")

    # Waiting for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))
    logging.info("Search results loaded successfully.")

    # Clicking on the link which takes you to the amazon login page
    amazon_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Amazon")
    amazon_link.click()
    logging.info("Clicked on the Amazon link.")

    # Waiting for the page to load
    WebDriverWait(driver, 10).until(EC.title_contains("Amazon"))
    logging.info("Amazon website loaded successfully.")

    # Clicking on "Sign in" link
    sign_in_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='nav-signin-tooltip']//span[@class='nav-action-inner'][normalize-space()='Sign in']")))
    sign_in_link.click()
    logging.info("Clicked on the 'Sign in' link.")

    # Login to https://www.amazon.in/ (you need to fill in your login details)

    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_email")))
    email_input.send_keys("bineet.singh0077@outlook.com")
    logging.info("Entered email.")

    # Clicking on the "Continue" button
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()
    logging.info("Clicked on the 'Continue' button.")

    # Handlining password input element
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ap_password")))
    password_input.send_keys("Bineet1992")
    logging.info("Entered password.")

    login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "signInSubmit")))
    login_button.click()
    logging.info("Clicked on the 'Login' button.")

    # Clicking on all buttons on search & select Electronics
    electronics_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Electronics")
    electronics_button.click()
    logging.info("Clicked on 'Electronics'.")

    # Searching for dell computers
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.clear()
    search_box.send_keys("dell computers")
    search_box.send_keys(Keys.RETURN)
    logging.info("Searched for 'dell computers'.")

    # Waiting for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-result-item")))
    logging.info("Search results for 'dell computers' loaded successfully.")

    # Applying the filter of range Rs 30000 to 50000
    filter_button = driver.find_element(By.ID, "p_n_price_range")
    filter_button.click()
    price_range_filter = driver.find_element(By.XPATH, "//a[contains(text(),'₹30,000 - ₹50,000')]")
    price_range_filter.click()
    logging.info("Applied price range filter.")

    # Validating all the products on the first 2 pages are shown in the range of Rs 30000 to 50000
    products = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item")
    for product in products:
        price_element = product.find_element(By.CSS_SELECTOR, "span.a-price")
        price = price_element.text
        price = price.replace('₹', '').replace(',', '')
        price = float(price)
        if not (30000 <= price <= 50000):
            logging.error("Price out of range: %s", price)

    # Printing all the products on the first 2 pages whose rating is 5 out of 5
    for product in products:
        rating_element = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt")
        rating = rating_element.get_attribute("innerHTML")
        if rating == "5 out of 5 stars":
            logging.info("Product with 5-star rating found: %s", product.text)

    # Add the first product whose rating is 5 out of 5 to the wish list. (Create a new wish list)
    wishlist_button = driver.find_element(By.ID, "add-to-wishlist-button-submit")
    wishlist_button.click()
    logging.info("Clicked on 'Add to Wishlist'.")

    # Validating the product is added to the wish list
    wishlist_link = driver.find_element(By.ID, "WLHUC_viewlist")
    wishlist_link.click()
    wishlist_items = driver.find_elements(By.CLASS_NAME, "a-link-normal")
    wishlist_items_text = [item.text for item in wishlist_items]
    if "Dell Computer" in wishlist_items_text:
        logging.info("Product successfully added to wishlist")
    else:
        logging.error("Product not added to wishlist")

finally:
    # Closing the browser
    driver.quit()
    logging.info("Browser closed.")
