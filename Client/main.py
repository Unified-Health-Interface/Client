import json
import os
import pathlib

import AppKit
import pyttsx3
import requests
import speech_recognition as sr
from dotenv import load_dotenv
from notify_run import Notify
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

load_dotenv()

API_SERVER_URL = os.getenv('API_SERVER_URL')
RASA_SERVER_URL = os.getenv('RASA_SERVER_URL')
RASA_ACTIONS_SERVER_URL = os.getenv('RASA_ACTIONS_SERVER_URL')
CONFIG_FILE = os.path.join(pathlib.Path.home(), '.config', 'uhi.json')

BANNER = \
    """[cyan]








                                      $$ $$$$$ $$
                                      $$ $$$$$ $$
                                     .$$ $$$$$ $$.
                                     :$$ $$$$$ $$:
                                     $$$ $$$$$ $$$
                                     $$$ $$$$$ $$$
                                    ,$$$ $$$$$ $$$.
                                   ,$$$$ $$$$$ $$$$.
                                  ,$$$$; $$$$$ :$$$$.
                                 ,$$$$$  $$$$$  $$$$$.
                               ,$$$$$$'  $$$$$  `$$$$$$.
                             ,$$$$$$$'   $$$$$   `$$$$$$$.
                          ,s$$$$$$$'     $$$$$     `$$$$$$$s.
                        $$$$$$$$$'       $$$$$       `$$$$$$$$$
                        $$$$$Y'          $$$$$          `Y$$$$$


    """

r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')

notify = Notify()

console = Console()

os.system('clear')
console.print(BANNER)

engine.say("Welcome to Unified Healthcare Interface. Your virtual assistant is currently booting up.")
engine.runAndWait()


def generate_test_data(username):
    requests.post(f"{API_SERVER_URL}/allergy/", json={
        'allergy': 'peanuts',
        'username': username
    })

    requests.post(f"{API_SERVER_URL}/allergy/", json={
        'allergy': 'milk',
        'username': username
    })

    requests.post(f"{API_SERVER_URL}/allergy/", json={
        'allergy': 'pollen',
        'username': username
    })

    # Vaccinations

    requests.post(f"{API_SERVER_URL}/vaccination/", json={
        'vaccine': 'influenza',
        'date_time': '2023-02-04 17:45:00',
        'done': False,
        'username': username,
    })

    requests.post(f"{API_SERVER_URL}/vaccination/", json={
        'vaccine': 'DDT',
        'date_time': '2023-03-07 11:30:00',
        'done': False,
        'username': username,
    })

    # Appointments

    requests.post(f"{API_SERVER_URL}/appointment/", json={
        'doctor': 'Dr Manas',
        'hospital': 'Manipal Hospital',
        'date_time': '2023-02-04 14:00:00',
        'username': username,
    })

    requests.post(f"{API_SERVER_URL}/appointment/", json={
        'doctor': 'Dr Govind',
        'hospital': 'Chinmaya Mission Hospital',
        'date_time': '2023-02-04 21:15:00',
        'username': username,
    })

    # Doctors Notes

    requests.post(f"{API_SERVER_URL}/doctor-note/", json={
        'doctor': 'Dr Varun',
        'note': 'Your lungs are responding well to the treatment. However, you need to stay away from highly polluted areas.',
        'username': username,
    })

    requests.post(f"{API_SERVER_URL}/doctor-note/", json={
        'doctor': 'Dr Sanjay',
        'note': 'The fracture you suffered 2 months ago is almost fully healed, and you are safe to return to your everyday activities.',
        'username': username,
    })

    # Prescriptions

    requests.post(f"{API_SERVER_URL}/prescription/", json={
        'doctor': 'Dr Nikhil',
        'medicines': 'Crocin',
        'date_time': '2023-01-23 08:30:00',
        'done': False,
        'username': username,
    })

    requests.post(f"{API_SERVER_URL}/prescription/", json={
        'doctor': 'Dr Ishaan',
        'medicines': 'Paracetamol',
        'date_time': '2023-01-29 21:00:00',
        'done': False,
        'username': username,
    })

    # Bills

    requests.post(f"{API_SERVER_URL}/bill/", json={
        'hospital': 'Manipal Hospital',
        'service': 'ICU',
        'amount': 50000,
        'due_date': '2023-02-11',
        'paid': False,
        'username': username,
    })

    requests.post(f"{API_SERVER_URL}/bill/", json={
        'hospital': 'Chinmaya Mission Hospital',
        'service': 'lung disease treatment',
        'amount': 25000,
        'due_date': '2023-02-19',
        'paid': False,
        'username': username,
    })


