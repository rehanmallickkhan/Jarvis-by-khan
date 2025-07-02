import openai
from keys import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pyjokes
import os
import webbrowser
import random
import requests

# Init engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Female voice (optional)

# Set OpenAI key
openai.api_key = "sk-..."

# Personality mode
current_personality = "helpful assistant"

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def run_jarvis():
    print("🔧 run_jarvis() started")
    ...

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print("You said:", query)
        return query.lower()
    except:
        speak("Sorry, could you say that again?")
        return "none"

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning, sir.")
    elif hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")
    speak("I am JARVIS. Fully online and operational.")

def tell_time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}")

def tell_date():
    date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {date}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(result)
    except:
        speak("Sorry, I couldn't find anything.")

def get_weather(city="Delhi"):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp}°C with {desc}")
    except:
        speak("Unable to fetch weather data.")

def open_software_or_website(command):
    if "file explorer" in command:
        os.system("explorer")
        speak("Opening File Explorer.")
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Launching YouTube.")
    elif "google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "chrome" in command:
        try:
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
            speak("Launching Chrome.")
        except:
            speak("Chrome path not found.")
    else:
        speak("That function is not yet available.")

def respond_like_jarvis():
    lines = [
        "Online and functioning perfectly.",
        "System diagnostics complete. Everything’s green.",
        "Standing by.",
        "I await your next command.",
        "JARVIS ready."
    ]
    speak(random.choice(lines))

def ask_chatgpt(prompt):
    personalities = {
        "helpful assistant": "You are a helpful and intelligent assistant named JARVIS.",
        "sarcastic": "You are JARVIS, an AI with witty and sarcastic comebacks.",
        "flirty": "You are JARVIS, a flirty and charming AI who playfully interacts with the user."
    }
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": personalities[current_personality]},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except:
        return "Sorry, I couldn't reach the AI servers."

def run_jarvis():
    global current_personality
    wish_me()

    while True:
        command = take_command()

        if command == "none":
            continue

        elif "time" in command:
            tell_time()

        elif "date" in command:
            tell_date()

        elif "joke" in command:
            tell_joke()

        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            search_wikipedia(topic)

        elif "weather" in command:
            get_weather("Delhi")

        elif "open" in command:
            open_software_or_website(command)

        elif "how are you" in command:
            respond_like_jarvis()

        elif "activate sarcastic mode" in command:
            current_personality = "sarcastic"
            speak("Sarcastic mode activated. Prepare for some sass.")

        elif "activate flirty mode" in command:
            current_personality = "flirty"
            speak("Flirty mode on. You're looking smart today.")

        elif "deactivate mode" in command or "back to normal" in command:
            current_personality = "helpful assistant"
            speak("Back to default mode, sir.")

        elif "jarvis" in command or "ai" in command:
            speak("What would you like to ask me?")
            prompt = take_command()
            reply = ask_chatgpt(prompt)
            speak(reply)

        elif "exit" in command or "goodbye" in command or "shutdown" in command:
            speak("Shutting down systems. Goodbye, sir.")
            break

        else:
            speak("I didn't understand that command yet, but I'm learning.")

# ✅ This should be outside of all functions
if __name__ == "__main__":
    run_jarvis()
