import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import time
import warnings
import calendar
import random
import wikipedia
import webbrowser
import subprocess
import pyjokes

warnings.filterwarnings('ignore')

# Function that helps us to record our voice
def recordAudio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say Something")
        audio = r.listen(source)

    data =''
    try:
        data = r.recognize_google(audio)
        print('You said: ' +data )
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand the audio, unknown error ')
    except sr.RequestError as e:
        print('Request result from Google Speech Recognition service error')
    return data

#This function returns our assistant's response in mp3 format
def assisstantResponse(text):
    print(text)
    myobj = gTTS(text = text, lang='en', slow=False)
    myobj.save('assistant_response.mp3')
    os.system('start assistant_response.mp3')

#Here we have wake words.
# With this wake words our Voice Assistant will response us
def wakeWord(text):
    WAKE_WORDS = ('jarvis','jarvi','javis', 'jervis', 'garvis','jar vis')
    text = text.lower()

    for phrases in WAKE_WORDS:
        if phrases in text:
            return True

    return False

#Our function to take current date and time
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_name =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                 'September','October','November', 'December']
    ordinalNumber =['1st', '2nd', '3rd','4th','5th','6th','7th','8th','9th','10th',
                    '11th','12th','13th','14th','15th','16th','17th','18th','19th','20th',
                    '21th','22th','23th','24th','25th','26th','27th','28th','29th','30th','31th']

    return 'Today is '+ weekday+' '+ month_name[monthNum-1]+ ' the '+ordinalNumber[dayNum-1]+'.'

#If one of this greeting inputs has been told
#Voice Assistant return us one of the greeting response
def greeting(text):
    GREETING_INPUTS = ['hey', 'hi', 'hola','greetings',"What's up",'Sup', 'wassup', 'hello','hey there' ]
    GREETING_RESPONSES = ['howdy', 'whats good','hello', 'hey there']

    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)+ '.'
    return ''

#Here we get the person' information and
#we can also play music on Youtube
def getPerson(text):
    wordList = text.split()
    for i in range(0, len(wordList)):
        if i+3 <= len(wordList) - 1 and ((wordList[i].lower() =='who' and wordList[i+1].lower() =='is')or(wordList[i].lower() =='play' and wordList[i+1]=='music' )):
            return wordList[i+2]+ ' '+ wordList[i+3]

while True:
    text =recordAudio()
    response =''

    if (wakeWord(text)==True):
        response = response + greeting(text)

        if('date' in text):
            get_date = getDate()
            response = response +' '+get_date

        if('time' in text):
            now = datetime.datetime.now()
            meridiem =''
            if now.hour >=12:
                meridiem = 'pm'
                hour = now.hour
            else:
                meridiem='am'
                hour = now.hour
            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)
            response = response+ ' '+'It is '+str(hour)+':'+ minute+' '+ meridiem+' .'

        if('who is' in text):
            person =getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response +' ' + wiki

        # We can search anything we want on Google with these code-block
        if ('search' in text):
            try:
                    kelimeler = text.split()
                    endeks = kelimeler.index("search")
                    search = ""
                    i = endeks + 1
                    while i < len(kelimeler):
                        search += " " + kelimeler[i]
                        i += 1
                    webbrowser.open(f"https://google.com.tr/search?q={search}")
                    search = wikipedia.summary(search, sentences=2)
                    response = response +' '+ search
            except:
                empty ="You did not search anything but ı open the google for you"
                response = response + ' '+ empty


        if ('play' in text):
            kelimeler = text.split()
            endeks = kelimeler.index("play")
            play = ""
            i = endeks + 1
            while i < len(kelimeler):
                play += " " + kelimeler[i]
                i += 1
            webbrowser.open(f"https://www.youtube.com/results?search_query={play}")
            response =response+'Good choice '+play+''

        # with these word our Voice Assistant will not listen us for a 1 minute
        if "don't listen" in text or "stop listening" in text:
            response = response + "I am ready after 1 minute waiting"
            time.sleep(60)

        #Voice Assistant will tell us a joke
        if ("joke" in text):
            response = response+ pyjokes.get_joke()

        if("how are you" in text):
            response = response + "I am fine.Thank you. How are you Sir"

        if("fine" in text or "good" in text):
            response = response +"It is good to know that your fine"

        if("thank you" in text):
            response = response + "You are welcome"

        # With these code-blocks we can do shutdown, restart or log off operations on computer
        if 'shutdown system' in text:
            response = response+"Hold On a Sec ! Your system is on its way to shut down"
            subprocess.call('shutdown / p /f')
        elif "restart" in text:
            subprocess.call(["shutdown", "/r"])
        elif "log off" in text or "sign out" in text:
            response = response+ "Make sure all the application are closed before sign-out"
            #time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        # Halt the Voice Assistant
        if 'exit' in text:
            exit()
        assisstantResponse(response)
