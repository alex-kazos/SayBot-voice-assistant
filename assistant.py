## Libraries

import pandas as pd
import subprocess
import pyttsx3
import requests
from gnews import GNews
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import webbrowser
import os
import shutil
import random
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import openai
import os
import pywhatkit

## API Set Up 

openai.api_key = os.getenv('OPENAI_API_KEY')
# find your OpenAI API key here https://platform.openai.com/
# openai.api_key = input('give your OpenAi API Key:')
# find yourwheaterAPI_key key here https://www.weatherapi.com/
wheaterAPI_key = os.getenv('WHEATHER_API_KEY')
# wheaterAPI_key = input('give your WheaterAPI_key Key:')

## Functions
print('Initializing...')

# initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# fetching NEWS
google_news = GNews()
top_news = google_news.get_top_news()
news_df = pd.DataFrame(top_news)

# clean news
def getTitle(title):
    try:
        return title.split('-')[0]
    except:
        return title
    

# define function to speak a response
def speak(text):
    engine.say(text)
    engine.runAndWait()

def greetings():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		print("Good Morning!")
		speak("Good Morning!")

	elif hour>= 12 and hour<18:
		print("Good Afternoon!")
		speak("Good Afternoon!")

	else:
		print("Good Evening!")
		speak("Good Evening!")

	print("I'm SayBot you personal Generative Ai Vitrual Assistant, how can I help you?")
	speak("I'm SayBot you personal Generative Ai Vitrual Assistant, how can I help you?")

# define function to listen to user's voice command
def takeCommand():
	# initialize recognizer and microphone
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold = 1
		# adjust for ambient noise
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)

	try:
		command = r.recognize_google(audio, language ='en-in')
		print(f"You said: {command}")

	except Exception as e:
		# print(e)
		print("Sorry, I did not understand.")
		speak("Sorry, I did not understand.")
		return "None"
	return command

def get_City(query,x):
    if f"weather like {x}" in query:
        city_name = query.split('like in')[1]
    elif f"weather {x}" in query:
        city_name = query.split('weather in')[1]
    return city_name

def getLocation(query):
	try:
		location = get_City(query,'in')
	except:
		pass
	try:
		location =get_City(query,'on')
	except:
		pass
	try:
		location = get_City(query,'at')
	except:
		pass

	return location

def randomNumber(numb):
    # Generate a random string of 5 digits
    return ''.join([str(random.randint(0, 9)) for _ in range(numb)])

def save_image(image_url,file_name):
    image_res= requests.get(image_url,stream=True)
    if image_res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(image_res.raw,f)
    else:
        print('ERROR LOADING IMAGE')
    
    return image_res.status_code

news_df['title'] = news_df['title'].apply(getTitle)

# creation of the Bot
class ChatBot:

    def __init__(self,system_prompt):

        self.system = system_prompt
        self.messages = [{'role':'system','content':system_prompt}]

    # def chat(self):
    def chat(self,query):

        question = query
        n = 1
        exit_var = False

        keywords = ['exit','stop', 'open youtube', 'open google', 'play', 'search', 'news', 'lock device', 'shutdown', 'empty recycle bin', 'where is', 'take a photo', 'restart', 'write a note', 'show note', 'weather', 'exit', 'bye', 'create', 'paint', 'image']

        while any(keyword not in question for keyword in keywords):
            
            if question == query and n != 1:
                query = takeCommand()
            
            question = query
            
            if "exit" in query or "stop" in question:
                exit_var = True
            elif any(keyword in query for keyword in keywords):
                break

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
            print(content)
            speak(content)
            n=2
            

            self.messages.append({'role':'assistant','content':content})

        return exit_var,query

## Assistant Script

