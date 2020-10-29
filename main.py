import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

# parsehub info
API_KEY = "tTRi3gZfzPyh"
PROJECT_TOKEN = "tmpPtFoT03sJ"
RUN_TOKEN = "tnGdovJgMXau"


class Data:
    def __init__(self, api_key, project_token, run_token):
        self.api_key = api_key
        self.project_token = project_token
        self.run_token = run_token
        self.params = {
            'api_key': self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        total_data = self.data['total']
        for item in total_data:
            if(item['name'] == 'Coronavirus Cases:'):
                return item['value']

    def get_total_deaths(self):
        total_data = self.data['total']
        for item in total_data:
            if(item['name'] == 'Deaths:'):
                return item['value']
        return '0'

    def get_country_data(self, country):
        countries_data = self.data['country']
        for item in countries_data:
            if(item['name'].lower() == country.lower()):
                return item
        return '0'

    def get_country_list(self):
        countries_data = self.data['country']
        country_list = []
        for item in countries_data:
            country_list.append(item['name'].lower())
        return country_list

    def update_data(self):
        response = requests.get(f"""
        https://www.parsehub.com/api/v2/projects/
        {self.project_token}/run
        """, self.params)

        def poll():

            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print('Data updated')
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():

    recognizer = sr.Recognizer()
    said = ''
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            said = recognizer.recognize_google(audio)
            print('recognised voice: ' + said)
        except Exception as e:
            print("Exception : ", str(e))
    return said.lower()


# print(get_audio())

def main():

    print('Started')
    data = Data(API_KEY, PROJECT_TOKEN, RUN_TOKEN)

    PATTERNS = {
        re.compile(r'[\w\s]+ total+ [\w\s]+ cases'): data.get_total_cases,
        re.compile(r'[\w\s]+ total cases'): data.get_total_cases,
        re.compile(r'[\w\s]+ total+ [\w\s]+ deaths'): data.get_total_deaths,
        re.compile(r'[\w\s]+ total deaths'): data.get_total_deaths
    }

    COUNTRY_PATTERNS = {
        re.compile(r'[\w\s]+ cases+ [\w\s]'):
        lambda country: data.get_country_data(country)['total_cases'],
        re.compile(r'[\w\s]+ deaths+ [\w\s]'):
        lambda country: data.get_country_data(country)['total_deaths']
    }

    # print(PATTERNS.items())
    while True:
        print('Listening')
        text = input()
        result = None
        country_list = data.get_country_list()

        # check for country specific data
        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break
                # print(text)
                break

        # check for general data
        for pattern, func in PATTERNS.items():
            if pattern.match(text):
                result = func()
                print(text)
                break

        if text == 'update':
            result = "Data is being updated and this may take a moment"
            data.update_data()

        if text.find('stop') != -1:
            break

        if result:
            # print('pattern ' + text)
            print('Answer: ' + result)
            speak(result)


main()
