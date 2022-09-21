import speech_recognition 
import os
import sys
import webbrowser
import pyttsx3
from socket import gethostbyname, create_connection
from datetime import datetime
import random
import requests
from datetime import datetime
from googletrans import Translator
from langdetect import detect


api_key = 'your api_key'

launch = 'ON'

def check_net():
    try:
        print("Проверка интернет соединения")
        host = gethostbyname("www.google.com")
        link = create_connection((host, 80), 2)
        link.close()
        print("Есть подключение")
        return True
    except Exception:
        print("Подключение отсутствует")


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru')
for voice in voices:
    if voice.name == 'Aleksandr':
        tts.setProperty('voice', voice.id)


def speak(words):
    tts.say(words)
    tts.runAndWait()


translator = Translator()

commands_dict = {
    'commands': {
        'greeting': ['привет', 'здравствуй'],
        'get_weather': ['погода', 'градусов'],
        'get_time': ['время', 'сколько сейчас'],
        'create_task': ['добавить задачу', 'создать задачу'],
        'work_with_browser': ['интернет', 'браузер'],
        'open_file': ['файл', 'запись'],
        'repeat': ['повтори'],
        'random_number': ['случайное', 'рандомное'],
        'solve': ['реши', 'посчитай'],
        'translate': ['перевод', 'переведи'],
        'game': ['поиграть', 'игра', 'скучно'],
        'goodbye': ['пока', 'выйти', 'закрыть'],
    }
}


def listen_command():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-Ru').lower()
        return query
    except speech_recognition.UnknownValueError:
        return "Damn..."


def greeting():
    speak("Привет")
    print("Привет")


def get_weather():
    city = listen_command()
    try: 
        get_city = requests.get("http://api.openweathermap.org/data/2.5/find",
            params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': api_key})
        data = get_city.json()
        for_voice = data['list'][0]['main']['temp']
        print('Температура сейчас - ', data['list'][0]['main']['temp'])
        speak(for_voice)
    except Exception as error:
        return f"Exception: {error}"


def get_time():
    time_init = datetime.now().time()
    time_n = f"{time_init.hour}:{time_init.minute}"
    speak(time_n)
    print("Сейчас - ", time_n)


def create_task():
    speak("Что добавить в список?")
    print("Что добавить в список?")

    query = listen_command()

    with open('todo-list.txt', 'a') as file:
        file.write(f"{query}\n")
    
    speak("Задача добавлена")
    print(f"Задача {query} была добавлена в список")


def work_with_browser():
    query = listen_command()
    var = query.split()
    if var[1] == 'вк':
        var[1] = 'vk'
        url = f"https://{var[1]}.com"
        webbrowser.get(using='safari').open(url)
        speak("Открываю...VK")
        print("Открываю...VK")


def open_file():
    speak("Открываю")
    print("Открываю...")
    with open('todo-list', 'r') as file:
        print(file.read())


def repeat():
    query = listen_command()
    speak(query)
    print(query)


def random_number():
    limits = listen_command().split()
    x = int(limits[1])
    y = int(limits[3])
    r_num = random.randint(x, y)
    speak(str(r_num))
    print("Ваше случайное число - ", r_num)


def solve():
    speak("Что посчитать?")
    phrase = listen_command().split()
    x = int(phrase[0])
    y = int(phrase[2])
    operation = phrase[1]

    if operation == '+':
        res = x + y
        speak(str(res))
        print(res)
    elif operation == '-':
        res = x - y
        speak(str(res))
        print(res)
    elif operation == 'х':
        res = x * y
        speak(str(res))
        print(res)
    elif operation == '/':
        res = x / y
        speak(str(res))
        print(res)
    else:
        speak('Что-то пошло не так ') 
        print('Что-то пошло не так ')

    
def translate():
    speak("Что перевести?")
    words = listen_command()
    details = detect(words)
    
    if details == 'en':
        res = translator.translate(words, dest='ru')
    else:
        res = translator.translate(words, dest='en')

    speak(str(res.text))
    print(res.text)


def game():
    flag = 'on'

    values_all = {
    'Камень': 'Ножницы',
    'Ножницы': 'Бумага',
    'Бумага': 'Камень'
    }

    while flag == 'on':
        value_vs = random.choice(list(values_all.keys()))
        value_us = listen_command()

        if value_us == value_vs:
            speak('Ничья')
            print('Ничья')
            continue
        for v_us, v_vs in values_all.items():
            if value_us == v_us and value_vs == v_vs:
                speak("Ты победил")
                print("Ты победил")
                break
            elif value_vs == v_vs and value_us == v_us:
                speak('Победа за мной')
                print('Победа за мной')
                break
        
        if value_us == 'Завершить':
            flag = "off"


def goodbye():
    global launch
    launch = 'OFF'
    speak('До скорого!')
    print('До скорого!')


def main():
    query = listen_command()

    for k, v in commands_dict['commands'].items():
        if query in v:
            globals()[k]()


if __name__ == '__main__' and check_net() == True:
    # if check_net() == True:
    print("<|Голосовой помощник|>")
    while launch != 'OFF':
        print('Произнесите команду... ')
        speak('Чем могу помочь?')
        main()
