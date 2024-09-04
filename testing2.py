import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import threading

def run_testing2():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("model1/keras_model.h5", "model1/labels.txt")
    offset = 20
    imgSize = 300
    labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
    # labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W","X","Y","Z"]

    def process_frame():
        while True:
            success, img = cap.read()
            if not success:
                break
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
                aspectRatio = h / w
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                            (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.rectangle(imgOutput, (x - offset, y - offset),
                            (x + w + offset, y + h + offset), (255, 0, 255), 4)
                cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)
            cv2.imshow("Image", imgOutput)
            key = cv2.waitKey(1)
            if key == ord('q'):  # Press 'q' to exit the loop
                break

    try:
        # Run the frame processing in a separate thread
        thread = threading.Thread(target=process_frame)
        thread.start()
        thread.join()  # Ensure the thread completes
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return "Testing completed successfully."

def run_testing_words2():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model2/keras_model.h5", "Model2/labels.txt")
    offset = 20
    imgSize = 300
    labels = ["Bye", "Hello", "No", "Perfect", "Thank You", "Yes" ]
    def process_frame():
        while True:
            success, img = cap.read()
            if not success:
                break
            imgOutput = img.copy()
            hands, img = detector.findHands(img)
            if hands:
                hand = hands[0]
                x, y, w, h = hand['bbox']
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
                aspectRatio = h / w
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                            (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.rectangle(imgOutput, (x - offset, y - offset),
                            (x + w + offset, y + h + offset), (255, 0, 255), 4)
                cv2.imshow("ImageCrop", imgCrop)
                cv2.imshow("ImageWhite", imgWhite)
            cv2.imshow("Image", imgOutput)
            key = cv2.waitKey(1)      
            if key == ord('q'):  # Press 'q' to exit the loop
                break

    try:
        # Run the frame processing in a separate thread
        thread = threading.Thread(target=process_frame)
        thread.start()
        thread.join()  # Ensure the thread completes
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return "Testing completed successfully."
# run_testing()


