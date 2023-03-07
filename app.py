from flask import Flask, jsonify
from contextlib import contextmanager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from json import loads
from queue import Queue

# Create a Flask app instance
app = Flask(__name__)

# Define constants for Spiceworks login credentials and API URL
BASE_URL = ""
USER_EMAIL = ""
USER_PASSWORD = ""

# Define the maximum number of Chrome drivers in the pool and create a queue for them
DRIVER_POOL_SIZE = 5
driver_pool = Queue(maxsize=DRIVER_POOL_SIZE)

# Define a function to initialize a Chrome driver with the Spiceworks login credentials
def init_driver():
    # Set Chrome options to run in headless mode without GPU acceleration
    options = ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    # Create a new Chrome driver with the specified options
    driver = Chrome(options=options)
    # Log in to the Spiceworks helpdesk using the login credentials
    driver.get("https://accounts.spiceworks.com/sign_in?policy=hosted_help_desk")
    driver.find_element(By.ID, "login[email]").send_keys(USER_EMAIL)
    driver.find_element(By.ID, "login[password]").send_keys(USER_PASSWORD)
    driver.find_element(By.NAME, "commit").click()
    # Return the initialized Chrome driver
    return driver

# Define a function to create a pool of Chrome drivers
def create_driver_pool():
    # Create DRIVER_POOL_SIZE number of Chrome drivers and add them to the driver pool
    for _ in range(DRIVER_POOL_SIZE):
        driver = init_driver()
        driver_pool.put(driver)

# Define a function to get a Chrome driver from the driver pool
def get_driver_from_pool():
    return driver_pool.get()

# Define a function to return a Chrome driver to the driver pool
def return_driver_to_pool(driver):
    driver_pool.put(driver)

# Define a context manager to get a Chrome driver from the driver pool
@contextmanager
def get_driver():
    driver = get_driver_from_pool()
    yield driver
    return_driver_to_pool(driver)

# Define a function to get all helpdesk tickets using a Chrome driver
def get_tickets():
    with get_driver() as driver:
        driver.get(f"https://{BASE_URL}/api/tickets")
        response = loads(driver.find_element(By.TAG_NAME, "pre").text)["tickets"]
    return response

# Define a function to get all helpdesk users using a Chrome driver
def get_users():
    with get_driver() as driver:
        driver.get(f"https://{BASE_URL}/api/users")
        response = loads(driver.find_element(By.TAG_NAME, "pre").text)
    return response

# Define a Flask route for getting all helpdesk tickets
@app.route('/api/tickets/')
def api_tickets():
    return jsonify(get_tickets())

# Define a Flask route for getting helpdesk tickets filtered by status
@app.route('/api/tickets/<status>/')
def api_tickets_status(status):
    # Get all helpdesk tickets
    tickets = get_tickets()
    # Filter the tickets by the given status
    open_tickets = []
    for ticket in tickets:
        if ticket["status"] == status:
            open_tickets.append(ticket)
    # Return the filtered tickets
    return open_tickets

# Define a Flask route for getting all helpdesk users
@app.route('/api/users/')
def api_users():
    return jsonify(get_users())

# Start the Flask app and create the driver pool
if __name__ == '__main__':
    create_driver_pool()
    app.run(port=80)
