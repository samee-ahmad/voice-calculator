import speech_recognition as sr
import pyttsx3
import re
from sympy import sympify

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Variables to hold memory and previous result
memory = None

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to perform advanced arithmetic calculations
def calculate(expression):
    try:
        # Use sympy to evaluate complex expressions safely
        result = sympify(expression)
        return result
    except Exception as e:
        return "Error"

# Function to take voice input
def take_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            voice_text = recognizer.recognize_google(audio)  # Use Google API
            print(f"User said: {voice_text}")
            return voice_text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Network error. Please check your connection.")
            return None

# Function to display help
def display_help():
    help_text = (
        "You can ask me to perform calculations like:\n"
        "1. What is 5 plus 3?\n"
        "2. Calculate 10 divided by 2.\n"
        "3. What is the square root of 16?\n"
        "You can also say 'memory' to recall the last result or 'clear memory' to reset it.\n"
        "To exit, say 'exit' or 'quit'."
    )
    speak(help_text)

# Main function to run the calculator
def voice_calculator():
    global memory
    speak("Welcome to the Voice Command Calculator. You can say 'help' for instructions.")

    while True:
        # Take voice input
        voice_input = take_voice_input()

        if voice_input:
            voice_input = voice_input.lower()

            if "exit" in voice_input or "quit" in voice_input:
                speak("Goodbye!")
                break

            elif "help" in voice_input:
                display_help()
                continue

            elif "memory" in voice_input:
                if memory is not None:
                    result_message = f"The last stored result is {memory}"
                    speak(result_message)
                else:
                    speak("No results stored in memory.")
                continue

            elif "clear memory" in voice_input:
                memory = None
                speak("Memory cleared.")
                continue

            # Calculate the expression
            result = calculate(voice_input)
            print(f"Result: {result}")
            speak(f"The result is {result}")

            # Store the result in memory
            memory = result
        else:
            speak("Please repeat your command.")

# Run the voice calculator
voice_calculator()
