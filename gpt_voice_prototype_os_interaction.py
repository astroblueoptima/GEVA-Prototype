
import speech_recognition as sr
from gtts import gTTS
import os

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Dictionary to store user-defined commands
user_commands = {}

def get_voice_input():
    """Capture voice input from user and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio_data = recognizer.listen(source)
        try:
            # Recognize the content and convert it to text
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "API unavailable."

def gpt_response(text):
    """Generate a response using GPT or predefined commands."""
    
    # Check if the text matches any user-defined commands
    for command, response in user_commands.items():
        if command in text:
            return response
    
    # OS-interaction commands (simulated)
    if "open" in text and "for me" in text:
        app_name = text.split("open")[1].split("for me")[0].strip()
        return f"Opening {app_name}..."
    elif "search my files for" in text:
        keyword = text.split("search my files for")[1].strip()
        return f"Searching files for {keyword}..."
    elif "adjust my screen brightness to" in text:
        level = text.split("adjust my screen brightness to")[1].strip("%").strip()
        return f"Adjusting screen brightness to {level}%..."
    elif "set a timer for" in text:
        duration = text.split("set a timer for")[1].strip("minutes").strip()
        return f"Setting a timer for {duration} minutes..."
    elif "tell me my battery percentage" in text:
        return "Your battery is currently at 75%."  # Just a simulated response
    
    # High-value commands
    if "summarize a topic for me" in text:
        return "Sure! The topic you mentioned is about..."
    elif "translate this to" in text:
        return "Translation: [Translated Text]"
    elif "help me brainstorm ideas about" in text:
        return "Here are some ideas about the topic..."
    elif "generate a short story about" in text:
        return "Once upon a time in a world where..."
    elif "explain the concept of" in text and "to a five-year-old" in text:
        return "Alright! Imagine you have a toy..."
    
    # If the text starts with 'Teach command:', store the command and its response
    if text.startswith("Teach command:"):
        parts = text.split("you do")
        if len(parts) == 2:
            command = parts[0].replace("Teach command: When I say", "").strip()
            response = parts[1].strip()
            user_commands[command] = response
            return f"Got it! I've learned the command: When you say '{command}', I'll respond with '{response}'."
    
    # Default GPT-like response
    return f"I heard you say: {text}"

def text_to_voice(text):
    """Convert text to voice and play it."""
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    while True:
        # Get voice input
        user_input = get_voice_input()
        
        # Get GPT response
        response = gpt_response(user_input)
        
        # Convert response to voice and play
        text_to_voice(response)

        # Check for exit command
        if "exit" in user_input.lower():
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
