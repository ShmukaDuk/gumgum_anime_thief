import pyautogui
import pygetwindow as gw
from pynput import keyboard
import pyperclip
import sys
import time
from PIL import Image, ImageChops
import os


from urllib.parse import urljoin
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import random
import signal
import sys

SHOW_NAME = "One Piece"
GOGOLINK = "https://ww4.gogoanime2.org/watch/one-piece-dub/"
LATEST_EPISODE = 988
STARTING_EPISODE = 798

def findPirateScreen():
    play_button = "\x00"
    for i in range(10):
        play_button = findButton("deps/a_button.png")
        if play_button is not None:
            break
            time.sleep(1)
        else:
            return -1
    if play_button is not None:
        x, y = play_button
        pyautogui.moveTo(x, y, 0.2)
        pyautogui.click()
        time.sleep(0.01)
        pyautogui.click()
        pyautogui.hotkey('left')
        
        button_path = ""
        button_counter = 1
        download_button = findButton(f"deps/download_button_{button_counter}.png")
        while download_button is None:
            button_counter += 1
            button_filename = f"deps/download_button_{button_counter}.png"
            button_filepath = os.path.join(button_path, button_filename)
            
            if os.path.isfile(button_filepath):
                print("found button: ", button_filepath)
                download_button = findButton(button_filepath)
            else:
                break
        
        if download_button is not None:
            x, y = download_button
            pyautogui.moveTo(x, y, 0.2)
            pyautogui.click()
            time.sleep(5)
            return 0
        else:
            return -1
    else:
        return -1

def extractHTML(resolution):
    background = findButton("deps/download_page_background.png")
    x, y = background
    pyautogui.hotkey('ctrl', "shift", 'c')
    pyautogui.moveTo( x + random.randint(1, 10) , y, 1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.1)
    pyperclip.copy(resolution)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('escape')    
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    print(pyperclip.paste())
    html_string = pyperclip.paste()
    pyautogui.hotkey('ctrl', 'shift', "i")
    time.sleep(0.3)
    return html_string
    
    
def getLink(episode_number):
    resolutions = ["1080p", "720p", "480p", "360p"]
    resolution_txt = ""
    link = ""
    for resolution in resolutions:
        link = extractHTML(resolution)
        if link.startswith('<a href="https://gogodownload.net'):
            resolution_txt = resolution
            break
        if resolution == "360p":
            return -1
    
    print(link, resolution_txt)
    saveStringToList(episode_number, resolution_txt, link)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(1)
    return 0
    
def saveStringToList(episode_number, resolution, html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    link = soup.a['href']

    # Format the entry as "ep_number, resolution, link"
    
    entry = f"{SHOW_NAME}, {episode_number}, {resolution}, {link}"
    pyperclip.copy(link)
    # Append the entry to the text file
    with open('download_list.txt', 'a') as file:
        file.write(entry + '\n')
    print("Entry added to the file.")
    
def on_key_press(key):
    try:
        if key.char == 'a':
            pirate()
        elif key.char == 'q':
            print("Quitting")
            return False
    except AttributeError:
        pass

def idmDownload():
    result = pyautogui.locateOnScreen("deps/idm_download_button.png")
    if result is not None:
        x, y = pyautogui.center(result)
        print("Button found at:", x, y)
        pyautogui.moveTo(x, y, 1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(1)
        pyautogui.hotkey('right')
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(1)
        
    else:
        print("Button not found.")
    return 

def goToEpisode(episode_number, window):
    if window is not None:
        left, top, width, height = window.left, window.top, window.width, window.height   
        pyautogui.moveTo(left + 300, top + 60, 1)
        pyautogui.click()
        pyperclip.copy(GOGOLINK + str(episode_number))
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        time.sleep(5)    
    return 1

def pirate():
    for episode in range(LATEST_EPISODE, LATEST_EPISODE + 1):
        #load webpage
        goToEpisode(episode)    
        #open download page
        if (findPirateScreen() < 0):
            print ("no pirates here")
            continue
        #scrape download link
        if(getLink(episode) < 0):
            continue
        idmDownload()

def signal_handler(signal, frame):
    print("Closing the program...")
    sys.exit(0)    


def findButton(button_picture):
    window = gw.getActiveWindow()
    left, top, width, height = window.left, window.top, window.width, window.height
    result = pyautogui.locateOnScreen(button_picture, region=(left, top, width, height))
    if result is not None:
        x, y = pyautogui.center(result)
        print("Button found at:", x, y)
        return x, y
        pyautogui.moveTo(x, y, 1)
        
    else:
        print("Button not found.")
    return 
    
    

def main():  
    print("GUMGUM ART THIEF!")
    signal.signal(signal.SIGINT, signal_handler)

    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()   
    listener.join()

if __name__ == "__main__":
    main()



