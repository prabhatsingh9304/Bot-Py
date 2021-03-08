import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import webbrowser
import playsound
import os
import re
from requests import get
import random
import time
from gtts import gTTS
from sys import platform
if platform == "linux" or platform == "linux2":
    PATH="./chromedriver"
elif platform == "win32":
    PATH="./chromedriver.exe"
r=sr.Recognizer()
def check(answer):
    time.sleep(2)
    if answer != None:
        return
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
        return voice_data.lower()


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
        search= record_audio(blue_speak('Tell me the topic name'))
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
        time.sleep(5)
        stop=driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/paper-icon-button[2]/iron-icon')
        stop.click()
        blue_speak("Do you want to Continue This song? yes or no")
        decide1=record_audio()
        if 'yes' in decide1.lower():
            stop=driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/paper-icon-button[2]/iron-icon')
            stop.click()
            time.sleep(170)
        else:
            driver.quit()
           
    except NoSuchElementException:
        blue_speak("No song found")

def die():
    a=random.randint(1, 6)
    blue_speak("You got %d"%a) 
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
    elif 'die' in voice_data or 'dice' in voice_data:
        die()
    elif 'weather' in voice_data:
        weather()
    else:
        blue_speak("I don't know how to help with that but I am learning.")
def weather():
    Ip_info = get('https://api.ipdata.co?api-key=test').json()
    latlong=[Ip_info['latitude'],Ip_info['longitude']]
    weather = get('http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=cd809c3984afb49d5e8a9ff4d8e7b405'.format(latlong[0], latlong[1])).json()
    weather_info1=list(weather.values())
    maxt=int(weather_info1[3]['temp_max']-273.15)
    mint=int(weather_info1[3]['temp_min']-273.15)
    hum=int(weather_info1[3]['humidity'])
    blue_speak("Todays' maximum temperature is %d and\nminimum temperature is %d degree celsius and\nhumidity is %d"%(maxt,mint,hum))
def blue_speak(audio_string):
    print(audio_string)
    tts= gTTS(text=audio_string, lang='en')
    r =random.randint(1,1000000)
    audio_file= 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    os.remove(audio_file)
blue_speak("How can i help you?")
while 1:
    voice_data = record_audio()
    if voice_data.strip()=="":
        blue_speak("Try again Later")
        break
    elif "exit" in voice_data or "quit" in voice_data or voice_data=="no":
        blue_speak("Thank You")
        break
    print(voice_data)
    respond(voice_data)
    blue_speak("Anything else? ")
