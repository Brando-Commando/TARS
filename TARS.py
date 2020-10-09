# This will be a Personal Voice Assistant following various tutorials listed below:
# https://www.geeksforgeeks.org/personal-voice-assistant-in-python/

# It seems that several aspects of the tutorial are outdated, and those aspects need to be redone
# What needs to be redone  
#   -calcuating with Wolfram Alpha
#   -searching with firefox

# Importing -
import speech_recognition as sr # from google
import playsound # to play saved mp3 files
from gtts import gTTS # googles Text To Speech for output
import os # for file functions
import wolframalpha # for mathamatical calculations from strings
from selenium import webdriver # for browser operations
import time

num = 1
def assistant_speaks(output):
    global num

    # num renames every audio file to remove ambiguity
    num += 1
    print("TARS : ", output)

    toSpeak = gTTS(text = output, lang='en', slow = False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file
    playsound.playsound(file, True)
    os.remove(file)

def get_audio():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")

        # recording the audio using speech recog
        audio = rObject.listen(source, phrase_time_limit = 5)
    print("Stop.") # limits to 5 currently

    try:
        
        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except: # exception for when command could not be understood

        assistant_speaks("Could not understand that, please try again!")
        return 0

def process_text(input):
    try:
        if 'search' in input or 'play' in input:
            # basic web crawler using selenium
            search_web(input)
            return

        elif "who are you" in input or "define yourself" in input:
            speak = " I am Tars. A personal Assistant. I am currently in beta testing."
            assistant_speaks(speak)
            return
        
        elif "calculate" in input():
            # wolframalpha app_id - 
            app_id = ""
            client = wolframalpha.Client(app_id)
            
            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text 
            assistant_speaks("The answer is " + answer)
            return

        else:
            assistant_speaks("I can search the web for you. Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)
            else: 
                return
    except:
        assistant_speaks("I don't understand, I can search the web for you, do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)

def search_web(input):

    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if 'youtube' in input.lower():

        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query))
        return
    
    elif 'wikipedia' in input.lower():

        assistant_speaks("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

# Driver Code
if __name__ == "__main__":
    assistant_speaks("What's your name, user?")
    name ='user'
    name = get_audio()
    assistant_speaks("Hello, " + name + '.')

    while(1):
        
        assistant_speaks("What can i do for you?")
        text = get_audio().lower()

        if text == 0:
            continue

        if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, " + name + '.')
            break

        # calling process text to process the query
        process_text(text)