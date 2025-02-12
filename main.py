from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select  # Import the Select class
from selenium.webdriver.support import expected_conditions as EC
import time

# def get_headless_driver():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     return webdriver.Chrome(options=options)


def get_headless_driver():

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    grid_url = "http://selenium-hub:4444/wd/hub"
    driver = webdriver.Remote(command_executor=grid_url, options=options)
    return driver


def test_homepage():
    driver = None
    try:
        driver = get_headless_driver()
        driver.get("https://useinsider.com/")
        assert "Insider" in driver.title
        print("TEST PASSED: Homepage loaded successfully")
    except Exception as e:
        print(f"TEST FAILED: Homepage - {e}")
    finally:
        driver.quit()


def test_careers_page():
    driver = None
    try:
        driver = get_headless_driver()
        driver.get("https://useinsider.com/")

        company_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Company"))
        )
        company_menu.click()

        careers_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Careers"))
        )
        careers_link.click()

        assert "careers" in driver.current_url
        assert driver.find_element(By.XPATH, "//h3[contains(text(), 'Our Locations')]").is_displayed()
        assert driver.find_element(By.XPATH, "//a[contains(text(), 'See all teams')]").is_displayed()
        assert driver.find_element(By.XPATH, "//h2[contains(text(), 'Life at Insider')]").is_displayed()

        print("TEST PASSED: Careers page loaded successfully with all sections visible")
    except Exception as e:
        print(f"TEST FAILED: Careers page - {e}")
    finally:
        driver.quit()




def test_qa_jobs_page():
    driver = None
    try:
        # Initialize the headless driver
        driver = get_headless_driver()
        driver.get("https://useinsider.com/careers/quality-assurance/")

        # Handle the cookie consent banner if it exists
        try:
            cookie_banner = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "cookie-law-info-bar"))
            )
            # Click the "Accept" button on the cookie banner
            accept_button = cookie_banner.find_element(By.XPATH, ".//a[contains(text(), 'Accept')]")
            accept_button.click()
            print("Cookie consent banner accepted")
        except:
            print("No cookie consent banner found or already dismissed")

        # Click "See all QA jobs" using the href attribute
        see_all_qa_jobs_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://useinsider.com/careers/open-positions/?department=qualityassurance']"))
        )
        see_all_qa_jobs_link.click()
        time.sleep(15)

        # Verify redirection to the correct page
        WebDriverWait(driver, 10).until(
            EC.url_contains("open-positions")
        )
        assert "qualityassurance" in driver.current_url, "Redirection to QA jobs page failed"

        # Add location filter
        try:
            # Wait for the location filter dropdown to be present
            location_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter-by-location"))
            )

            # Use Selenium's Select class to interact with the dropdown
            dropdown_element = driver.find_element(By.ID, "filter-by-location")
            select = Select(dropdown_element)

            # Select the second option (index 1, since it's 0-based)
            time.sleep(5)
            select.select_by_index(1)  # This selects the second option in the dropdown
            time.sleep(5)

            # Verify that the filter is applied
            selected_option = select.first_selected_option
            time.sleep(5)
            assert selected_option.text == "Istanbul, Turkiye", "Location filter not applied correctly"
            print("Location filter applied successfully")
        except Exception as e:
            print(f"Failed to apply location filter: {e}")

        # Click the "View Role" button after the filter is applied
        try:
            # Wait for the "View Role" button to be clickable
            view_role_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, 'btn-navy') and contains(text(), 'View Role')]"))
            )

            # Get the href attribute of the button
            view_role_url = view_role_button.get_attribute("href")
            print(f"View Role button URL: {view_role_url}")

            # Click the button
            view_role_button.click()
            print("View Role button clicked successfully")

            # Wait for the new tab to open and switch to it
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])

            # Verify the URL of the new tab
            WebDriverWait(driver, 10).until(EC.url_contains("jobs.lever.co"))
            assert "jobs.lever.co/useinsider" in driver.current_url, "View Role button did not open the correct URL"
            print("View Role button opened the correct URL")

        except Exception as e:
            print(f"Failed to click View Role button: {e}")

    finally:
        # Close all browser windows
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_homepage()
    test_careers_page()
    test_qa_jobs_page()
