import requests
import json


API_KEY = "tTRi3gZfzPyh"
PROJECT_TOKEN = "tmpPtFoT03sJ"
RUN_TOKEN = "tnGdovJgMXau"

class Data:
    def __init__(self, api_key, project_token, run_token):
        self.api_key = api_key
        self.project_token = project_token
        self.run_token = run_token
        self.params = {
            'api_key':self.api_key
        }
        self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',self.params)
        self.data = json.loads(response.text)

