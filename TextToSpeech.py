from gtts import gTTS
from playsound import playsound

import pyttsx3

import os
import sys

class TextToSpeech:
    def __init__(self, language = "deutsch"):
        self.engine = pyttsx3.init()
        # self.language ist eigentlich nicht nötig

        if language == "deutsch" or language == "de":
            self.language = "de"
            self.voiceID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"
        elif language == "englisch" or language == "english" or language == "en":
            self.language = "en"
            self.voiceID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        # elif language == "russisch" or language == "ru":
        #     self.language = "ru"
        
        (self.engine).setProperty('voice', self.voiceID)
        self.setVoiceError = "Diese Stimme ist unbekannt."

        self.speechVolume = 1.0
        self.maxSpeechVolume = 1.0
        self.minSpeechVolume = 0.0

        # alles ausserhalb dieser Werte ist schwachsinnig
        self.maxSpeechRate = 340
        self.minSpeechRate = 60
        
        self.fastSpeechRate = 240
        self.normalSpeechRate = 180
        self.slowSpeechRate = 140

        self.outOfBoundsError = "Dieser Werte kann nicht gesetzt werden."

                

    def textToSpeech(self, text : str):
        (self.engine).say(text)#'Der flotte braune Hund sprang über den faulen Hund.')
        
        #engine.startLoop(True)
        #engine.endLoop()

        (self.engine).runAndWait()


    def getAllVoices(self):
        return (self.engine).getProperty('voices')

    def getActiveVoice(self):
        return (self.engine).getProperty('voice')

    def setVoice(self, voiceID : str):
        voices = self.getAllVoices()

        for v in voices:
            if voiceID == v.id:
                (self.engine).setProperty('voice', voiceID)
                return 0

        return self.setVoiceError

    def printAllVoicesInfo(self, testVoice = False):
        voices = self.getAllVoices()

        for i in range(0, len(voices)):
            print("\nVoice {}:".format(i+1))
            print("ID: ", voices[i].id)
            print("Name: ", voices[i].name)
            print("Age: ", voices[i].age)
            print("Gender: ", voices[i].gender)
            print("Languages: ", voices[i].languages)
            
            if testVoice == True:
                (self.engine).setProperty('voice', voices[i].id)
                (self.engine).say('Ein netter Zungenbrecher, der mir nicht einfällt.')
                (self.engine).runAndWait()
        (self.engine).setProperty('voice', self.voiceID)


    def getSpeechVolume(self):
        # return float from 0.0 to 1.0
        return (self.engine).getProperty('volume')

    def setSpeechVolume(self, volume : float):
        # set float from 0.0 to 1.0
        if volume < self.minVolume or volume > self.maxVolume:
            return self.outOfBoundsError
        else:
            (self.engine).setProperty('volume', volume)

    def maxSpeechVolume(self):
        (self.engine).setProperty('volume', 1.0)

    def mute(self):
        self.speechVolume = (self.engine).getProperty('volume')
        (self.engine).setProperty('volume', 0.0)

    def unmute(self):
        (self.engine).setProperty('volume', self.speechVolume)

    def increaseSpeechVolume(self, step = 0.1):
        curVol = (self.engine).getProperty('volume')
        (self.engine).setProperty('volume', curVol + step)
        
    def decreaseSpeechVolume(self, step = 0.1):
        curVol = (self.engine).getProperty('volume')
        (self.engine).setProperty('volume', curVol - step)
    
    
    def getSpeechRate(self):
        return (self.engine).getProperty('rate')

    def setSpeechRate(self, rate : int):
        (self.engine).setProperty('rate', rate)

    def increaseSpeechRate(self, step = 20):
        curRate = (self.engine).getProperty('rate')
        if curRate <= self.maxSpeechRate - step:
            (self.engine).setProperty('rate', curRate + step)

    def decreaseSpeechRate(self, step = 20):
        curRate = (self.engine).getProperty('rate')
        if curRate >= self.minSpeechRate + step:
            (self.engine).setProperty('rate', curRate - step)


def findOwnPath():
    return sys.path[0] + "\\"

# TTS mit Google = einzige Methode
def googleTTS(text, language, saveOutput=False):
    outputFileName = "audio_tts.mp3"
    outputFilePath = findOwnPath()

    tts = gTTS(text = text, lang = language, slow = False)
    tts.save(outputFilePath + outputFileName)
    playsound(outputFilePath + outputFileName)

    if saveOutput == False:
        if os.path.exists(outputFilePath + outputFileName):
            os.remove(outputFilePath + outputFileName)



#Testing
engine = pyttsx3.init()

def onWord(name, location, length):
   print('word', name, location, length)
   if location > 10:
      engine.stop()

def testing():
    engine.connect('started-word', onWord)
    engine.say('Ein netter Zungenbrecher, der mir nicht einfällt.')
    engine.runAndWait()



if __name__ == '__main__':
    language = "de"

    if language == "de":
        text = "Hallo. Ich bin der Anfang eines Sprachassistenten. Und warum? Weil es ein sehr schönes Projekt ist!"
    elif  language == "ru":
        text = "Здравствуй. Я начинающий голосовой помощник. И почему? Потому что это очень хороший проект!"

    #googleTTS(text, language, saveOutput=False)

    tts = TextToSpeech(language = language)
    text = "Ein netter Zungenbrecher, der mir nicht einfällt."
    
    # voiceID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"
    # print(tts.setVoice(voiceID))
    # tts.printAllVoicesInfo()
    # tts.textToSpeech(text)

    tts.printAllVoicesInfo(testVoice=False)

    # text = "Das ist ein Test."
    # text = '''
    #     Bekannte Befehle werden ausgeführt, unbekannte werden ignoriert, 
    #     bzw. vielleicht nach wiederholtem Fehlschlagen wird man informiert, dass dies kein Befehl ist.
    #     Jedenfalls wird noch kurze Zeit (1 min) auf weitere Befehle gewartet und ggf. diese ausgeführt nach oberem Schema.
    #     '''
    text = "hallo"
    if 0: # Lautstärketest
        if 0:
            i = 0.0
            for j in range(0, 20):
                print("i =", i)
                tts.setSpeechVolume(i)
                
                print(tts.getSpeechVolume())
                tts.textToSpeech(text)
                i += 0.1
        elif 0:
            i = 0.3
            for j in range(0, 10):
                print("i =", i)
                tts.setSpeechVolume(i)
                
                print(tts.getSpeechVolume())
                tts.textToSpeech(text)
                i -= 0.1

    elif 0: # Sprechratetest
        if 0: # Automatisierte Inkrementierung
            for i in range(0, 10):
                
                tts.decreaseSpeechRate()
                tts.textToSpeech(text)
                print(tts.getSpeechRate())
        elif 0:
            while True:
                i = input("Input: ")
                if i == "exit":
                    break
                try:
                    x = int(i)
                except ValueError:
                    continue
                print("x =", x)
                tts.setSpeechRate(x)
                tts.textToSpeech(text)
                print("tatsächliche Rate: ", tts.getSpeechRate())
            

    # tts.textToSpeech(text)


