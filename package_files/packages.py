import pyttsx3 as tts
import speech_recognition as sr
import requests
import datetime
import sympy
import webbrowser
import urllib
from pynput.keyboard import Key, Controller
import math
import os
import re
import time
import wikipedia

class Listener:

    def init_voice_pack():
        engine = tts.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        return engine, voices

    def init_recognizer():
        mic = sr.Microphone()
        recognizer = sr.Recognizer()
        return mic, recognizer

    def takecommand(mic, recognizer):                               
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print('Listening...')
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)

        try:                                        
            print('Recognizing...')
            query = recognizer.recognize_google(audio,language = 'en-in')
            print(f'User said: {query}\n')
            return query

        except Exception as e :
            print('Say that again please...')       
            return 'None'

    def speak(audio,engine):                                
        engine.say(audio)
        engine.runAndWait() 

class Weather:

    def get_weather(api,city):
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
        response=requests.get(url).json()
        return response

    def display_weather( weather_api, city_name,engine):
        weather=Weather.get_weather(weather_api,city_name)
                
        Listener.speak("Current temperature is "+ str(math.floor(weather["main"]["temp"]-272.15)) + " degrees Celsius.",engine)
        Listener.speak("It actually feels like "+str(math.floor(weather["main"]["feels_like"]-272.15)) + " degrees Celsius.",engine)
        Listener.speak("Humidity outside is "+str(weather["main"]["humidity"]),engine)
        Listener.speak("The vibe outside is "+str(weather['weather'][0]['description']),engine)

    

class Humanity:

    def wishme(engine):                                    
        hour = int(datetime.datetime.now().hour)
        if hour>=0 and hour<12:
            Listener.speak('Good Morning. It is time to grind!',engine)

        elif hour>12 and hour<18:
            Listener.speak('Good Afternoon! Do not forget to rest sometimes!',engine)

        else:
            Listener.speak('I hope you are having a nice evening, George!',engine)

        Listener.speak('May I help you?',engine)

class Calculator:

    def calculate(query,engine):
        operation = query[14:]
        operation = operation.replace("x","*")
        if "/" in operation:
            operation=operation.split("/")
            operation=sympy.sympify(operation)
            a=float(operation[0])
            b=float(operation[1])
            result=a/b

        else:

            operation=sympy.sympify(operation)
            result=operation
       
        Listener.speak("The results is : "+str(result),engine)

class Youtube:

    def play_video(query, chrome_path, engine):
        keyword=query[21:]
        keyword=keyword.replace(" ","+")   
            
        if keyword:
            Listener.speak("Searching for video.",engine)
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+str(keyword))
        
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

            webbrowser.get(chrome_path).open("https://www.youtube.com/watch?v=" + video_ids[0])

        else:
            Listener.speak("You did not specify a video.",engine)

    def pause_video( query, engine, keyboard):
        Listener.speak("Pause",engine)
        keyboard.press(Key.space)
        keyboard.release(Key.space)

    def return_keyboard():
        return Controller()

class Web_Searcher:
    def search( query, chrome_path, engine):
        Listener.speak('Understood. Searching what you desired!',engine)

        if "busy" in query:
            webbrowser.get(chrome_path).open("biziday.ro")

        elif "work" in query and "email" in query:
            webbrowser.get(chrome_path).open("webmail.eli-np.ro")
            Listener.speak("Checking work mails.",engine)
        elif "wikipedia" in query:
            Listener.speak('Searching Wikipedia....')
            query = query.replace('wikipedia','')
            query = query.replace('hope','')
            query = query.replace('search','')
            results = wikipedia.summary(query, sentences = 4)
            Listener.speak(results, engine)
        else:
            webbrowser.get(chrome_path).open(str(query[12:]))


class App_Opener:
    def open( path, engine):
        Listener.speak('Understood. Opening your desired app!',engine)
        os.startfile(path)

class OSys:
    def shut_down(engine):
        Listener.speak("Shutting down the system in 3 seconds.",engine)
        time.sleep(3)
        os.system("shutdown /s /t 1")