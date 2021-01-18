
from multiprocessing import Process
from pocketsphinx import LiveSpeech
import argparse
import cv2
import pyautogui
import pydirectinput
from yolo import YOLO
from keybinding import PressKey,ReleaseKey
import time  

ap = argparse.ArgumentParser()
ap.add_argument('-n', '--network', default="tiny", help='Network Type: normal / tiny / prn / v4-tiny')
ap.add_argument('-d', '--device', default=0, help='Device to use')
ap.add_argument('-s', '--size', default=416, help='Size for yolo')
ap.add_argument('-c', '--confidence', default=0.2, help='Confidence for yolo')
args = ap.parse_args()


if args.network == "normal":
    print("loading yolo...")
    yolo = YOLO("models/cross-hands.cfg", "models/cross-hands.weights", ["hand"])
elif args.network == "prn":
    print("loading yolo-tiny-prn...")
    yolo = YOLO("models/cross-hands-tiny-prn.cfg", "models/cross-hands-tiny-prn.weights", ["hand"])
elif args.network == "v4-tiny":
    print("loading yolov4-tiny-prn...")
    yolo = YOLO("models/cross-hands-yolov4-tiny.cfg", "models/cross-hands-yolov4-tiny.weights", ["hand"])
else:
    print("loading yolo-tiny...")
    yolo = YOLO("models/cross-hands-tiny.cfg", "models/cross-hands-tiny.weights", ["hand"])


def boom():
    boom = LiveSpeech(lm=False, keyphrase='jump', kws_threshold=1e-30)
    for phrase in boom:
        print(phrase.segments(detailed=True))
        if phrase.segments(detailed=True):
            PressKey(0x39)
            time.sleep(0.05)
            ReleaseKey(0x39)
def stop():
    stop = LiveSpeech(lm=False, keyphrase='shoot', kws_threshold=1e-20)
    for phrase in stop:
        print(phrase.segments(detailed=True))

def hand_gesture():
    yolo.size = int(args.size)
    yolo.confidence = float(args.confidence)

    print("starting webcam...")
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    W = 0x11
    A = 0x1E
    S = 0x1F
    D = 0x20

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False
    pydirectinput.FAILSAFE = False
    pressed_key = None
    while rval:
        width, height, inference_time, results = yolo.inference(frame)
        cv2.rectangle(frame , (200,180),(400,300),(255,255,255),2)
    
        for detection in results:
            id, name, confidence, x, y, w, h = detection
            cx = x + (w / 2)
            cy = y + (h / 2)
            # draw a bounding box rectangle and label on the image
            center_of_hand = ((2*x+w)//2,(2*y+h)//2)
            color = (0, 255, 255)
            cv2.circle(frame , center_of_hand,5,color,5)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = "%s (%s)" % (name, round(confidence, 2))
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color, 2)
            if center_of_hand[0] < 200 and center_of_hand[1] in range(180,300):
                if pressed_key != D:
                    if pressed_key is not None:
                        ReleaseKey(pressed_key)
                    PressKey(D)
                    pressed_key=D

            elif center_of_hand[0] > 400 and center_of_hand[1] in range(180,300):
                if pressed_key != A:
                    if pressed_key is not None:
                        ReleaseKey(pressed_key)
                    PressKey(A)
                    pressed_key=A
            elif center_of_hand[0] in range(200,400) and center_of_hand[1] > 300:
                if pressed_key != S:
                    if pressed_key is not None:
                        ReleaseKey(pressed_key)
                    PressKey(S)
                    pressed_key=S
            elif center_of_hand[0] in range(200,400) and center_of_hand[1] < 180:
                if pressed_key != W:
                    if pressed_key is not None:
                        ReleaseKey(pressed_key)
                    PressKey(W)
                    pressed_key=W  
            else:
                if pressed_key is not None:
                        ReleaseKey(pressed_key)
                        pressed_key = None                 
        frame = cv2.flip(frame,1)    
        cv2.imshow("preview",frame )

        rval, frame = vc.read()

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow("preview")
    vc.release()


if __name__ == "__main__":
    p1 = Process(target=boom)
    p1.start()
    p2 = Process(target=stop)
    p2.start()
    p3 = Process(target=hand_gesture)
    p3.start()