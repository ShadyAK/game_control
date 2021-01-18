'''from pocketsphinx import LiveSpeech
import speech_recognition as sr
import threading
#for index, name in enumerate(sr.Microphone.list_microphone_names()):
  #  print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
#for phrase in LiveSpeech(): print(phrase


r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)                # use the default microphone as the audio source
    audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

try:
    print("You said " + r.recognize_google(audio))    # recognize speech using Google Speech Recognition
except:                           # speech is unintelligible
    print("Could not understand audio")
#r.recognize_sphinx(audio)    



def boom():
    boom = LiveSpeech(lm=False, keyphrase='boom', kws_threshold=1e-30)
    for phrase in boom:
        print(phrase.segments(detailed=True))
    print('pass')
def stop():
    stop = LiveSpeech(lm=False, keyphrase='stop', kws_threshold=1e-30)
    for phrase in stop:
        print(phrase.segments(detailed=True))
    print('pass')
print(__name__)
'''
import logging
import threading
import time


from multiprocessing import Process
from pocketsphinx import LiveSpeech
    
def boom():
    boom = LiveSpeech(lm=False, keyphrase='jump', kws_threshold=1e-20)
    for phrase in boom:
        print(phrase.segments(detailed=True))
def stop():
    stop = LiveSpeech(lm=False, keyphrase='roll', kws_threshold=1e-20)
    for phrase in stop:
        print(phrase.segments(detailed=True))
        
            
if __name__ == "__main__":
    p1 = Process(target=boom)
    p1.start()
    p2 = Process(target=stop)
    p2.start()