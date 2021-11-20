import random
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import time
import requests

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
URL = "https://minecraft-mp.com/server/295107/vote?alternate_captcha=2"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"

def delay():
    time.sleep(random.randint(4, 6))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result


try:
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    delay()
    # go to website which have recaptcha protection
    driver.get(URL)
    delay()
    
except Exception as e:
   print("Ye")

g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
outerIframe.click()

xapt = driver.find_element_by_name("accept")
xapt.click()
nicknames = driver.find_element_by_name("nickname")
nicknames.send_keys(Keys.ENTER)
iframes = driver.find_elements_by_tag_name('iframe')
print("[INFO!] Minecraft NickName = MengKosong")
audioBtnFound = False
audioBtnIndex = -1

for index in range(len(iframes)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(delayTime)
    try:
        audioBtn = driver.find_element_by_id("recaptcha-audio-button")
        audioBtn.click()
        audioBtnFound = True
        audioBtnIndex = index
        break
    except Exception as e:
        pass

if audioBtnFound:
    try:
        while True:
            # get the mp3 audio fil
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)

            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)

            # key in results and submit
            inputField = driver.find_element_by_id("audio-response")
            inputField.send_keys(key)
            delay()
            inputField.send_keys(Keys.ENTER)
            delay()
            print("S")
            time.sleep(3)

            err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
            if err.text == "" or err.value_of_css_property('display') == 'none':
                print("[INFO] Success!")
                break

    except Exception as e:
        print(e)
else:
    sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")

time.sleep(30)
driver.quit()