def setup_new_user():
    engine.say("Welcome, new user! I will guide you through the setup process.")
    engine.runAndWait()

    engine.say("Enter your full name.")
    engine.runAndWait()
    full_name = Prompt.ask("[cyan]Enter your full name")

    os.system('clear')
    console.print(BANNER)

    username = ''.join(full_name.split(' ')).lower()

    requests.post(f"{API_SERVER_URL}/user/", json={
        'username': username,
        'full_name': full_name
    })

    engine.say(f"Successfully registered. Welcome, {full_name}!")
    engine.runAndWait()

    counter = 1

    while True:
        os.system('clear')
        console.print(BANNER)

        engine.say(f"Enter emergency contact name number {counter}. Press enter to exit.")
        engine.runAndWait()
        name = Prompt.ask(f"[cyan]Enter emergency contact name number {counter}. Press enter to exit")

        if name == '':
            break

        os.system('clear')
        console.print(BANNER)

        engine.say(f"Enter the email address of {name}.")
        engine.runAndWait()
        email = Prompt.ask(f"[cyan]Enter the email address of {name}")

        os.system('clear')
        console.print(BANNER)

        engine.say(f"Enter the phone number of {name}.")
        engine.runAndWait()
        phone = Prompt.ask(f"[cyan]Enter the phone number of {name}")

        os.system('clear')
        console.print(BANNER)

        requests.post(f"{API_SERVER_URL}/emergency-contact/", json={
            'username': username,
            'name': name,
            'email': email,
            'phone': phone
        })

        engine.say(f"Successfully registered {name} as an emergency contact!")
        engine.runAndWait()

        counter += 1

    os.system('clear')
    console.print(BANNER)

    # engine.say("Scan the below QR code to get push notifications for emergency contacts.")
    # engine.runAndWait()

    notify_register = notify.register()
    endpoint = notify_register.endpoint

    # print(notify_register)

    requests.post(f"{API_SERVER_URL}/notify-runner/", json={
        'username': username,
        'endpoint': endpoint
    })

    os.system('clear')
    console.print(BANNER)

    engine.say("Enter your age.")
    engine.runAndWait()
    age = IntPrompt.ask("[cyan]Enter your age")

    os.system('clear')
    console.print(BANNER)

    engine.say("Enter your date of birth.")
    engine.runAndWait()
    dob = Prompt.ask("[cyan]Enter your date of birth (format: yyyy-mm-dd)")

    os.system('clear')
    console.print(BANNER)

    engine.say("Enter your sex.")
    engine.runAndWait()
    sex = Prompt.ask("[cyan]Enter your sex", choices=['Male', 'Female', 'Other'])

    os.system('clear')
    console.print(BANNER)

    engine.say("Enter your blood group.")
    engine.runAndWait()
    blood_group = Prompt.ask("[cyan]Enter your blood group")

    requests.post(f"{API_SERVER_URL}/basic-health/", json={
        'username': username,
        'age': age,
        'dob': dob,
        'sex': sex,
        'blood_group': blood_group
    })

    os.system('clear')
    console.print(BANNER)

    engine.say("Setup complete! You may begin using Unified Healthcare Interface!")
    engine.runAndWait()

    write_config(username)

    input()
    generate_test_data(username)

    engine.say(
        "Received scanned hospital records data from the Unified Health Interface mobile app. Processing complete!")
    engine.runAndWait()


def write_config(username):
    json.dump({'username': username}, open(CONFIG_FILE, 'w'))


def read_config():
    return json.load(open(CONFIG_FILE, 'r'))['username']


if not pathlib.Path(CONFIG_FILE).exists():
    setup_new_user()

username = read_config()

while True:
    os.system('clear')
    console.print(BANNER)

    AppKit.NSBeep()

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    query = r.recognize_google(audio)

    os.system('clear')
    console.print(BANNER)

    result = \
        requests.post(f"{RASA_SERVER_URL}/webhooks/rest/webhook", json={'sender': username, 'message': query}).json()[
            0][
            'text']

    # print(result)
    engine.say(result)
    engine.runAndWait()
    input()
