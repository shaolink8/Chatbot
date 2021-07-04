import aiml
import json
import requests
import wikipedia
import pyttsx3
import speech_recognition as sr

speechEngine = pyttsx3.init()
r = sr.Recognizer()
mic = sr.Microphone()

kernel = aiml.Kernel()
kernel.learn("learn.xml")

#weather codes
def getWeather(city):
    appid = "f4b61b8e5967d5867a77b495f8055ca3"
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?appid="+appid+"&q="+city)
    jsonResponse = response.json()
    return jsonResponse

def getJoke():
    response = requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'})
    return json.loads(response.text)

def getWiki(keyword):
    return wikipedia.summary(keyword, sentences=2)

def getWikiPage(page):
    return wikipedia.page(page).content

def voiceResponse(text):
    print(text)
    speechEngine.say(text)
    speechEngine.runAndWait()

while True:
    try:
        print ("\nSpeak..")
        with mic as source:
            audio = r.listen(source)
            print ("\nProcessing what you just said..")
            voiceText = r.recognize_google(audio)
            print ("\nFinding a suitable response\n")
            response = kernel.respond(voiceText)
            responseParts = response.split()
            if len(responseParts) > 0:
                if responseParts[0] == "weather":
                    weatherData = getWeather(responseParts[1])
                    if weatherData['cod'] != 404:
                        temp = (weatherData['main']['temp'] - 273.15)  #kelvin to fahrenheit
                        cel=int(temp)
                        voiceResponse(str(cel)+" Degree Celsius")
                    else:
                        voiceResponse("There is some problem in getting weather data")
                elif responseParts[0] == "joke":
                    jokeData = getJoke()
                    if jokeData["status"] != 404:
                        voiceResponse(jokeData["joke"].encode("utf-8"))
                    else:
                        voiceResponse("There is some problem in getting joke, why don't you say one yourself?")
                elif responseParts[0] == "wikipedia":
                    try:
                        voiceResponse(getWiki(response[10:]).encode("utf-8"))
                    except wikipedia.exceptions.DisambiguationError as e:
                        voiceResponse(getWikiPage(e.options[0]).encode("utf-8")[:500])
                else:
                    voiceResponse(response)

            else:
                voiceResponse("\nI couldn't get you")
    except sr.UnknownValueError as e:
        print (e)
        
