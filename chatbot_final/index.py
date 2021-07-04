import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:

    while True:
        print("Hello! Say the speech you want to convert into text!")
        audio = r.listen(source)

        try:

            print("Sphinx thinks you said "+ r.recognize_sphinx(audio))
        except sr.UnknownValueError:
 
           print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        try:
            
            print("Shaolin thinks you said : \n"+r.recognize_google(audio))

        except sr.RequestError as e:

            print("Could not request results from Google Speech Recognition Service; {0}".format(e))
