import speech_recognition as sr
from datetime import datetime
import pyttsx3 as speak
import time
import cv2
import pytesseract
import requests
import winsound

pytesseract.pytesseract.tesseract_cmd = "C:/Users/Ollie/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M ")
engine = speak.init("sapi5")
r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)
with mic as source:
    winsound.PlaySound("IronMan.wav", winsound.SND_ASYNC)
    while True:
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
                    engine.say("It is " + dt_string)
                    engine.runAndWait()
                    recognized = ""
                elif recognized == "stop":
                    engine.say("Stopping the program")
                    engine.runAndWait()
                    exit()
                elif recognized == "thank you":
                    engine.say("You're welcome")
                    engine.runAndWait()
                    recognized = ""
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
                        engine.say("Start dictating")
                        engine.runAndWait()
                        audio = r.listen(source)
                        recognized = r.recognize_google(audio)
                        file.write(recognized)
                    elif recognized2 == "rewrite":
                        file = open(recognized, "w")
                        engine.say("Start dictating")
                        engine.runAndWait()
                        audio = r.listen(source)
                        recognized = r.recognize_google(audio)
                        time.sleep(10)
                        file.write(recognized)
                        engine.say("Dictating session ending")
                        engine.runAndWait()
                        exit()
                elif recognized == "read out":
                    cam = cv2.VideoCapture(0)
                    ret, frame = cam.read()
                    cv2.imwrite("webcamphoto.png", frame)
                    cam.release()
                    text = pytesseract.image_to_string(
                        "C:/Users/Ollie/OneDrive/Documents/Python/SpeechInterpreter/webcamphoto.png")
                    engine.say(text)
                    engine.runAndWait()
                    print(text)
                    recognized = ""
                elif recognized == "weather":
                    headers = {
                        "Accept": "application/json"
                    }

                    coat = 0
                    r2 = requests.get(
                        'https://api.open-meteo.com/v1/forecast?latitude=51.8004&longitude='
                        '-0.2169&hourly=precipitation', params={}, headers=headers).json()
                    if datetime.now().day < 10 and datetime.now().month < 10:
                        day = str(datetime.now().year) + "-0" + str(datetime.now().month) + "-0" + str(
                            datetime.now().day) + "T"
                    elif datetime.now().day < 10 and datetime.now().month > 10:
                        day = str(datetime.now().year) + "-" + str(datetime.now().month) + "-0" + str(
                            datetime.now().day) + "T"
                    elif datetime.now().day > 10 and datetime.now().month < 10:
                        day = str(datetime.now().year) + "-0" + str(datetime.now().month) + "-" + str(
                            datetime.now().day) + "T"
                    else:
                        day = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(
                            datetime.now().day) + "T"
                    r_time = r2["hourly"]["time"]
                    r_precipitation = r2["hourly"]["precipitation"]

                    engine.say("What time are you going out(in the 24 hour format and hourly intervals"
                                " for example 06:00)?")
                    engine.runAndWait()
                    outing_time_audio = r.listen(source)
                    outing_time = r.recognize_google(outing_time_audio)
                    if int(outing_time) < 10:
                        outing_time = "0" + outing_time
                    outing_time = outing_time + ":00"
                    engine.say("How many hours will you be out (if not a full hour round up)")
                    engine.runAndWait()
                    outing_length_audio = r.listen(source)
                    outing_length = r.recognize_google(outing_length_audio)
                    outing_length = int(outing_length)
                    index = r_time.index(day + outing_time)
                    for i in range(outing_length):
                        if r_precipitation[index + i] > 0:
                            coat = coat + 1
                    if coat > 0:
                        engine.say("You need to bring your coat (this is just a prediction)")
                        engine.runAndWait()
                    else:
                        engine.say("You do not need to bring your coat (this is just a prediction)")
                        engine.runAndWait()
                    recognized = ""
                else:
                    engine.say("I did not understand that")
                    engine.runAndWait()
                    recognized = ""
