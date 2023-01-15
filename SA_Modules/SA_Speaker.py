import random

import TextToSpeech as tts
import FileManager as fm



class SA_Speaker:
    def __init__(self, sa_name : str, sa_tts_lang : str, set_to_complete_init = True):
        self.sa_name = sa_name
        self.sa_speaker = tts.TextToSpeech(sa_tts_lang)

        # Dialog-Ausgabe
        self.dialogOutputOption = "terminal"   # "terminal", "file", "window"/"gui", "not"
        self.dialogOutputFile = fm.findOwnPath() + "Dialog.txt"
        self.overwriteDialogFile = True

        self.dialogOutputOptions = {"not" : 0, "terminal" : 1, "file" : 2}#, "window"/"gui" : 3}

        self.confirmationPhrases = ["Natürlich.", "Gerne.", "Sehr gerne.", "Selbstverständlich.", "Wie du wünscht."]

        # Standardwerte für Sprechrate und -lautstärke
        self.speechVolStep = 0.1 # änderbar über Prozent
        self.speechRateStep = 20
        # alles ausserhalb dieser Werte ist schwachsinnig
        self.maxSpeechRate = 340
        self.minSpeechRate = 60
        
        self.fastSpeechRate = 300 #240
        self.normalSpeechRate = 180
        self.slowSpeechRate = 140

        if set_to_complete_init == True:
            (self.sa_speaker).setSpeechRate(self.normalSpeechRate)

        self.conf_not = 0 #"not"
        self.conf_before = 1 #"before"
        self.conf_after = 2 #"after"

        _before = self.conf_before
        _after = self.conf_after
        _not = self.conf_not
        # Alle Befehle: <Befehl> : [<ausführende Methode>, <Aktion bestätigen>]
        self.commands_0Arg = {
                            self.sa_name.lower() : [self.spokenToMe, _not],
                            "sprich lauter" : [self.increaseSpeechVolume, _not],
                            "sprich leiser" : [self.decreaseSpeechVolume, _after],
                            "sprich schneller" : [self.increaseSpeechRate, _not],
                            "sprich langsamer" : [self.decreaseSpeechRate, _not],
                            "sprich langsam" : [self.speakSlowly, _after],
                            "sprich normal" : [self.speakNormally, _after],
                            "sprich schnell" : [self.speakFast, _after],
                            "schalte dich stumm" : [self.mute, _not],
                            "testing meeee" : []
        }
        self.commands_1Arg = {
                            "grüße" : [self.greetPerson, _not],
                            "hallo" : [self.greetPerson, _not],
                            "verabschiede dich von" : [self.goodbyePerson, _not],
                            "verabschiede" : [self.goodbyePerson, _not],
                            "sag" : [self.say, _not],
                            "schreibe den dialog" : [self.setDialogOption_speech, _after]
        }

    def shareCmds_dict(self) -> dict:
        return {0 : self.commands_0Arg, 1 : self.commands_1Arg}

    def confirmCmdExec(self):
        index = random.randint(0, len(self.confirmationPhrases) - 1)
        self.talk(self.confirmationPhrases[index])

    def talk(self, message : str, specialOutput = None):
        # vielleicht irgendwann asynchron -> schreibtwährend spricht
        if specialOutput == None:
            self.outputDialog(self.sa_name, message)
        else:
            self.outputDialog(self.sa_name, specialOutput)
        (self.sa_speaker).textToSpeech(message)

    def outputDialog(self, speaker : str, dialog : str):
        if dialog == None:
            dialog = ""
        output = speaker +":\n " + str(dialog) + "\n"
        
        if self.dialogOutputOption == "terminal":
            print(output)
        
        elif self.dialogOutputOption == "file":
            if fm.checkExistingFile(self.dialogOutputFile) == False:
                directory, file = fm.separateFileAndDir(self.dialogOutputFile)
                fm.createFile(directory, file)
                fm.addNewLine(self.dialogOutputFile, output)
            elif self.overwriteDialogFile == True:
                fm.overwriteExistingFile(self.dialogOutputFile, output)
                self.overwriteDialogFile = False
            else:
                fm.addNewLine(self.dialogOutputFile, output)

            '''
            Datei ex nicht -> erstellen + neue Zeile
            Datei ex
                > überschreiben: ja -> overwrite + überschreiben >nein
                > überschreiben: nein -> neue Zeile
            '''

        elif self.dialogOutputOption == "window": #/"gui"
            pass

    def configureDialogOuput(self, outputOption : str) -> str:
        try:
            self.dialogOutputOptions[outputOption]
            self.dialogOutputOption = outputOption
        except KeyError:
            pass
        
        return self.dialogOutputOption

    def setDialogOption_speech(self, speech : str):
        option = self.getDialogOptionFromSpeech(speech)
        self.configureDialogOuput(option)

    def getDialogOptionFromSpeech(self, speech : str) -> str:
        speech = speech.strip()
        
        if speech == "nicht auf":
            return "not"
        elif speech == "in das terminal":
            return "terminal"
        elif speech == "in die datei":
            return "file"
        elif speech == "in das fenster":
            return "window"
        
        return ""


    def say(self, toSay: str): # eher Teil von commands_1Arg
        self.talk(toSay)

    def greetPerson(self, person : str):
        print(person)
        if person.lower() == "mich" or person.lower() == self.sa_name.lower():
            person = "Herr Hein"
        message = "Hallo {}.".format(person) # "Ich grüße {}.".format(person)
        self.talk(message)

    def goodbyePerson(self, person : str):
        lowerStr = person.lower()

        concerningMe =  {
                        "mir" : 0,
                        "mich" : 0,
                        "dich" : 0
                        }

        try:
            concerningMe[person]
            person = ""
        except KeyError:
            person = " " + person
        # if lowerStr == "mir" or lowerStr == "mich" or lowerStr == "dich":
        #     person = ""
        # else:
        #     person = " " + person
        
        message = "Auf Wiedersehen{}.".format(person)
        self.talk(message)

    # Reaktionen des Ass., wenn sein Name genannt wird:
    def spokenToMe(self):
        self.talk("Ja bitte?")

    def welcome(self):
        message = "Guten Tag."
        self.talk(message)# for google:, self.tts_lang , saveOutput=False)
    
    def goodbye(self):
        message = "Auf Wiedersehen."
        self.talk(message)# for google:, self.tts_lang , saveOutput=False)



    # Setze Sprechoptionen

    def mute(self):
        (self.sa_speaker).mute()

    def increaseSpeechVolume(self, step = -1.0):# = self.speechVolStep):
        if (self.sa_speaker).getSpeechVolume() >= (self.sa_speaker).maxSpeechVolume:
            massage = "Ich kann nicht lauter sprechen."
            self.talk(massage)
            return
        
        if step < 0:
            step = self.speechVolStep

        (self.sa_speaker).increaseSpeechVolume(step = step)

        self.confirmCmdExec()

    def decreaseSpeechVolume(self, step = -1.0):# = self.speechVolStep):
        if step < 0:
            step = self.speechVolStep
            
        (self.sa_speaker).decreaseSpeechVolume(step = step)

    def increaseSpeechRate(self, step = -1.0):# = self.speechRateStep):
        if (self.sa_speaker).getSpeechRate() == self.maxSpeechRate:
            massage = "Ich kann nicht schneller sprechen."
            self.talk(massage)
            return
        
        if step < 0:
            step = self.speechRateStep

        if (self.sa_speaker).getSpeechRate() + step >= self.maxSpeechRate:
            (self.sa_speaker).setSpeechRate(self.maxSpeechRate)
        else:
            (self.sa_speaker).increaseSpeechRate(step = step)

        self.confirmCmdExec()

    def decreaseSpeechRate(self, step = -1.0):# = self.speechRateStep):
        if (self.sa_speaker).getSpeechRate() == self.minSpeechRate:
            massage = "Ich kann nicht langsamer sprechen."
            self.talk(massage)
            return
        
        if step < 0:
            step = self.speechRateStep

        if (self.sa_speaker).getSpeechRate() - step <= self.minSpeechRate:
            (self.sa_speaker).setSpeechRate(self.minSpeechRate)
        else:
            (self.sa_speaker).decreaseSpeechRate(step = step)

        self.confirmCmdExec()

    def speakSlowly(self):
        (self.sa_speaker).setSpeechRate(self.slowSpeechRate)

    def speakNormally(self):
        (self.sa_speaker).setSpeechRate(self.normalSpeechRate)

    def speakFast(self):
        (self.sa_speaker).setSpeechRate(self.fastSpeechRate)
