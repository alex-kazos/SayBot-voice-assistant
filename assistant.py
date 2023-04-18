import speech_recognition as sr
import pyttsx3
import pywhatkit
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

# initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# define function to speak a response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# define function to listen to user's voice command
def get_command():
    # initialize recognizer and microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        # adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # listen for user's voice command
        audio = r.listen(source)
        try:
            # recognize speech using Google Speech Recognition
            command = r.recognize_google(audio)
            print("You said: " + command)
        except sr.UnknownValueError:
            speak("Sorry, I did not understand.")
            command = ""
        return command.lower()

class CreateBot:

    def __init__(self,system_prompt):

        self.system = system_prompt
        self.messages = [{'role':'system','content':system_prompt}]

    # def chat(self):
    def chat(self,command):

        # print('To terminate the conversation, type "END"')
        # question = ''

        question = command
        n = 1
        exit_var = False
        while "exit" not in question or "stop" not in question or "play" not in question:

            
            
            if question == command and n != 1:
                command = get_command()
            
            question = command
            
            if "exit" in command or "stop" in question:
                exit_var = True
            elif "play" in command:
                break

        # while question != 'END':

            # user input
            # question = input("")
            print('\n')
            # ad user input to messages
            self.messages.append({'role':'user','content':question})
            #grab response
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages = self.messages,
                temperature=0.1,
                # max_tokens=512,
                max_tokens=126,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.2
            )
            #grab response 
            content = response['choices'][0]['message']['content']
            # print('\n')
            print(content)
            speak(content)
            # print('\n')
            n=2
            

            self.messages.append({'role':'assistant','content':content})

        return exit_var,command

            



    # define function to execute voice commands
def run_assistant(chat_bot):
    command = get_command()
    # print(command)
    if "play" in command:
        song = command.split("play ")[1]
        speak("Playing " + song + " on YouTube.")
        pywhatkit.playonyt(song)

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        return False

    else:
        exit_var,command = chat_bot.chat(command)
        if exit_var == True:
            return False
        else:
            song = command.split("play ")[1]
            speak("Playing " + song + " on YouTube.")
            pywhatkit.playonyt(song)
    return True

# main program loop
AI_ASSISTANT = CreateBot(system_prompt="You are a helpful AI Assistant that only answers if its 100% certaint")
speak("Hello! I'm Say Bot How can I assist you?")
print("Hello! I'm SayBot How can I assist you?")
while True:
    if not run_assistant(AI_ASSISTANT):
        break