
# QA Test Automation with Selenium

This repository contains an automated test suite built with Selenium WebDriver to test various pages on a website using headless Chrome. The tests are run using a Selenium Grid with a Selenium Hub and Node setup. This README explains how the tests work, how to communicate with the Selenium Hub and Node, and how the GitHub Actions CI/CD pipeline works.

![image](https://github.com/user-attachments/assets/42cfd7cf-8afe-49fb-b5f4-723ee846bbec)


## 1. How the Test Case Code Works

The test case code uses the Selenium WebDriver to automate web interactions in headless mode. The core tests are written as functions that:

1. **Initialize the WebDriver** with specific options for headless mode.
2. **Navigate to the website** and verify elements, including page loads, buttons, and interactive features.
3. **Handle actions** such as clicking links, waiting for elements to load, applying filters, and interacting with dynamic content.

### `get_headless_driver()`

This function configures and returns a headless Chrome driver instance connected to a Selenium Hub. The driver is configured with several options:
- Headless mode (`--headless=new`) for better stability.
- Disable GPU and sandboxing to ensure compatibility with CI/CD environments.
- Prevent bot detection by disabling certain Chrome features.

```python
def get_headless_driver():
    options = Options()
    options.add_argument("--headless=new")  # Headless mode for stability
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection
    options.add_argument("--window-size=1920,1080")  # Ensure proper rendering

    grid_url = "http://selenium-hub:4444/wd/hub"  # Connect to Selenium Grid Hub
    driver = webdriver.Remote(command_executor=grid_url, options=options)
    return driver
```

### `test_homepage()`

This test navigates to the homepage of the website and verifies that the title contains "Insider". If successful, it prints a success message.

```python
def test_homepage():
    driver = None
    try:
        driver = get_headless_driver()
        driver.get("https://useinsider.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "Insider" in driver.title
        print("✅ TEST 1 PASSED: Homepage loaded successfully")
    except Exception as e:
        print(f"❌ TEST 1 FAILED: Homepage - {e}")
    finally:
        if driver:
            driver.quit()
```

### `test_careers_page()`

This test navigates to the "Careers" page, clicks through the "Company" menu, and verifies the presence of key elements.

```python
def test_careers_page():
    driver = None
    try:
        driver = get_headless_driver()
        driver.get("https://useinsider.com/")

        company_menu = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Company"))
        )
        company_menu.click()

        careers_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Careers"))
        )
        careers_link.click()

        WebDriverWait(driver, 10).until(EC.url_contains("careers"))
        assert "careers" in driver.current_url
        print("✅ TEST 2 PASSED: Careers page loaded successfully")
    except Exception as e:
        print(f"❌ TEST 2 FAILED: Careers page - {e}")
    finally:
        if driver:
            driver.quit()
```

### `test_qa_jobs_page()`

This test checks the "Quality Assurance" jobs page. It handles the cookie consent banner, clicks the "See all QA jobs" link, and applies filters like location. Additionally, it tests hovering over elements and opening URLs in new tabs.

```python
def test_qa_jobs_page(): #test_qa_jobs_page
    driver = None
    try:
        driver = get_headless_driver()
        driver.get("https://useinsider.com/careers/quality-assurance/")

        # Handle cookie consent banner if it exists
        try:
            accept_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Accept')]"))
            )
            accept_button.click()
            print("✅ TEST 3 PASSED:  Cookie consent accepted and QA Jobs Loaded successfully ")
        except Exception:
            print("❌ TEST 3  FAILED: No cookie banner found or already dismissed")

        # Click "See all QA jobs"
        see_all_qa_jobs_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='https://useinsider.com/careers/open-positions/?department=qualityassurance']")
            )
        )
        see_all_qa_jobs_link.click()

        # Verify redirection
        WebDriverWait(driver, 15).until(EC.url_contains("open-positions"))
        assert "qualityassurance" in driver.current_url, "❌ Redirection to QA jobs page failed"


        try: #test_apply_locatiom
            dropdown_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter-by-location"))
            )
            select = Select(dropdown_element)
            time.sleep(3)  # Allow dropdown options to load
            select.select_by_index(1)  # Select the second option
            time.sleep(2)

            selected_option = select.first_selected_option.text
            assert selected_option == "Istanbul, Turkiye", "❌ Location filter not applied correctly"
            print("✅ TEST 4 PASSED: Location filter applied successfully")
        except Exception as e:
            print(f"❌ TEST 4 FAILED: Failed to apply location filter: {e}")

        # Click "View Role" button

        try: #test_view_role
            # Locate the element to hover over (the parent container or the button itself)
            hover_element = driver.find_element(By.XPATH, '//*[@id="jobs-list"]/div[1]/div')

            # Use ActionChains to move the cursor to the element
            actions = ActionChains(driver)
            actions.move_to_element(hover_element).perform()
            print("✅ Cursor moved to the element")

            # Wait for the "View Role" button to be clickable
            view_role_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, 'btn-navy') and contains(text(), 'View Role')]")
                )
            )
            view_role_url = view_role_button.get_attribute("href")
            print(f"ℹ️ View Role button URL: {view_role_url}")

            # Open the URL in a new tab using JavaScript
            driver.execute_script(f"window.open('{view_role_url}', '_blank');")
            print("✅ Opened the View Role URL in a new tab")

            # Wait for new tab to open and switch to it
            WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])

            # Verify new tab URL
            WebDriverWait(driver, 15).until(EC.url_contains("jobs.lever.co"))
            assert "jobs.lever.co" in driver.current_url, "❌ View Role button did not open correct URL"
            print("✅ TEST 5 PASSED: View Role button opened the correct URL")

        except TimeoutException as e:
            print(f"❌ TEST 5 FAILED: Timeout while waiting for element or new tab: {e}")
        except NoSuchElementException as e:
            print(f"❌ TEST 5 FAILED: Element not found: {e}")
        except Exception as e:
            print(f"❌ TEST 5 FAILED: Unexpected error: {e}")

    finally:
        if driver:
            driver.quit()

```

## 2. Communicating with Selenium Hub and Node

The Selenium Grid consists of two key components:
- **Selenium Hub**: The central server that manages all WebDriver requests.
- **Selenium Nodes**: The machines (or containers) that execute the tests on specific browsers.

In the test code, the `webdriver.Remote()` method is used to communicate with the Selenium Hub:
```python
driver = webdriver.Remote(command_executor="http://selenium-hub:4444/wd/hub", options=options)
```
The Selenium Hub routes the test request to an available node (e.g., a Chrome Node) to execute the test in the desired environment.

Ensure the Selenium Hub and Node are properly set up and running in your environment. For Kubernetes, you can define the Hub and Node as separate containers and configure the network properly.

## 3. How the GitHub Actions CI/CD Pipeline Works

### Build-and-Push-ECR Job

1. **Checkout code**: This step fetches the latest code from the repository.
2. **Configure AWS credentials**: The AWS credentials are configured to allow access to Amazon ECR.
3. **Login to Amazon ECR**: Logs into the Amazon Elastic Container Registry (ECR) to push images.
4. **Build, tag, and push Docker images**: Builds Docker images for the application, Selenium Hub, and Selenium Node, then pushes them to the ECR.

```yaml
docker build -t $AWS_REPOSITORY:$APP_TAG -f Dockerfileapp .
docker push $AWS_REPOSITORY:$APP_TAG
```

### Deploy-EKS Job

1. **Install AWS CLI**: Installs the AWS CLI to interact with AWS services.
2. **Update kube config**: Updates the Kubernetes configuration to use the EKS cluster.
3. **Deploy to EKS**: Deploys the Docker images to the EKS cluster using `kubectl apply`.

```yaml
kubectl create namespace automation --dry-run=client -o yaml | kubectl apply -f -
```




This deploys the Docker images (Application, Hub, and Node) to the EKS cluster, ensuring that the containers run on the appropriate nodes.

## Conclusion

This setup allows you to automate web tests with Selenium, deploy and run tests in Kubernetes using a Selenium Grid, and manage the entire process with GitHub Actions.
