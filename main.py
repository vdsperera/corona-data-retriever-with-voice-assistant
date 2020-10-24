import requests
import json
import pyttsx3
import speech_recognition as sr
import re

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

    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if(content['name'] == 'Coronavirus Cases:'):
                return content['value']

    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if(content['name'] == 'Deaths:'):
                return content['value']
        return '0'

    def get_country_data(self, country):
        data = self.data['country']
        for content in data:
            if(content['name'].lower() == country.lower()):
                return content
        return '0'


# print(data.data['country'])
# print(data.get_total_cases())
# print(data.get_total_deaths())
# print(data.get_country_data('sri Lanka'))

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
        except Exception as e:
            print("Exception : ", str(e))

    return said.lower()


# print(get_audio())

def main():
    print('Started')
    data = Data(API_KEY, PROJECT_TOKEN, RUN_TOKEN)

    PATTERNS = {
        re.compile('[\w\s] + total + [\w\s] + cases') : data.get_total_cases,
        re.compile('[\w\s] + total cases') : data.get_total_cases,
        re.compile('[\w\s] + total + [\w\s] + deaths') : data.get_total_deaths,
        re.compile('[\w\s] + total deaths') : data.get_total_deaths
    }
    # print(PATTERNS.items())
    while True:
        print('Listening')
        text = get_audio()
        result = None
        for pattern, func in PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if result:
            print(text)
            speak(text)

        if text.find('stop'):
            break
        print(text)

main()
