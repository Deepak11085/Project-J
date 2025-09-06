import speech_recognition as sr
import pyttsx3
from gpt4all import GPT4All
import os

# 1. Initialize speech engine (initial setup)

# 2. Function to speak
def speak(text):
    """Converts a given text string into speech."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()

# 3. Function to listen
def listen():
    """Listens for a voice command and returns the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f" Sir said: {text}")
        return text
    except sr.UnknownValueError:
        print(" Sorry Sir, I could not understand.")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Could not request results from Google Speech Recognition service; {e}")
        return ""
        
# 4. Initialize GPT4All model (offline)
model_file_name = "qwen2-1_5b-instruct-q4_0.gguf"
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, model_file_name)

if not os.path.exists(model_path):
    print(f" Error: Model file not found at {model_path}")
    print("Please make sure the model is in the same directory as this script.")
    exit()
else:
    print(f"✅ Found model file at {model_path}")
    try:
        model = GPT4All(
            model_name=model_file_name,
            model_path=script_dir,
            allow_download=False
        )
    except Exception as e:
        print(f"An error occurred while initializing the model: {e}")
        print("This may be due to a corrupted file or an incompatible model format.")
        exit()

# 5. Function to ask GPT4All
# 5. Function to ask GPT4All
def ask_chatgpt(prompt):
    """Sends the user's prompt to the local GPT4All model and returns the response."""
    formatted_prompt = f"You are a helpful assistant named Jarvis. {prompt}"
    
    try:
        response = model.generate(
            formatted_prompt,
            max_tokens=50,  # <-- Add this line to limit the response
            temp=0.7
        )
        return response
    except Exception as e:
        print(f"An error occurred while generating a response: {e}")
        return "I'm sorry, an error occurred while processing your request."

# 6. Main loop
def jarvis():
    """The main loop for the voice assistant."""
    speak("Hello Sir, I am Jarvis. How can I help you?")
    while True:
        query = listen()
        if "exit" in query.lower() or "quit" in query.lower() or "stop" in query.lower() or "kill it" in query.lower():
            speak("Goodbye Sir!")
            break
        if query:
            print(" Jarvis is thinking...")
            answer = ask_chatgpt(query)
            print(f" Jarvis: {answer}")
            speak(answer)

if __name__ == "__main__":
    jarvis()