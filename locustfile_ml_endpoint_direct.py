from locust import HttpUser, task, constant_pacing, LoadTestShape
import json

# -----------------------
# CONFIG
# -----------------------
MAX_USERS = 200
RAMP_UP_SECONDS = 100
HOLD_SECONDS = 120
RAMP_DOWN_SECONDS = 100
REQUEST_PACING = 1


# -----------------------
# Wave Load Shape
# -----------------------
class WaveLoadShape(LoadTestShape):
    def tick(self):
        run_time = self.get_run_time()

        if run_time < RAMP_UP_SECONDS:
            user_count = int(MAX_USERS * (run_time / RAMP_UP_SECONDS))
            return (user_count, 2)

        elif run_time < RAMP_UP_SECONDS + HOLD_SECONDS:
            return (MAX_USERS, 2)

        elif run_time < RAMP_UP_SECONDS + HOLD_SECONDS + RAMP_DOWN_SECONDS:
            time_in_ramp = run_time - (RAMP_UP_SECONDS + HOLD_SECONDS)
            progress = time_in_ramp / RAMP_DOWN_SECONDS
            user_count = int(MAX_USERS * (1 - progress))
            return (max(user_count, 0), 2)

        else:
            return None


# -----------------------
# User Class
# -----------------------
class CPDUser(HttpUser):

    wait_time = constant_pacing(REQUEST_PACING)

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

    def on_start(self):

        # Authentication
        login_payload = {
            "username": "cpadmin",
            "password": "4ovTInI8VzLvjv48SXrw3BO8FO1BkBgY"
        }
        login_headers = {
            "Content-Type": "application/json",
            "Cookie": "2ac1df5a53d05af1ed3c0e46006c8757=643363c7e1bc1cac53deb959486acfd7"
        }

        resp = self.client.post(
            "/icp4d-api/v1/authorize",
            data=json.dumps(login_payload),
            headers=login_headers,
            name="auth_login"
        )

        try:
            self.token = resp.json().get("token")
        except:
            self.token = ""

        self.prediction_headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        self.prediction_payload = {
            "input_data": [
                {
                    "fields": [
                        "customer_ID","D_63","D_64","D_66","D_68",
                        "B_30","B_38","D_114","D_116","D_117","D_120","D_126"
                    ],
                    "values": [
                        ["ameen","1","1",1,1,1,1,1,1,1,1,1]
                    ]
                }
            ]
        }

    @task(1)
    def xgb_01(self):
        self._call(0)

    @task(1)
    def xgb_02(self):
        self._call(1)

    @task(1)
    def xgb_03(self):
        self._call(2)

    @task(1)
    def xgb_04(self):
        self._call(3)

    @task(1)
    def xgb_05(self):
        self._call(4)

    @task(1)
    def xgb_06(self):
        self._call(5)

    @task(1)
    def xgb_07(self):
        self._call(6)

    @task(1)
    def xgb_08(self):
        self._call(7)

    @task(1)
    def xgb_09(self):
        self._call(8)

    @task(1)
    def xgb_10(self):
        self._call(9)

    # internal helper
    def _call(self, index):
        self.client.post(
            f"/{self.BASE_URLS[index]}",
            params={"version": "2021-05-01"},
            headers=self.prediction_headers,
            json=self.prediction_payload,
            name=f"xgb-{str(index+1).zfill(2)}"
        )
