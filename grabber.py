import pyautogui
import time
import os
from PIL import Image
import pytesseract
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:/Users/Andre/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
months_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def text_to_datetime(my_text):
    print(my_text)
    separated_info = my_text.split()
    day_text = separated_info[0]
    day_number = int(day_text)

    month_text = separated_info[1]
    month_number = months_dict[month_text]

    year_number = int(separated_info[2])

    time = separated_info[3]
    hour_text = ''
    for character in time:
        if character == ':' or character == '-' or character == ';' or character == '_':
            break
        hour_text += character
    hour_number = int(hour_text)
    
    return datetime(year_number, month_number, day_number, hour_number)

def get_timestamp(image):
    text_timestamp = pytesseract.image_to_string(image)
    return text_to_datetime(text_timestamp)

print("Put mouse pointer on prev button")
time.sleep(10)
curpos = pyautogui.position()
print(curpos)

# Find out where the image is in the screen
full_img = pyautogui.screenshot()

# Find top corner of photo
left = curpos.x
top = curpos.y

# Get pixel colour to the right of the button
pixels = full_img.load()
left = left + 20
bg_pix = pixels[left,top]
cur_pix = bg_pix

# Scan right until pix changes
while cur_pix == bg_pix:
    left = left + 1
    cur_pix = pixels[left,top]

# Scan up until pixel changes back to background colour
while cur_pix != bg_pix:
    top = top - 1
    cur_pix = pixels[left,top]

top = top + 1
print(left,top)
img_centre = pyautogui.center((left,top,800,600))

# Now start grabbing
while(1):
    try:
        # Code to extract the timestamp from what's onscreen
        # This is just something temporary to emulate that
        image = pyautogui.screenshot('screenshot.png',region=(left+245,top+410,155,20))
        timestamp = get_timestamp(image)
        timestamp = format(timestamp)
        timestamp = timestamp.replace(' ', '_')
        timestamp = timestamp.replace(':', '-')

        # Click the image to cause it to be downloaded to Downloads
        pyautogui.click(img_centre.x, img_centre.y)
        time.sleep(2) # Needed to ensure the image download has finished

        # Find the downloaded file
        downloads_dir = 'C:/Users/Andre/Downloads'
        found_files = os.listdir(downloads_dir)
        for fname in found_files:
            if fname.startswith('W1si'):
                os.rename(downloads_dir + '/' + fname, timestamp + '.jpg')
    except:
        downloads_dir = 'C:/Users/Andre/Downloads'
        found_files = os.listdir(downloads_dir)
        for fname in found_files:
            if fname.startswith('W1si'):
                os.remove(downloads_dir + '/' + fname)

    # Move on to next image
    pyautogui.click(curpos.x,curpos.y)
    time.sleep(3)