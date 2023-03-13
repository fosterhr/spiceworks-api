from flask import Flask, jsonify
from contextlib import contextmanager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from json import loads
from queue import Queue

# Create a Flask app instance
app = Flask(__name__)

# Define the credentials and URL for the Spiceworks API
BASE_URL = ""
USER_EMAIL = ""
USER_PASSWORD = ""

# Define the number of drivers in the driver pool
DRIVER_POOL_SIZE = 5
driver_manager = None

# Define a class for managing the driver pool
class DriverManager:
    def __init__(self, driver_pool_size):
        self.driver_pool_size = driver_pool_size
        self.driver_pool = Queue(maxsize=self.driver_pool_size)

        # Initialize the driver pool
        for _ in range(self.driver_pool_size):
            driver = self.init_driver()
            self.driver_pool.put(driver)

    # Define a method to initialize a new driver
    def init_driver(self):
        # Configure the ChromeOptions for the driver
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-crash-reporter")
        options.add_argument("--disable-oopr-debug-crash-dump")
        options.add_argument("--no-crash-upload")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-low-res-tiling")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("--headless")

        # Create a new Chrome driver with the configured options
        driver = Chrome(options=options)

        # Log in to the Spiceworks API using the user credentials
        driver.get("https://accounts.spiceworks.com/sign_in?policy=hosted_help_desk")
        driver.find_element(By.ID, "login[email]").send_keys(USER_EMAIL)
        driver.find_element(By.ID, "login[password]").send_keys(USER_PASSWORD)
        driver.find_element(By.NAME, "commit").click()

        # Return the initialized driver
        return driver

    # Define a method to get a driver from the driver pool
    def get_driver_from_pool(self):
        return self.driver_pool.get()

    # Define a method to return a driver to the driver pool
    def return_driver_to_pool(self, driver):
        self.driver_pool.put(driver)

    # Define a context manager to get a driver from the driver pool
    @contextmanager
    def get_driver(self):
        driver = self.get_driver_from_pool()
        yield driver
        self.return_driver_to_pool(driver)

# Define a function to get the ticket data from the Spiceworks API
def get_ticket_data():
    with driver_manager.get_driver() as driver:
        # Navigate to the ticket API URL and retrieve the response
        driver.get(f"https://{BASE_URL}/api/tickets")
        response = loads(driver.find_element(By.TAG_NAME, "pre").text)
    return response

# Define a function to get all the tickets from the Spiceworks API
def get_tickets():
    return get_ticket_data()["tickets"]

# Get the end user data from the get_ticket_data function
def get_end_users():
    return get_ticket_data()["end_users"]

# Get the admin user data using Selenium WebDriver and return the response
def get_admin_users():
    with driver_manager.get_driver() as driver:
        # Load the API endpoint for users
        driver.get(f"https://{BASE_URL}/api/users")
        # Extract the JSON response from the page
        response = loads(driver.find_element(By.TAG_NAME, "pre").text)
    return response

# Set up the API endpoint for tickets
@app.route('/tickets/')
def api_tickets():
    return jsonify(get_tickets())

# Set up the API endpoint for a specific ticket by ID
@app.route('/tickets/id/<id>/')
def api_tickets_id(id):
    tickets = get_tickets()
    response = {}
    for ticket in tickets:
        if ticket["id"] == int(id):
            response = ticket
            break
    return response

# Set up the API endpoint for all tickets created by a specific user
@app.route('/tickets/user/<user>/')
def api_tickets_user(user):
    ticket_data = get_ticket_data()
    tickets = ticket_data["tickets"]
    users = ticket_data["end_users"]

    # Check if user is passed as email or id and set filter accordingly
    try:
        user = int(user)
        filter = "id"
    except:
        filter = "email"

    # Find the user object in the list of end users
    for u in users:
        if u[filter] == user:
            user = u
            break

    response = []
    # Find all tickets created by the user
    for ticket in tickets:
        try:
            if ticket["creator"]["id"] == user["id"]:
                response.append(ticket)
        except:
            break
    return jsonify(response)

# Set up the API endpoint for all tickets with a specific status
@app.route('/tickets/status/<status>/')
def api_tickets_status(status):
    tickets = get_tickets()
    response = []
    # Find all tickets with the given status
    for ticket in tickets:
        if ticket["status"] == status:
            response.append(ticket)
    return jsonify(response)

# Set up the API endpoint for all end users
@app.route('/users/')
def api_users():
    return jsonify(get_end_users())

# Set up the API endpoint for a specific end user by ID or email
@app.route('/users/<user>/')
def api_users_user(user):
    all_users = get_end_users()

    response = {}
    # Check if user is passed as email or id and set filter accordingly
    try:
        user = int(user)
        filter = "id"
    except:
        filter = "email"

    # Find the user object in the list of end users
    for u in all_users:
        if u[filter] == user:
            response = u
            break
    return jsonify(response)

# Set up the API endpoint for all admin users
@app.route('/admin/users/')
def api_admin_users():
    return jsonify(get_admin_users())

# Set up the API endpoint for a specific admin user by ID or email
@app.route('/admin/users/<user>/')
def api_admin_users_user(user):
    all_users = get_admin_users()

    response = {}
    # Check if user is passed as email or id and set filter accordingly
    try:
        user = int(user)
        filter = "id"
    except:
        filter = "email"

    # Find the user object in the list of admin users
    for u in all_users["users"]:
        if u[filter] == user:
            response = u
            break
    return jsonify(response)

if __name__ == '__main__':
    # Initialize the driver manager object, and start the web app
    driver_manager = DriverManager(driver_pool_size=DRIVER_POOL_SIZE)
    app.run(port=80, debug=True)
