from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    grades = []
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Set up WebDriver options
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')  # Run in headless mode
        service = Service("/path/to/geckodriver")  # Replace with the actual path to geckodriver

        # Initialize WebDriver
        driver = webdriver.Firefox(service=service, options=options)

        try:
            driver.get("https://parents.edison.k12.nj.us/")

            # Log in
            username_field = driver.find_element(By.ID, "j_username")
            password_field = driver.find_element(By.ID, "passwordField")

            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            # Wait for and navigate to the gradebook
            menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.menu-selector"))
            )
            menu_button.click()

            gradebook_tab = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'gradebook')]"))
            )
            gradebook_tab.click()

            time.sleep(3)  # Wait for the page to load

            # Scrape grades
            grade_elements = driver.find_elements(By.CLASS_NAME, "twoColGridItem")
            grades = [grade.text for grade in grade_elements]

        finally:
            driver.quit()

    return render_template("index.html", grades=grades)

if __name__ == "__main__":
    app.run(debug=True)
