import speech_recognition as sr
from datetime import datetime
import pyttsx3 as speak
import time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M ")
engine = speak.init("sapi5")
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)
with mic as source:
    while True:
        audio = r.listen(source)

        while True:
            try:
                audio = r.listen(source)
                recognized = r.recognize_google(audio)
                if recognized == "activate":
                    break
            except sr.UnknownValueError:
                engine.say("Say activate to begin")
                engine.runAndWait()
            except KeyboardInterrupt:
                raise
        if recognized == "activate":
            engine.say("How may I help you")
            while recognized == "activate":
                engine.runAndWait()
                audio = r.listen(source)
                recognized = r.recognize_google(audio)
                if recognized == "hello":
                    engine.say("Hello to you too")
                    engine.runAndWait()
                    recognized = ""
                elif recognized == "what's the time":
                    engine.say("It is "+dt_string)
                    engine.runAndWait()
                    recognized = ""
                elif recognized == "stop":
                    engine.say("Stopping the program")
                    engine.runAndWait()
                    exit()
                elif recognized == "thank you":
                    engine.say("You're welcome")
                    engine.runAndWait()
                elif recognized == "dictate":
                    engine.say("What is the file called")
                    engine.runAndWait()
                    audio = r.listen(source)
                    recognized = r.recognize_google(audio)
                    engine.say("Would you like to append or rewrite")
                    engine.runAndWait()
                    audio2 = r.listen(source)
                    recognized2 = r.recognize_google(audio2)
                    if recognized2 == "append":
                        file = open(recognized, "a")
                        audio = r.listen(source)
                        recognized = r.recognize_google(audio)
                        engine.say("Start dictating")
                        engine.runAndWait()
                        file.write(recognized)
                    elif recognized2 == "rewrite":
                        file = open(recognized, "w")
                        audio = r.listen(source)
                        recognized = r.recognize_google(audio)
                        engine.say("Start dictating")
                        engine.runAndWait()
                        time.sleep(10)
                        file.write(recognized)
                        engine.say("Dictating session ending")
                        exit()
                else:
                    engine.say("I did not understand that")
                    engine.runAndWait()
                    recognized = ""