if __name__ == '__main__':
	clear = lambda: os.system('cls')
	
	# This Function will clean any
	# command before execution of this python file
	clear()
	greetings()
	
	# setting up chatbot
	sayBot = ChatBot(system_prompt="You are Say Bot, a helpful AI Assistant that only answers if its 100% certaint")
		
	while True:
		
		query = takeCommand().lower()
		
		if 'open youtube' in query:
			print("Opening Youtube\n")
			speak("Opening Youtube\n")
			webbrowser.open("youtube.com")

		elif 'open google' in query:
			print("Opening Google\n")
			speak("Opening Google\n")
			webbrowser.open("google.com")


		elif "play" in query:
			song = query.split("play ")[1]
			print(f"Playing {song} on YouTube.")
			speak(f"Playing {song} on YouTube.")
			pywhatkit.playonyt(song)

		elif 'the time' in query:
			strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
			print(f"The time is {strTime}")
			speak(f"The time is {strTime}")
			
		elif 'joke' in query:
			joke=pyjokes.get_joke()
			print(joke)
			speak(joke)
			

		elif 'search' in query:
			query = query.replace("search", "")	
			print(f'Searching...')
			webbrowser.open(query)


		elif "who are you" in query:
			print("I am Say Bot an AI Voice Assistant")
			speak("I am Say Bot an AI Voice Assistant")

		elif 'news' in query:
			news = True
			print('Here are some News:')
			speak('Here are some News:')
			while news:
				random = news_df.sample(5).reset_index()
				for i in range(len(random)):
					print(f"{i+1}. {random['title'][i]}.")
					speak(f"{i+1}. {random['title'][i]}.")
					
				print('Do you want to more details in any of this news ?') 
				speak('Do you want to more details in any of this news ?') 
				print('If so which? Or do you want me to refresh?')
				speak('If so which? Or do you want me to refresh?')
				try:
					query = takeCommand().lower()
					
					if '1' in query:
						response = openai.Completion.create(engine='text-davinci-003',
												prompt=f"summarize this news with a more causal tone: {random['description'][0]}",
												max_tokens=512,
												temperature=0.7)
						print(response['choices'][0]['text'])
						speak(response['choices'][0]['text'])
						news = False
					elif '2' in query:
						response = openai.Completion.create(engine='text-davinci-003',
												prompt=f"summarize this news with a more causal tone: {random['description'][1]}",
												max_tokens=512,
												temperature=0.7)
						print(response['choices'][0]['text'])
						speak(response['choices'][0]['text'])
						news = False
					elif '3' in query:
						response = openai.Completion.create(engine='text-davinci-003',
												prompt=f"summarize this news with a more causal tone: {random['description'][2]}",
												max_tokens=512,
												temperature=0.7)
						print(response['choices'][0]['text'])
						speak(response['choices'][0]['text'])
						news = False
					elif '4' in query:
						response = openai.Completion.create(engine='text-davinci-003',
												prompt=f"summarize this news with a more causal tone: {random['description'][3]}",
												max_tokens=512,
												temperature=0.7)
						print(response['choices'][0]['text'])
						speak(response['choices'][0]['text'])
						news = False
					elif '5' in query:
						response = openai.Completion.create(engine='text-davinci-003',
												prompt=f"summarize this news with a more causal tone: {random['description'][4]}",
												max_tokens=512,
												temperature=0.7)
						print(response['choices'][0]['text'])
						speak(response['choices'][0]['text'])
						news = False
					elif 'refresh' in query:
						pass
					elif 'no' in query:
						break

				except:
					break
		
		elif 'lock device' in query:
				print("locking the device")
				speak("locking the device")
				ctypes.windll.user32.LockWorkStation()

		elif 'shutdown system' in query:
				print("Your system is on its way to shut down")
				speak("Your system is on its way to shut down")
				subprocess.call('shutdown / p /f')

		elif "restart" in query:
			print("Your system is on its way to be restared")
			speak("Your system is on its way to be restared")
			subprocess.call(["shutdown", "/r"])
				
		elif 'empty recycle bin' in query:
			winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
			print("Recycle Bin is now empty!")
			speak("Recycle Bin is now empty!")


		elif "where is" in query:
			query = query.split("where is")[1]
			location = query
			webbrowser.open("https://www.google.com/maps/place/" + location )

		elif "take a photo" in query:
			print("Smile for the camera!")
			speak("Smile for the camera!")
			Image_id =randomNumber(numb=5)
			ec.capture(0, f"sayBot_{Image_id}" ,"img.jpg")
			

		elif "write a note" in query:
			print("What should I write?")
			speak("What should I write?")
			note = takeCommand()
			file = open('sayBot_Notes.txt', 'w')
			print("Should i include date and time")
			speak("Should i include date and time")
			snfm = takeCommand()
			if 'yes' in snfm or 'sure' in snfm:
				strTime = datetime.datetime.now().strftime("% H:% M:% S")
				file.write(strTime)
				file.write(" :- ")
				file.write(note)
			else:
				file.write(note)
		
		elif "show note" in query:
			print("Opening Notes")
			speak("Opening Notes")
			file = open("sayBot_Notes.txt", "r")

		elif "weather" in query:
			location = getLocation(query)
			
			url = f"http://api.weatherapi.com/v1/current.json?key={wheaterAPI_key}&q={location}&aqi=no"

			response = requests.get(url)

			if response.status_code == 200:
				data = response.json()
				
				time = data["location"]["localtime"]
				location = data["location"]["name"]
				current_temperature = data["current"]["temp_c"]
				country = data["location"]["country"]
				condition = data["current"]["condition"]["text"]
				wind_speed = data["current"]["wind_kph"]
				wind_dir = data["current"]["wind_dir"]
				feels_like = data["current"]["feelslike_c"]
				
				
				print(f"Time: {time}")
				print(f"Location: {location}, {country}")
				print(f"Current temperature is: {current_temperature}°C")
				print(f"Condition: {condition}")
				print(f"Wind Speed: {wind_speed} kph, Wind Direction: {wind_dir}")
				print(f"Feels Like: {feels_like}°C")

				speak(f"Time: {time}")
				speak(f"Location: {location}, {country}")
				speak(f"Current temperature is: {current_temperature}°C")
				speak(f"Condition: {condition}")
				speak(f"Wind Speed: {wind_speed} kph, Wind Direction: {wind_dir}")
				speak(f"Feels Like: {feels_like}°C")
			else:
				print("Failed to get weather data")
				speak("Failed to get weather data")

		elif 'create' in query or 'paint' in query or 'image' in query:
			prompt = query 
			print('What resolution do you want?')
			print('Low, Medium or High?')
			speak('What resolution do you want?')
			speak('Low, Medium or High?')
			input = takeCommand().lower()
			if 'low' in input:
				size = "1024x1024"
			elif 'medium' in input:
				size = '512x512'
			elif 'high' in input:
				size = "1024x1024"

			print('What artstyle type do you want?\ni.e. Digital Art')
			speak('What artstyle type do you want?')
			art_style = takeCommand().lower()
			Image_response = openai.Image.create(prompt=f'Generate an image of : {prompt},{art_style}',
                                     n=1,
                                     size=size)
			image_response_url = Image_response['data'][0]['url']

			Image_id =randomNumber(numb=5)
			save_image(image_response_url,f'sayBot_GenerativeImage_{Image_id}.png')

			print('Image saved Successfully')
			speak('Image saved Successfully')

		elif "exit" in query or "bye" in query:
			print('Goodbye!')
			speak("Goodbye!")
			break

		else:
			exit_var,query = sayBot.chat(query=query)
			if exit_var == True:
				break 
			elif 'open youtube' in query:
				speak("Here you go to Youtube\n")
				webbrowser.open("youtube.com")

			elif 'open google' in query:
				speak("Here you go to Google\n")
				webbrowser.open("google.com")


			elif "play" in query:
				song = query.split("play ")[1]
				speak("Playing " + song + " on YouTube.")
				pywhatkit.playonyt(song)

			elif 'the time' in query:
				strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
				print(f"The time is {strTime}")
				speak(f"The time is {strTime}")
			
			elif 'joke' in query:
				speak(pyjokes.get_joke())
				

			elif 'search' in query:
				
				query = query.replace("search", "")
				query = query.replace("play", "")		
				webbrowser.open(query)


			elif 'news' in query:
				news = True
				print('Here are some News:')
				speak('Here are some News:')
				while news:
					random = news_df.sample(5).reset_index()
					for i in range(len(random)):
						print(f"{i+1}. {random['title'][i]}.")
						speak(f"{i+1}. {random['title'][i]}.")
						
					print('Do you want to more details in any of this news ?') 
					speak('Do you want to more details in any of this news ?') 
					print('If so which? Or do you want me to refresh?')
					speak('If so which? Or do you want me to refresh?')
					try:
						query = takeCommand().lower()
						
						if '1' in query:
							response = openai.Completion.create(engine='text-davinci-003',
													prompt=f"summarize this news with a more causal tone: {random['description'][0]}",
													max_tokens=512,
													temperature=0.7)
							print(response['choices'][0]['text'])
							speak(response['choices'][0]['text'])
							news = False
						elif '2' in query:
							response = openai.Completion.create(engine='text-davinci-003',
													prompt=f"summarize this news with a more causal tone: {random['description'][1]}",
													max_tokens=512,
													temperature=0.7)
							print(response['choices'][0]['text'])
							speak(response['choices'][0]['text'])
							news = False
						elif '3' in query:
							response = openai.Completion.create(engine='text-davinci-003',
													prompt=f"summarize this news with a more causal tone: {random['description'][2]}",
													max_tokens=512,
													temperature=0.7)
							print(response['choices'][0]['text'])
							speak(response['choices'][0]['text'])
							news = False
						elif '4' in query:
							response = openai.Completion.create(engine='text-davinci-003',
													prompt=f"summarize this news with a more causal tone: {random['description'][3]}",
													max_tokens=512,
													temperature=0.7)
							print(response['choices'][0]['text'])
							speak(response['choices'][0]['text'])
							news = False
						elif '5' in query:
							response = openai.Completion.create(engine='text-davinci-003',
													prompt=f"summarize this news with a more causal tone: {random['description'][4]}",
													max_tokens=512,
													temperature=0.7)
							print(response['choices'][0]['text'])
							speak(response['choices'][0]['text'])
							news = False
						elif 'refresh' in query:
							pass
						elif 'no' in query:
							break

					except:
						break
			
			elif 'lock device' in query:
					print("locking the device")
					speak("locking the device")
					ctypes.windll.user32.LockWorkStation()

			elif 'shutdown system' in query:
					print("Your system is on its way to shut down")
					speak("Your system is on its way to shut down")
					subprocess.call('shutdown / p /f')

			elif "restart" in query:
				print("Your system is on its way to be restared")
				speak("Your system is on its way to be restared")
				subprocess.call(["shutdown", "/r"])
					
			elif 'empty recycle bin' in query:
				winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
				print("Recycle Bin is now empty!")
				speak("Recycle Bin is now empty!")


			elif "where is" in query:
				query = query.split("where is")[1]
				location = query
				webbrowser.open("https://www.google.com/maps/place/" + location )

			elif "take a photo" in query:
				print("Smile for the camera!")
				speak("Smile for the camera!")
				Image_id =randomNumber(numb=5)
				ec.capture(0, f"sayBot_{Image_id}" ,"img.jpg")
				

			elif "write a note" in query:
				speak("What should i write?")
				note = takeCommand()
				file = open('sayBot_Notes.txt', 'w')
				speak("Should i include date and time")
				snfm = takeCommand()
				if 'yes' in snfm or 'sure' in snfm:
					strTime = datetime.datetime.now().strftime("% H:% M:% S")
					file.write(strTime)
					file.write(" :- ")
					file.write(note)
				else:
					file.write(note)
			
			elif "show note" in query:
				speak("Showing Notes")
				file = open("sayBot_Notes.txt", "r")
				print(file.read())
				speak(file.read(6))

			elif "weather" in query:
				location = getLocation(query)

				url = f"http://api.weatherapi.com/v1/current.json?key={wheaterAPI_key}&q={location}&aqi=no"
				response = requests.get(url)

				if response.status_code == 200:
					data = response.json()
					
					time = data["location"]["localtime"]
					location = data["location"]["name"]
					current_temperature = data["current"]["temp_c"]
					country = data["location"]["country"]
					condition = data["current"]["condition"]["text"]
					wind_speed = data["current"]["wind_kph"]
					wind_dir = data["current"]["wind_dir"]
					feels_like = data["current"]["feelslike_c"]
					
					
					print(f"Time: {time}")
					print(f"Location: {location}, {country}")
					print(f"Current temperature is: {current_temperature}°C")
					print(f"Condition: {condition}")
					print(f"Wind Speed: {wind_speed} kph, Wind Direction: {wind_dir}")
					print(f"Feels Like: {feels_like}°C")

					speak(f"Time: {time}")
					speak(f"Location: {location}, {country}")
					speak(f"Current temperature is: {current_temperature}°C")
					speak(f"Condition: {condition}")
					speak(f"Wind Speed: {wind_speed} kph, Wind Direction: {wind_dir}")
					speak(f"Feels Like: {feels_like}°C")
				else:
					speak("Failed to get weather data")
					print("Failed to get weather data")

			elif 'create' in query or 'paint' in query or 'image' in query:
				prompt = query 
				print('What resolution do you want?')
				print('Low, Medium or High?')
				speak('What resolution do you want?')
				speak('Low, Medium or High?')
				input = takeCommand().lower()
				if 'low' in input:
					size = "1024x1024"
				elif 'medium' in input:
					size = '512x512'
				elif 'high' in input:
					size = "1024x1024"

				print('What artstyle type do you want?\ni.e. Digital Art')
				speak('What artstyle type do you want?')
				art_style = takeCommand().lower()
				Image_response = openai.Image.create(prompt=f'Generate an image of : {prompt},{art_style}',
										n=1,
										size=size)
				image_response_url = Image_response['data'][0]['url']

				Image_id =randomNumber(numb=5)
				save_image(image_response_url,f'sayBot_GenerativeImage_{Image_id}.png')
				print('Image saved Successfully')
				speak('Image saved Successfully')




        
        