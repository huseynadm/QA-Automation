# Selenium Automation Testing on Kubernetes

## Overview
This project automates UI testing using Selenium WebDriver in a Kubernetes environment. It executes tests on a Selenium Grid, utilizing a Selenium Hub and Selenium Chrome Pod.

## Features
- Headless browser testing using Chrome
- Automated UI verification for [Insider](https://useinsider.com/)
- Tests include:
  - Homepage loading verification
  - Navigation to Careers page and element validation
  - QA jobs page redirection and cookie banner handling
- Executes on Kubernetes with Selenium Hub and Selenium Chrome Pod

## Prerequisites
Ensure you have the following installed and configured:
- Kubernetes cluster
- Selenium Hub and Selenium Chrome Pod deployed on Kubernetes
- Python 3.x
- Required Python dependencies (see `requirements.txt`)

## Setup
1. Clone the repository from GitLab:
   ```sh
   `git clone <your-repository-url>`
   `cd <your-repository-folder>`
   ```
2. Install dependencies:
   ```sh
   `pip install -r requirements.txt`
   ```

## Running Tests
Execute the tests using the following command:
```sh
`python test_script.py`
```

## Kubernetes Deployment
1. Deploy Selenium Grid components:
   ```sh
   `kubectl apply -f Deployment-hub.yaml`
   `kubectl apply -f Deployment-nodechrome.yaml`
   ```
2. Verify Pods are running:
   ```sh
   `kubectl get pods`
   ```
3. Execute the test script within a Kubernetes Deployment:
   ```sh
   `kubectl apply -f Deployment-app.yaml`
   ```

## Test Cases
### 1. Homepage Test
- Navigates to the homepage and verifies the title contains "Insider".

### 2. Careers Page Test
- Clicks on "Company" -> "Careers" and validates important page elements.

### 3. QA Jobs Page and Filter by Location Test
- Handles the cookie banner (if present) and verifies redirection to QA job listings.

## Logs and Debugging
View test execution logs:
```sh
`kubectl logs <test-pod-name>`
```


## Contributing
Feel free to submit issues or contribute to this project by forking the repository and submitting a merge request.

## License
This project is licensed under the MIT License.

