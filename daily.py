import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.service import Service
import speech_recognition as sr
from pydub import AudioSegment
import requests
import undetected_chromedriver as uc;
from twocaptcha import TwoCaptcha;
from pathlib import Path
from utils import *;
import json

class LocalStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()



def convert(mp3, wav):
    try:
        input_file = mp3
        audio = AudioSegment.from_file(input_file, format="mp3")
        output_file = wav
        audio.export(output_file, format="wav")
    except:
        pass




def daily(*args):
    with open('tokens.txt', 'r') as f:
        tokens = f.read().splitlines();
        print(tokens)
    for token in tokens:
        options = uc.ChromeOptions()
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        driver = uc.Chrome(options=options)
        driver.set_window_size(1020, 800)
        driver.get('https://discord.com/oauth2/authorize?client_id=282859044593598464&scope=identify+guilds+email&response_type=code&redirect_uri=https://api.probot.io/auth');
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div/div[1]/div/div[2]/button'))).click()
        
        token_script = f"""
            function login(token) {{
                        setInterval(() => {{
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`
                            }}, 50)
                        setTimeout(() => {{
                  location.reload()
                    }}, 2500)
            }}
        login("{token}")
        """
        print(token)
        driver.execute_script(script=token_script)
        driver.refresh()
        wait = WebDriverWait(driver=driver, timeout=20)
        auth_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='button-ejjZWC lookFilled-1H2Jvj colorBrand-2M3O3N sizeMedium-2oH5mg grow-2T4nbg']")))
        auth_btn.click()
        time.sleep(2)
        driver.get('https://probot.io/daily');
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div[1]/div/div[2]'))).click();
        print(driver.window_handles)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1]);
        time.sleep(2)
        sauth_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[@class='button-ejjZWC lookFilled-1H2Jvj colorBrand-2M3O3N sizeMedium-2oH5mg grow-2T4nbg']")))
        sauth_btn.click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(4)
        try:
            if driver.find_element(By.XPATH, '//*[@id="daily-time-left"]'):
                try:
                    os.system("taskkill /im chrome.exe /f")
                    continue;
                except Exception:
                    continue;
            else:
                pass;
        except Exception:
            pass;
        rewards_btn = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.onboarding-container > .content > button')))
        rewards_btn.click()
        try:
            if driver.find_element(By.XPATH, '//*[@id="daily-time-left"]'):
                try:
                    os.system("taskkill /im chrome.exe /f")
                    
                    continue;
                except Exception:
                    
                    continue;
            else:
                pass;
        except Exception:
            pass;
        time.sleep(2)
        container = driver.find_element(By.CSS_SELECTOR, ".daily-logo-text")
        container.click()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
        time.sleep(2)
        driver.switch_to.default_content()
        
        driver.switch_to.frame(driver.find_element(
        By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
        driver.find_element(By.ID, "recaptcha-audio-button").click()
        time.sleep(2)
        m = driver.find_element(By.ID, "audio-source").get_attribute('src')
        print(m)
        res = requests.get(m)
        with open('files/file.mp3', 'wb') as file:
            file.write(res.content)
            convert('files/file.mp3', 'files/file.wav')
            r = sr.Recognizer()
            with sr.AudioFile('files/file.wav') as source:
                audio = r.listen(source)
                text = r.recognize_google(audio)
                time.sleep(4)
                driver.find_element(By.ID, "audio-response").send_keys(text);
                driver.find_element(By.ID, "recaptcha-verify-button").click();
                time.sleep(2)
                send_webhook_things(name="Sphinx TOOL", money="Not yet discoverd", token=token, discord_webhook_url='https://discord.com/api/webhooks/1086810216785514607/muhHsg8aPN3RTpa1tct-5zwBo2_CfH7S3Qaoo9SUrIBoamSUAQNiHisy3mXabt72okI-')
                
                try:
                    if driver.find_element(By.XPATH, '//*[@id="daily-multiple-devices-div"]/h3'):
                        changeVPN()
                        continue;
                except:
                    continue;

daily()