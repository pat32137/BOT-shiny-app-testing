import time
from locust import User, task, between, events, LoadTestShape
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

# -----------------------
# CONFIG
# -----------------------
MAX_USERS = 200
RAMP_UP_SECONDS = 30
RAMP_DOWN_SECONDS = 30

# Base domain
BASE_DOMAIN = "https://cpd-cpd.apps.690ea4442e6041d6a4c81788.cloud.techzone.ibm.com/"

# List of endpoint paths
BASE_URLS = [
    "ml/v4/deployments/shinyapp01/r_shiny?version=2021-05-01",
    "ml/v4/deployments/web_app_02/r_shiny?version=2021-05-01",
    "ml/v4/deployments/web_app_03/r_shiny?version=2021-05-01",
    "ml/v4/deployments/339a9b52-0eba-422a-b280-c87b9cc89045/r_shiny?version=2021-05-01",
    "ml/v4/deployments/a31aa9bc-8d35-42a3-9d6a-20bedf8909b8/r_shiny?version=2021-05-01",
    "ml/v4/deployments/ea17ea35-6e1d-4381-8b10-7cb2bd099a52/r_shiny?version=2021-05-01",
    "ml/v4/deployments/efbdf1b5-a044-4c69-ad1d-ec461bacbc20/r_shiny?version=2021-05-01",
    "ml/v4/deployments/d8c4c363-febb-41d0-8840-c415d33691c5/r_shiny?version=2021-05-01",
    "ml/v4/deployments/351715bc-b1e3-4a02-a87c-d830cf8ca6e8/r_shiny?version=2021-05-01",
    "ml/v4/deployments/1a984df3-0f63-451f-bc4f-83a3af5b5d11/r_shiny?version=2021-05-01"
]


# -----------------------
# Wave Load Shape
# -----------------------
class WaveLoadShape(LoadTestShape):
    """
    Wave-shaped load pattern: ramp up to MAX_USERS, then ramp down
    Total duration: RAMP_UP_SECONDS + RAMP_DOWN_SECONDS
    """

    def tick(self):
        run_time = self.get_run_time()

        # Ramp up phase
        if run_time < RAMP_UP_SECONDS:
            user_count = int(MAX_USERS * (run_time / RAMP_UP_SECONDS))
            return (user_count, 10)

        # Ramp down phase
        elif run_time < RAMP_UP_SECONDS + RAMP_DOWN_SECONDS:
            time_in_ramp = run_time - RAMP_UP_SECONDS
            progress = time_in_ramp / RAMP_DOWN_SECONDS
            user_count = int(MAX_USERS * (1 - progress))
            return (max(user_count, 0), 10)

        # End test
        else:
            return None


# -----------------------
# Selenium User Class
# -----------------------
class SeleniumUser(User):
    # wait_time = between(1, 2)

    def __init__(self, environment):
        super().__init__(environment)
        self.driver = None

    def on_start(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--window-size=1920,1080')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(60)

    def on_stop(self):
        """Clean up Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    # -------------------------------------------------------
    # 10 Equal Weight Tasks (endpoint-01 ... endpoint-10)
    # -------------------------------------------------------
    @task(1)
    def endpoint_01(self):
        self._wait_for_success(0)

    @task(1)
    def endpoint_02(self):
        self._wait_for_success(1)

    @task(1)
    def endpoint_03(self):
        self._wait_for_success(2)

    @task(1)
    def endpoint_04(self):
        self._wait_for_success(3)

    @task(1)
    def endpoint_05(self):
        self._wait_for_success(4)

    @task(1)
    def endpoint_06(self):
        self._wait_for_success(5)

    @task(1)
    def endpoint_07(self):
        self._wait_for_success(6)

    @task(1)
    def endpoint_08(self):
        self._wait_for_success(7)

    @task(1)
    def endpoint_09(self):
        self._wait_for_success(8)

    @task(1)
    def endpoint_10(self):
        self._wait_for_success(9)

    # Internal helper method
    def _wait_for_success(self, index):
        """
        Navigate to endpoint and wait for SUCCESS badge
        """
        url = BASE_DOMAIN + BASE_URLS[index]
        start = time.time()

        # Extract deployment ID or name for cleaner naming
        deployment_id = BASE_URLS[index].split('/')[3].split('?')[0]
        req_name = f"app-{str(index + 1).zfill(2)} ({deployment_id})"

        try:
            # Navigate to the page
            self.driver.get(url)

            # Wait for the SUCCESS badge to appear
            wait = WebDriverWait(self.driver, 45)
            element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class, 'status-badge') and contains(@class, 'success') and contains(text(), 'SUCCESS')]")
                )
            )

            duration = (time.time() - start) * 1000
            events.request.fire(
                request_type="SELENIUM",
                name=req_name,
                response_time=duration,
                response_length=0,
                exception=None,
            )

        except (TimeoutException, WebDriverException) as e:
            duration = (time.time() - start) * 1000
            events.request.fire(
                request_type="SELENIUM",
                name=req_name,
                response_time=duration,
                response_length=0,
                exception=e,
            )

# To run this test, use the command:
# locust -f your_script.py --headless -u 200 --host https://cpd-cpd.apps.itz-vftoyf.pok-lb.techzone.ibm.com