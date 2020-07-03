import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia
import webbrowser
import os
import pyfirmata
import time

board = pyfirmata.Arduino('COM3')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[3].id)
engine.setProperty('voice', voices[3].id)

def speak(audio):
     engine.say(audio)
     engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=5 and hour<12:
        speak ("Good Morning sir..")
        speak("how may I help u.... ?")      

    elif hour>=12 and hour<16:
        speak ("Good Afternoon sir...")  
        speak("how may I help u.... ?")       

    elif hour>=16 and hour<19:
        speak ("Good evening sir...") 
        speak("how may I help u....?")               

    else:
        speak("u need to sleep sir,its Night")  


def takecommand():
    #it takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning...")
        r.pause_threshold = 0.5
        audio = r.listen(source)  
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
      #  speak(query)
        print(f"User said: {query}\n")

    except Exception as e:
          print("say that again please....")
          speak("dot")
          return "None" 
    return query    

if __name__ == "__main__":  
     while True:
        query = takecommand().lower()#converts in lower case
        #logic for executing tasks based on query
        if 'wikipedia' in query:
           speak('searching wikipedia...')
           query = query.replace("wikipedia","")
           results = wikipedia.summary(query,sentences=2)
           speak("According to wikipedia")
           print(results)
           speak(results)

        elif 'charlotte' in query:
            wishMe()   

        elif 'youtube' in query:   
            speak('opening youtube...')
            webbrowser.open("youtube.com")

        elif 'google' in query:
            webbrowser.open("google.com")    
        
        elif 'play music' in query:
            speak('what do you want me to play sir ')  
            
        elif 'play one of my favorites' in query:
            speak('I think I know what to play ')  
            music_dir = 'E:\\python\\Eva\\song'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
           # exit()

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("its %H hour %M minutes and %S seconds")
            speak(f"Sir, the time is{strTime}")    

        elif 'open code' in query:
            codePath = "C:\\Users\\admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'blue light on' in query:
            board.digital[10].write(1)

        elif 'blue light off' in query:
            board.digital[10].write(0)

        elif 'green light on' in query:
            board.digital[2].write(1)

        elif "green light off" in query:
            board.digital[2].write(0)

        elif "turn off both" in query:
            board.digital[2].write(0)  
            board.digital[10].write(0)    

        elif "who are you" in query:
            speak('I am charlotte , a program created by u.... ,and your AI personal Assistant .... ')    

        elif "introduce yourself" in query:
            speak('I am charlotte , a program created by u.... ,and your AI personal Assistant .... ')    

        elif "stop" in query:
            exit()

        elif 'sleep' in query:
            exit()
        elif 'terminate' in query:
            exit()

