import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep, time
import cvzone

# Initialize the webcam and set its properties
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8)

# Define the keyboard keys layout
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space", "Backspace"]]

# Define a function to draw all the keys on the screen
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

# Define the Button class
class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Create button instances for each key
buttonList = []
for i in range(len(keys) - 1):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Add the Space and Backspace buttons with custom sizes and positions
buttonList.append(Button([50, 350], "Space", [500, 85]))
buttonList.append(Button([600, 350], "Backspace", [200, 85]))

# Initialize a variable to keep track of the last key press time
last_click_time = 0
finalText = ""

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image horizontally
    hands, img = detector.findHands(img)  # returns hands and the processed image
    img = drawAll(img, buttonList)

    if hands:
        lmList = hands[0]['lmList']  # Landmark list of the first hand
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                # Find distance between tip of index (lmList[8]) and tip of middle finger (lmList[12])
                l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2])

                # When clicked
                if l < 30 and (time() - last_click_time) > 0.5:
                    last_click_time = time()
                    if button.text == "Space":
                        finalText += " "
                    elif button.text == "Backspace":
                        finalText = finalText[:-1]
                    else:
                        finalText += button.text

                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    sleep(0.15)

    # Display the typed text
    cv2.rectangle(img, (50, 450), (1100, 550), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 520), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    # Check if 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for 'Esc'
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
