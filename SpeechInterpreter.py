import speech_recognition as sr
r = sr.Recognizer()
harvard = sr.AudioFile('harvard.wav')
with harvard as source:
    audio = r.record(source)
    text = r.recognize_google(audio)
print(text)
jackhammer = sr.AudioFile('jackhammer.wav')
with jackhammer as source:
    r.adjust_for_ambient_noise(source)
    audio2 = r.record(source)
    text2 = r.recognize_google(audio2)
print(text2)
mic = sr.Microphone(device_index=1)
print(mic)
with mic as source:
    audio = r.listen(source)
    text3 = r.recognize_google(audio)
print(text3)
