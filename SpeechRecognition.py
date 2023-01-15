import speech_recognition as sr
import time

import sys
sys.path.append("C:/Users/marti/Documents/VSCode_Workspace/pocketsphinx-python")

class SpeechRecognition:
    def __init__(self, language = "deutsch", keyword = ""):
        self.speechEngine = sr.Recognizer()
        if language == "deutsch" or "de-DE":
            self.language = "de-DE" # Sprache für Spracherkennungs-Software
        
        # self.language = "en-US"

        # Wenn keyword == "" wird nicht auf ein Schlüsselwort gewartet, sonder direkt aufgezeichnet.
        self.keyword = keyword
        self.listenKeywordSec = 1.5

    #keywordError = "Es ist kein Schlüsselwort vorhanden."

    def setKeyword(self, keyword : str):
        self.keyword = keyword

    def recFromFile(self, file):
        with sr.AudioFile(file) as f:
            data = (self.speechEngine).record(f)
            print("Wertet aus...")
            
            text = ""
            try:
                text = (self.speechEngine).recognize_google(data, language = self.language)
            except sr.UnknownValueError:
                return "Daten konnten nicht ausgewertet werden."
            
            return text

    def recFromMicrophone(self, duration):
        with sr.Microphone() as micro:
            print("Nimmt vom Mikrofon auf...")
            audio = (self.speechEngine).record(micro, duration = duration)
            print("Wertet aus...")
            text = ""
            try:
                text = (self.speechEngine).recognize_google(audio, language = self.language)
                # text = (self.speechEngine).recognize_sphinx(audio, language = self.language)
            except sr.UnknownValueError:
                return None

        return text

    def listenForKeyword(self, waitingForPhrase = None, waitingForSuccess = None) -> bool:
        '''
        Diese Methode wartet darauf, dass ein zuvor gesetztes Schlüsselwort gesagt wird.
        Falls kein Schlüsselwort gesetzt wurde, wird die Methode beendet.

        Rückgabewert: -keine-
        '''
        
        if self.keyword == "" or self.keyword == None:
            return True
        
        # if waitingForSuccess == None:
        #     waitingForSuccess = -1
        #     # dadurch wird ein nie erfüllbares Kriterium erzeugt -> nie

        with sr.Microphone() as micro:
            print("Wartet auf Schlüsselwort...")

            listening = ""

            startTimer = time.time()
            endTimer = startTimer
            while listening == None or listening.lower() != (self.keyword).lower():
                
                if waitingForSuccess != None:
                    duration = endTimer - startTimer
                    if duration >= waitingForSuccess:
                        return False

                print("\nstart listening")
                audio = (self.speechEngine).listen(micro, timeout = waitingForPhrase, phrase_time_limit = self.listenKeywordSec)
                print("stop listening")

                try:
                    listening = (self.speechEngine).recognize_google(audio, language = self.language)
                except sr.UnknownValueError:
                    listening = None
                
                print("Eingabe: {}".format(listening))

                if waitingForSuccess != None:
                    endTimer = time.time()
                
            print("Schlüsselwort erkannt!")
            return True

    # am besten soll gewartet werden, bis man anfängt zu sprechen und 
    # beendet werde, wenn man aufhört zu sprechen (z.B. 1s abwarten)
    def listenFromMicrophone(self, waitingForPhrase = None, phraseDuration = None):

        with sr.Microphone() as micro:
            print("Nimmt jetzt auf...")
            
            print("start listening")
            audio = (self.speechEngine).listen(micro, timeout = waitingForPhrase, phrase_time_limit = phraseDuration)
            print("stop listening")

            text = ""
            try:
                text = (self.speechEngine).recognize_google(audio, language = self.language)
                # text = (self.speechEngine).recognize_sphinx(audio, language = self.language)
            except sr.UnknownValueError:
                text = None
            
        return text

    
    # Methoden zum Testen:
    def recListeningLoop(self):
        print("Nimmt jetzt auf...")
        with sr.Microphone() as micro:
            
            text = ""
            count = 0
            while 1:
                print("\nStart")
                try:
                    audio = (self.speechEngine).listen(micro, timeout=2, phrase_time_limit =0.1)# self.listenKeywordSec)
                    print("Stopp")
                except sr.WaitTimeoutError:
                    print("Stopp")
                    continue

                print(audio)
                try:
                    text += " " + (self.speechEngine).recognize_google(audio, language = self.language)
                    # text += " " + (self.speechEngine).recognize_sphinx(audio, language = self.language)
                    count = 0
                except sr.UnknownValueError:
                    count += 1
                    if count == 10:
                        text += "." #None
                        break
                
                # if text != None and text.lower() == (self.keyword).lower():
                #     print("Treffer!", end = "")
                # print(text)

        return text
            
    def testings(self):
        print("Hier wird Speech Recognition getestet.")


# Hauptprogramm
if __name__ == '__main__':
    # Sprachassistent
    language = "en-US" #"deutsch"
    recDuration = 2
    speechRec = SpeechRecognition(language = language, keyword = "Friday")
    
    
    # gewünschte Audiodatei, ggf. über Tkinter
    #file = ""
    #print(recFromFile(file, language))

    #print(speechRec.recFromMicrophone(recDuration))

    #speechRec.listenFromMicrophone()
    
    #while 1:
    # print(speechRec.recListeningLoop())
    print(speechRec.listenFromMicrophone())

        # if input("again? ENTER / n:") == "n":
        #     break
    

