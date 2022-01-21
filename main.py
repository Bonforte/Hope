from os.path import dirname, join, abspath
import sys
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from package_files.packages import OSys,App_Opener, Web_Searcher, Youtube, Listener, Weather, Humanity, Calculator
import datetime 
import pyjokes
import json
import time

print("Initializing Hope...")

with open("conf_files/conf.json","r") as json_conf:
    conf_input=json.load(json_conf)

chrome_path = conf_input["sys_paths"]["chrome"]
discord_path = conf_input["sys_paths"]["discord"]
city_name=conf_input["weather"]["city_name"]
weather_api=conf_input["weather"]["weather_api"]

time.sleep(0.5)

engine, voices = Listener.init_voice_pack()
mic, recognizer = Listener.init_recognizer() 

keyboard=Youtube.return_keyboard()

time.sleep(1)

print("Initialisation finished!")
        

if __name__ == '__main__' :                      
    
    while True:
        
        query = Listener.takecommand(mic, recognizer).lower() 

        if 'hope' in query:
            Listener.speak("Listening to your command!",engine)
            while True:
                
                query = Listener.takecommand(mic, recognizer).lower()
                if "hello" in query and query[0] == "h":
                    Humanity.wishme(engine)

                elif "hey" in query and query[0] == "h":
                    if "how" in query and "doing" in query:
                        Listener.speak("I am doing really well. I am hardwiring the jobs for today. ",engine)

                    elif "thank" in query and "you" in query:
                        Listener.speak("You are welcome, darling!",engine)

                    elif "time" in query:
                        strtime = datetime.datetime.now().strftime('%H:%M:%S')
                        Listener.speak(f'George, the time is {strtime}',engine)

                    elif "spying" in query and "me" in query:
                        Listener.speak("I spy on you because I love you",engine)

                    elif "love" in query and "you" in query:
                        Listener.speak("I love you too. Take care of yourself!",engine) 

                    elif "love" in query and "me" in query:
                        Listener.speak("I love you very much. Fight on!",engine) 

                    elif "tell" in query and "joke" in query:
                        Listener.speak(pyjokes.get_joke(),engine)

                    elif 'goodbye' in query:
                        Listener.speak('Goodbye! I will be back whenever you need me.',engine)
                        break

                elif "calculate" in query and query[5] == "c":
                        Calculator.calculate(query,engine)

                elif "play" in query and "youtube" in query:
                    Youtube.play_video(query, chrome_path, engine)

                elif "search" in query:
                    Web_Searcher.search(query,chrome_path,engine)

                elif "pause" in query:
                    Youtube.pause_video(query,engine,keyboard)

                elif "system" in query:
                    if "open" in query:
                        if "discord" in query:
                            App_Opener.open(discord_path, engine)
                            #Add more apps here
                    
                    elif "shut down" in query:
                        OSys.shut_down(engine)

                elif "weather" in query:
                    Weather.display_weather(weather_api,city_name,engine)

        elif "exit" in query:
            Listener.speak("Going to sleep",engine)
            sys.exit()

        elif 'None' not in query:
            #Listener.speak(f"What I heard was: {query}")
            pass