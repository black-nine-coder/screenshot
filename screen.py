import pyautogui
import os
import time

def take_screenshot(x1, y1, x2, y2):
    image = pyautogui.screenshot(region=(x1,y1, x2-x1, y2-y1))
    # desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    desktop = '/Users/leejukhyun/Desktop/images'
    image = image.convert('RGB')
    image.save(os.path.join(desktop, 'screenshot.jpg'), 'JPEG')

    x1, y1 = pyautogui.position()
    pyautogui.mouseDown()
    x2, y2 = pyautogui.position()
    pyautogui.mouseUp()
    time.sleep(5)


if __name__ == '__main__':
	take_screenshot(100, 200, 300, 400)