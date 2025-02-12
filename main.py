from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import time


def get_remote_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    grid_url = "http://selenium-hub:4444/wd/hub"


    driver = webdriver.Remote(command_executor=grid_url, options=options)
    return driver


def test_homepage():
    try:
        driver = get_remote_driver()
        driver.get("https://useinsider.com/")
        assert "Insider" in driver.title
        print("Homepage loaded successfully")
    except Exception as e:
        print(f"Homepage - {e}")
    finally:
        driver.quit()


def test_careers_page():
    try:
        driver = get_remote_driver()
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

        print("Careers page loaded successfully with all sections visible")
    except Exception as e:
        print(f"Careers page - {e}")
    finally:
        driver.quit()


def test_qa_jobs_page():
    try:
        driver = get_remote_driver()
        driver.get("https://useinsider.com/careers/quality-assurance/")

        try:
            cookie_banner = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cookie-law-info-bar"))
            )
            accept_button = cookie_banner.find_element(By.XPATH, ".//a[contains(text(), 'Accept')]")
            accept_button.click()
            print("Cookie consent banner accepted")


            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "cookie-law-info-bar"))
            )
        except:
            print("No cookie consent banner found or already dismissed")


        see_all_qa_jobs_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://useinsider.com/careers/open-positions/?department=qualityassurance']"))
        )


        driver.execute_script("arguments[0].scrollIntoView(true);", see_all_qa_jobs_link)
        driver.execute_script("arguments[0].click();", see_all_qa_jobs_link)


        WebDriverWait(driver, 20).until(
            EC.url_contains("open-positions")
        )
        assert "qualityassurance" in driver.current_url, "Redirection to QA jobs page failed"


    finally:
        driver.quit()

if __name__ == "__main__":
    test_homepage()
    test_careers_page()
    test_qa_jobs_page()