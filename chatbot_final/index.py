import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        print("Say something!")
        audio = r.listen(source)

        try:
            print("Sphinx thinks you said "+ r.recognize_sphinx(audio))
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

        try:
            print("Google speech recognition thinks you said "+r.recognize_google(audio))
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition Service; {0}".format(e))