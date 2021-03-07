import speech_recognition as sr
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import webbrowser
import playsound
import re
import os

#import gi
import random
import time
from gtts import gTTS
from sys import platform
if platform == "linux" or platform == "linux2":
    PATH="./chromedriver"
elif platform == "win32":
    PATH="./chromedriver.exe"
r=sr.Recognizer()
def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        voice_data=''
        try:
            voice_data= r.recognize_google(audio)
        except sr.UnknownValueError:
            blue_speak("Sorry,I did Not get that")
        except sr.RequestError:
            blue_speak("Sorry,My speech service is down")
        return voice_data


def moodle_login():
    driver = webdriver.Chrome(PATH)
    blue_speak("Enter Username ")
    usrn=input()
    blue_speak("Enter Password ")
    passwd=input()
    driver.get("https://moodle.iitd.ac.in/login/index.php")
    usrname = driver.find_element_by_id("username")
    password=driver.find_element_by_id("password")
    text = driver.find_element_by_id("login").text
    cap=driver.find_element_by_id("valuepkg3")
    Number=[int(s) for s in text.split()if s.isdigit()]
    if 'add' in text:
        result=Number[0]+Number[1]
    elif 'subtract' in text:
        result=Number[0]-Number[1]
    elif 'first' in text:
        result=Number[0]
    else:
        result=Number[1]
    usrname.send_keys(usrn)
    password.send_keys(passwd)
    cap.send_keys(result)
    submit=driver.find_element_by_id("loginbtn")
    submit.click()
def search_studm():
    for i in range(3):
        search= record_audio(blue_speak('Can You Say me the topic name'))
        if search.strip()!="":
            break
        else:
            blue_speak("Say that again")
    url = "https://google.com/search?q=" + search +' nptel'
    yurl= "https://www.youtube.com/results?search_query=" + search + ' nptel' 
    webbrowser.get().open(url)
    webbrowser.get().open(yurl)
    blue_speak("Here is what I found for " + search)
def p_songs():
    song=record_audio(blue_speak('Tell me the song name'))
    driver = webdriver.Chrome(PATH)
    link="https://music.youtube.com/search?q=" + song
    driver.get(link)
    try:
        play=driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[2]/div[2]/ytmusic-responsive-list-item-renderer[1]/div[1]/ytmusic-item-thumbnail-overlay-renderer/div/ytmusic-play-button-renderer/div/yt-icon')
        play.click()
        time.sleep(1)
        blue_speak("Do you want to Continue This song")
        decide1=record_audio()
        if 'no' in decide1:
            driver.quit()
        else:
            time.sleep(200)
            blue_speak("do you want to listen more songs")
            decide2=record_audio()
            if 'finish' in decide2:
                pass 
            elif 'yes' in decide2:
                p_songs()
            else:
                driver.quit()
                return 0

    except NoSuchElementException:
        blue_speak("No song found")


def respond(voice_data):
    if 'login' in voice_data:
        moodle_login()
    elif 'song' in voice_data or "music" in voice_data:
        p_songs()    
    elif 'study material' in voice_data:
        search_studm()
    elif 'your' in voice_data and 'name' in voice_data:
        blue_speak("My name is Blue\nWhat's your name?")
        name = record_audio()
        if name !="":
            blue_speak("Hello %s"%name)
    else:
        blue_speak("I don't know how to help with that but I am learning.")
  
def blue_speak(audio_string):
    print(audio_string)
    tts= gTTS(text=audio_string, lang='en')
    r =random.randint(1,1000000)
    audio_file= 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)
def weather():
    Ip_info = get('https://api.ipdata.co?api-key=test').json()
    latlong=[Ip_info['latitude'],Ip_info['longitude']]
    weather = get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=cd809c3984afb49d5e8a9ff4d8e7b405'.format(latlong[0], latlong[1])).json()
    weather_info1=weather.values()
    print(weather_info1)
blue_speak("How can i help you?")
#time.sleep(2)
while 1:
    voice_data = record_audio()
    if voice_data.strip()=="":
        blue_speak("Try again Later")
        break
    elif "exit" in voice_data or "quit" in voice_data:
        blue_speak("Thank You")
        break
    print(voice_data)
    respond(voice_data)
    blue_speak("Anything else? ")
    
