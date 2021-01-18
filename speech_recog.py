
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
