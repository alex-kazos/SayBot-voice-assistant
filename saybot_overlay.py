import tkinter as tk
from tkinter import font
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk
import threading

class SayBotOverlay:
    def __init__(self, master):
        self.master = master
        self.master.title("SayBot Overlay")
        self.master.attributes('-alpha', 0.9)  # Set window transparency
        self.master.attributes('-topmost', True)  # Keep window on top
        self.master.overrideredirect(True)  # Remove window decorations

        # Set window size and position
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 300
        window_height = 400
        x = screen_width - window_width - 20
        y = screen_height - window_height - 60
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create a frame for the content
        self.frame = tk.Frame(self.master, bg='#1E1E1E')
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Load and display the assistant icon
        self.icon = Image.open("assistant_icon.png")  # Replace with your icon
        self.icon = self.icon.resize((100, 100), Image.LANCZOS)
        self.icon = ImageTk.PhotoImage(self.icon)
        self.icon_label = tk.Label(self.frame, image=self.icon, bg='#1E1E1E')
        self.icon_label.pack(pady=20)

        # Create a text area for displaying responses
        self.response_font = font.Font(family="Helvetica", size=12)
        self.response_area = tk.Text(self.frame, wrap=tk.WORD, bg='#2E2E2E', fg='white', font=self.response_font, height=10)
        self.response_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a button to start listening
        self.listen_button = tk.Button(self.frame, text="Listen", command=self.start_listening, bg='#4CAF50', fg='white')
        self.listen_button.pack(pady=10)

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Changed to index 0 for a different voice

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()

    def start_listening(self):
        self.update_response("Listening...")
        threading.Thread(target=self.listen_for_command).start()

    def listen_for_command(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            self.update_response(f"You said: {command}")
            self.process_command(command)
        except sr.UnknownValueError:
            self.update_response("Sorry, I didn't understand that.")
        except sr.RequestError:
            self.update_response("Sorry, there was an error processing your request.")

    def process_command(self, command):
        # Here, you can integrate your existing SayBot logic
        # For now, we'll just echo the command
        response = f"Processing command: {command}"
        self.update_response(response)
        self.speak(response)

    def update_response(self, message):
        self.response_area.delete(1.0, tk.END)
        self.response_area.insert(tk.END, message)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = SayBotOverlay(root)
    root.mainloop()
