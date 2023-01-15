import os
import sys
import time
import traceback

# einbinden des Pfades zu den Modulen des Sprachassistenten
sys.path.append("C:\\Users\\marti\\Documents\\VSCode_Workspace\\Sprachassistent\\SA_Modules")

# Module mit Hauptfunktionalität
import SpeechRecognition as sr
import SystemManager as SysM
# import TextToSpeech as tts
# import FileManager as FileM


# Module des Sprachassistenten
import SA_Speaker
import SA_WebManager as SA_WebM
import SA_Math

sys.path.append("C:\\Users\\marti\\Documents\\VSCode_Workspace\\Sprachassistent\\Routines")
import Routine


''' Notizen:
alle Befehle sind aktuell kleingeschreiben (-> str.lower()), auch self.name 

Geplanter Ablauf:

- Laden der Befehlslisten aller Module
- Zuhören, Befehl erhalten etc.
- suchen nach dem Befehl in der Liste
- Ausführen des Befehls, der im anderen Modul implementiert ist

-> Ziel: importieren und aktualisieren der Module gewährleisten Änderungen zur Laufzeit

'''

"""
Befehle:
- über Direktaufruf und try-except
- aktuell: geh jedes mal in jedes modul und schau nach --> problem: prüfe eigene Listen (z.B. "schalte dich ab")
- evtl: sammle alle (ggf einzelne) Befehlslisten, damit Direktaufruf über mehrere module gleichzeitig geht


> Befehlsaufrufe klein geschrieben prüfen
"""


# Weitere Funktionalitäten:
    # Erkennen von zwei verschiedenen Befehlen in einem Satz -> "und"
    # Funktion, die zwischen höflich und persönlich wechselt.
    # Wechsel zwischen Sprachen

# Weitere Befehle: 
    # Andere Programme öffnen, u.a. Python
    # Suche nach begriffen, standard ecosia, alternativ google etc.
    # Befehle in der CMD eingeben / ausführen. (gefährlich)
        # Dateien öffnen, Dateien verschieben, Dateien löschen (gefährlich)

    

# in Zukunft:
    # erstelle einfache Graphen
    # Steuere / kommuniziere mit Arduino
    # prüfe, ob und welche Geräte verfügbar sind -> z.B. Arduino
    # prüfe Verbindugen, die genutzt werden sollen (Bluetooth, WLAN, ...)

# optimierte schriftliche Eingabe und rein schriftliche Ausgabe, nur das Wichtigste der Antwort
# Sonderbefehle -> kill

# passives und flexibles zuhören jederzeit
# ggf aktivieren durch Schlüsselwort
# parallel schriftliche Eingabe möglich

"""
aktuell: Module in anderen Modulen genutzt -> v.a. speaker
idee: zetrales Modul, welches von jedem aufgerufen werden kann, 
    welches Anfragen an andere Module managed
"""

class SpeechAssistant:
    def __init__(self, name : str, language : str, time_standBy_sec = None, time_listenCmd_sec = 15):
        self.authorFirstName = "Martin"
        self.authorFamName = "Hein"
        self.authorTitle = "Herr"

        self.name = name
        if language == "deutsch":
            self.rec_lang = "de-DE" # Sprache für Spracherkennungs-Software
            self.tts_lang = "de" # Sprache für google-Sprachausgabe
        
        self.initInstances()

        self.kill = False

        self.time_standBy_sec = time_standBy_sec
        self.time_listenCmd_sec = time_listenCmd_sec

        # Bestätigung, dass Befehl ausgeführt wird
        self.confirmExec = True
        self.conf_not = 0 #"not"
        self.conf_before = 1 #"before"
        self.conf_after = 2 #"after"
        
        self.initAllDictsAndLists()
        self.importCommands()

        self.inputMode_index = 1
        self.inputModi = {
            "vocal" : "Spracheingabe", 
            "written" : "schriftliche Eingabe"
        }
        self.inputMode = list(self.inputModi.keys())[self.inputMode_index]


    def printAllCommands(self):

        len0 = len(self.commands_0Arg)
        print("Befehle ohne Argumenten:", len0)
        if len0 != 0:
            for cmd in self.commands_0Arg.keys():
                print(cmd)

        len1 = len(self.commands_1Arg)
        print("\nBefehle mit 1 Argumenten:", len1)
        if len1 != 0:
            for cmd in self.commands_1Arg.keys():
                print(cmd, "<Arg>")

        print("")
        # print(len(self.commands_0Arg), "\n", self.commands_0Arg, "\n", len(self.commands_1Arg), "\n", self.commands_1Arg)

    def print(self, printCall):
        
        if printCall.lower() == "alle befehle":
            self.printAllCommands()
        elif printCall.lower() == "alle module":
            for module in self.modules.keys():
                print(module)
            print("")

    def initModuleDict(self):
        self.modules = {
            "sr" : {"module" : sr, "instance" : self.speechRecogizer},
            "webm" : {"module" : SA_WebM, "instance" : self.webManager},
            "sa_math" : {"module" : SA_Math, "instance" : self.sa_math},
            "sa_speaker" : {"module" : SA_Speaker, "instance" : self.sa_speaker}
            # "tts" : [tts, self.],
            # "filem" : FileM,
        }

    def initAllDictsAndLists(self):

        self.initModuleDict()

        _before = self.conf_before
        _after = self.conf_after
        _not = self.conf_not
        # Alle Befehle: <Befehl> : [<ausführende Methode>, <Aktion bestätigen>]
        self.commands_0Arg = {
            # self.name.lower() : [(self.sa_speaker).spokenToMe, _not],
            "stelle dich vor" : [self.introduceYourself, _not],
            "terminiere dich" : [self.terminate, _not],
            "schalte dich ab" : [self.terminate, _not],
            "schalte dich leise ab" : [self.terminateScilently, _not],
            "kill quietly" : [self.terminateScilently, _not],
            "eingabe wechseln" : [self.switchInputMode, _not],
            # "sprich lauter" : [(self.sa_speaker).increaseSpeechVolume, _not],
            # "sprich leiser" : [(self.sa_speaker).decreaseSpeechVolume, _after],
            # "sprich schneller" : [(self.sa_speaker).increaseSpeechRate, _not],
            # "sprich langsamer" : [(self.sa_speaker).decreaseSpeechRate, _not],
            # "sprich langsam" : [(self.sa_speaker).speakSlowly, _after],
            # "sprich normal" : [(self.sa_speaker).speakNormally, _after],
            # "sprich schnell" : [(self.sa_speaker).speakFast, _after],
            # "schalte dich stumm" : [(self.sa_speaker).mute, _not],
            "teste sr" : [(self.speechRecogizer).testings, _not],
            "einbrecher alarm" : [self.routineManager.intrudorAlarm, _not] # unsauber, komplette Struktur fehlt
        }
        self.commands_1Arg = {
            "aktualisiere" : [self.reloadModules, _not],
            "zeig mir" : [self.print, _before],
            "ton" : [self.volumeSpeech, _after]
            # "grüße" : [(self.sa_speaker).greetPerson, _not],
            # "hallo" : [(self.sa_speaker).greetPerson, _not],
            # "verabschiede dich von" : [(self.sa_speaker).goodbyePerson, _not],
            # "verabschiede" : [(self.sa_speaker).goodbyePerson, _not],
            # "sag" : [(self.sa_speaker).say, _not],
            # "öffne" : [(self.webManager).openWebsite_speech, _not],
            # "schreibe den dialog" : [(self.sa_speaker).setDialogOption_speech, _after],
            # "Rechner" : [self.sa_math.doAll, _not],
            # "rechne" : [self.sa_math.doAll, _not]
        }
        
        self.listOfAllCommandDicts = [self.commands_0Arg, self.commands_1Arg]
        self.commandError = "Befehl nicht gefunden."


    def reloadDicts(self):
        self.initAllDictsAndLists()

    def initInstances(self):
        self.speechRecogizer = sr.SpeechRecognition(language = self.rec_lang, keyword = self.name)
        self.sa_speaker = SA_Speaker.SA_Speaker(self.name, self.tts_lang)
        self.sa_math = SA_Math.SA_Math()


        ###################
        # SA_WebManager Instanz! siehe klasse -> 
        # Befehlsliste anpassen auf die Auslagerung!
        self.webManager = SA_WebM.SA_WebManager(self.name, self.tts_lang)

        self.routineManager = Routine.RoutineManager()
        # self.modules["sr"]["instance"]
        self.initModuleDict()


    def importCommands(self, moduleKeys = []):
        if len(moduleKeys) == 0:
            for mod in (self.modules).values():
                moduleInstance = mod["instance"]
                # addressiere die Instanz und frage die Befehlsliste ab
                
                try:
                    cmds = moduleInstance.shareCmds_dict()
                except AttributeError:
                    continue

                for i in cmds.keys():
                    if i == 0:
                        self.commands_0Arg.update(cmds[i])
                        print("{}: commands_0Arg importiert".format(moduleInstance))
                    elif i == 1:
                        self.commands_1Arg.update(cmds[i])
                        print("{}: commands_1Arg importiert".format(moduleInstance))

            print("Alle Befehle geladen...")

        elif len(moduleKeys) == 1:
            print(moduleKeys)
            print(moduleKeys[0], type(moduleKeys[0]))
            module = self.modules[moduleKeys[0]]
            moduleInstance = module["instance"]
            try:
                cmds = moduleInstance.shareCmds_dict()
            except AttributeError:
                return 
            
            for i in cmds.keys():
                if i == 0:
                    self.commands_0Arg.update(cmds[i])
                elif i == 1:
                    self.commands_1Arg.update(cmds[i])

        else:
            for mod in moduleKeys:
                moduleInstance = (self.modules[mod])["instance"]
                # addressiere die Instanz und frage die Befehlsliste ab
                
                try:
                    cmds = moduleInstance.shareCmds_dict()
                except AttributeError:
                    continue

                for i in cmds.keys():
                    if i == 0:
                        self.commands_0Arg.update(cmds[i])
                    elif i == 1:
                        self.commands_1Arg.update(cmds[i])
            
        self.listOfAllCommandDicts = [self.commands_0Arg, self.commands_1Arg]

    # TODO: zu implementieren
    def askFor(self, requestMessage : str) -> str:
        self.sa_speaker.talk(requestMessage)
        # if written.lower() == "reload":
        #     self.sa_speaker.talk("Welches Modul soll neue geladen werden?: ")
        #     module_str = input("Modul: ").strip()
        #     try:
        #         SysM.reloadModule(self.modules[module_str])
        #         if module_str == "SA_Speaker":
        #             # reinitialize Instance:
        #             print("SA_Speaker erkannt")
        #             print("alte Sprecherinstanz:\t\t", self.sa_speaker)
        #             self.sa_speaker = SA_Speaker.SA_Speaker(self.name, self.tts_lang)
        #             print("neue Sprecherinstanz:\t\t", self.sa_speaker)
        #             self.initAllDictsAndLists()

        #         self.sa_speaker.talk("Modul wurde neu geladen.")
        #     except KeyError:
        #         self.sa_speaker.talk("Dieses Modul ist unbekannt.")
            
        #     continue
        return input()

    def castModules(self, moduleStr : str):
        
        # if type(moduleStr) == str: # z.B. "sr, tts,FileM"
        #     if (moduleStr.strip()).lower() == "alle":
        #         return self.modules.keys(), []
        #     moduleStr = [splitted.strip() for splitted in moduleStr.split(",")]

        # print("strList: ", moduleStr)

        # modules = []
        # unknown = []

        # print("Meth: castModules -- modules: ", modules, "\t Unknown: ", unknown)

        # for module_str in moduleStr:
        #     try:
        #         module = self.modules[module_str]
        #         modules = modules.append(module)
        #         print("here")
        #     except KeyError:
        #         unknown = unknown.append(module_str)
                
        # return modules, unknown

        # "SA_Speaker"
        module = ""
        try:
            module = self.modules[moduleStr.strip().lower()]["module"]
        except KeyError:
            pass
               
        return module

    def reloadModules(self, speech : list):
        
        # aktualisiere "SA_Speaker"

        # if len(speech) == 0:
        #     speech = self.askFor("Welche Module sollen neu geladen werden?")
        
        # modules, unknown = [], []

        # print("modules: ", modules, "\t Unknown: ", unknown)
        # if speech == "alle" or speech == "alle module":
        #     modules = self.modules.keys()
        # else:
        #     modules, unknown = self.castModules(speech)

        # print("modules: ", modules, "\t Unknown: ", unknown)

        # if len(modules) == 0:
        #     message = "Es sind keine Module bekannt."

        # for module in modules:
        #     SysM.reloadModule(module)

        #     # Instanzen neu Laden

        #     if module == SA_Speaker:
        #         self.sa_speaker = SA_Speaker.SA_Speaker(self.name, self.tts_lang)
        #         print("in SA_Speaker")
        #     elif module == sr:
        #         self.speechRecogizer = sr.SpeechRecognition(language = self.rec_lang, keyword = self.name)
        
        # self.initAllDictsAndLists()

        # self.sa_speaker.talk("Modul wurde neu geladen.")

        if len(speech) == 0 or speech == None:
            speech = self.askFor("Welche Module sollen neu geladen werden?")
        

        if speech.lower() == "alle" or speech.lower() == "alle module":
            
            for module in (self.modules).values():
                m = module["module"]
                SysM.reloadModule(m)
                print(m)

            # Instanzen neu Laden:
            self.initInstances()
                
            # self.reloadDicts()

            self.importCommands()

            message = "Alle Module wurden neu geladen."

        else:
            module = self.castModules(speech)


            if module == "":
                message = "Es ist kein Modul bekannt."
            else:
                
                SysM.reloadModule(module)

                # Instanzen neu Laden
                if module == SA_Speaker:
                    self.sa_speaker = SA_Speaker.SA_Speaker(self.name, self.tts_lang)
                elif module == sr:
                    self.speechRecogizer = sr.SpeechRecognition(language = self.rec_lang, keyword = self.name)
                elif module == SA_WebM:
                    self.webManager = SA_WebM.SA_WebManager(self.name, self.tts_lang)
                elif module == SA_Math:
                    self.sa_math = SA_Math.SA_Math()
            
                # self.reloadDicts()
                self.importCommands([speech])

                message = "Modul wurde neu geladen."
        
        self.sa_speaker.talk(message)
        

    def introduceYourself(self):
        message = "Wenn ich mich vorstellen darf: Mein Name ist {}. Ich bin ein Sprachassistent und wurde von {} {} erschaffen.".format(self.name, self.authorTitle, self.authorFamName)
        (self.sa_speaker).talk(message)

    def terminate(self):
        self.kill = True
        massage = "Ich werde mich jetzt abschalten. \n Auf Wiedersehen."
        (self.sa_speaker).talk(massage)
        # sys.exit("Der Prozess \'{}.exe\' wurde terminiert.".format(self.name))

    def terminateScilently(self, printInfo = False):
        info = ""
        if printInfo == True:
            info = "Der Prozess \'{}.exe\' wurde terminiert.".format(self.name)
        
        sys.exit(info)


    ## Methoden, die nicht auf direkte Befehle ausgeführt werden,
    ## sondern die Funktionalität des Ass. aufbauen.
    
    def findCommand(self, speech : str) -> tuple or str:

        # for cmddict in self.listOfAllCommandDicts:
        #     for cmd in cmddict:
        #         if speech == cmd:
        #             return cmddict, cmd
            # -> Problem mit filtern der entspr. Argumente -> if-Statements
        
        # Entferne überschüssige Leerzeichen an Anfang und Ende und setze alle Buchstaben klein.
        speech = (speech.strip())#.lower()

        for cmd in self.commands_0Arg:
            if speech.lower() == cmd:
                arg = None
                return self.commands_0Arg, cmd, arg

        # eher in executeCommand
        # try:
        #     self.commands_0Arg[speech]
        #     cmd = speech
        #     arg = None
        #     return self.commands_0Arg, cmd, arg
        # except KeyError:
        #     pass
        
        for cmd in self.commands_1Arg:
            if speech[0:len(cmd)].lower() == cmd:
                arg = speech[len(cmd):]
                return self.commands_1Arg, cmd, arg

        return self.commandError
        

    
    #!! war, als die Befehle noch nicht import wurden
    #!! jetzt ungebraucht
    def findCommandFromModule(self, speech : str):
        # "sr" : {"module" : sr, "instance" : self.speechRecogizer}
        for mod in (self.modules).values():
            moduleInstance = mod["instance"]
            # addressiere die Instanz und frage die Befehlsliste ab
            
            try:
                #!! Fehler: Methode heißt nun shareCmds_dict und gibt ein dict zurück, kein tuple
                cmds = moduleInstance.shareCmds()
            except AttributeError:
                continue
            # diffArgs = len(cmds)

            # Entferne überschüssige Leerzeichen an Anfang und Ende und setze alle Buchstaben klein.
            speech = (speech.strip())#.lower()

            for cmd in cmds[0]:
                if speech.lower() == cmd:
                    arg = None
                    return cmds[0], cmd, arg

            # eher in executeCommand
            # try:
            #     self.commands_0Arg[speech]
            #     cmd = speech
            #     arg = None
            #     return self.commands_0Arg, cmd, arg
            # except KeyError:
            #     pass
            
            for cmd in cmds[1]:
                if speech[0:len(cmd)].lower() == cmd:
                    arg = speech[len(cmd):]
                    return cmds[1], cmd, arg

        return self.commandError


    def executeCommand(self, cmdList : dict, cmd : str, arg = None):
        # If arg is None, no argument is given and used.
        # If arg is a string or a list of 1 element, it will be given as argument for execution.
        # If arg is a list of n element, the elements will be given as arguments for execution as arg[n].

        messageOnException = "Es ist ein Fehler bei der Ausführung geschehen."
        
        if cmdList == self.commands_0Arg:
            exec = cmdList[cmd][0]
            
            if self.confirmExec == True and cmdList[cmd][1] == self.conf_before:
                (self.sa_speaker).confirmCmdExec()
            
            try:
                exec()
            except Exception:
                self.sa_speaker.talk(messageOnException)

                tracebackError = traceback.format_exc()
                print(tracebackError)
            
            if self.confirmExec == True and cmdList[cmd][1] == self.conf_after:
                (self.sa_speaker).confirmCmdExec()

        elif cmdList == self.commands_1Arg:
            exec = cmdList[cmd][0]
            
            if self.confirmExec == True and cmdList[cmd][1] == self.conf_before:
                (self.sa_speaker).confirmCmdExec()
            
            # Bisher sind alle Argumente Strings
            # -> Entferne Leerzeichen am Anfang und Ende mit arg.strip()
            try:
                exec(arg.strip())
            except Exception:
                self.sa_speaker.talk(messageOnException)

                tracebackError = traceback.format_exc()
                print(tracebackError)

            if self.confirmExec == True and cmdList[cmd][1] == self.conf_after:
                (self.sa_speaker).confirmCmdExec()

    #!! war, als die Befehle noch nicht import wurden
    #!! jetzt ungebraucht
    def executeCommandFromModule(self, cmdList : dict, cmd : str, arg = None):
        # If arg is None, no argument is given and used.
        # If arg is a string or a list of 1 element, it will be given as argument for execution.
        # If arg is a list of n element, the elements will be given as arguments for execution as arg[n].

        messageOnException = "Es ist ein Fehler bei der Ausführung geschehen."
        
        if arg == None:
            exec = cmdList[cmd][0]
            
            if self.confirmExec == True and cmdList[cmd][1] == self.conf_before:
                (self.sa_speaker).confirmCmdExec()
            
            try:
                exec()
            except Exception:
                self.sa_speaker.talk(messageOnException)

                tracebackError = traceback.format_exc()
                print(tracebackError)
            
            if self.confirmExec == True and cmdList[cmd][1] == self.conf_after:
                (self.sa_speaker).confirmCmdExec()

        else:# cmdList == self.commands_1Arg:
            exec = cmdList[cmd][0]
            
            if self.confirmExec == True and cmdList[cmd][1] == self.conf_before:
                (self.sa_speaker).confirmCmdExec()
            
            # Bisher sind alle Argumente Strings
            # -> Entferne Leerzeichen am Anfang und Ende mit arg.strip()
            try:
                exec(arg.strip())
            except Exception:
                self.sa_speaker.talk(messageOnException)

                tracebackError = traceback.format_exc()
                print(tracebackError)

            if self.confirmExec == True and cmdList[cmd][1] == self.conf_after:
                (self.sa_speaker).confirmCmdExec()

## verschieben in SystemManager:
    # mach lauter/leiser
    # dreh die lautstärke/den Ton rauf/runter
    # setze die lautstärke/den Ton auf ..%/maximal
    # schalte den ton aus

    # -> Ton lauter/leiser // auf ..% // aus
    
    # evtl anfrage im SysM verarbeiten
    def volumeSpeech(self, speech, step=10):
        speech = speech.strip()

        if speech == "lauter":
            SysM.increaseVolume(step)
        elif speech == "leiser":
            SysM.decreaseVolume(step)
        elif speech == "aus":
            SysM.muteVolume()
        elif speech[:3] == "auf":
            SysM.setVolume(int(speech[3:]))


    def switchInputMode(self):
        self.inputMode_index += 1
        self.inputMode_index %= len(self.inputModi)
        self.inputMode = list(self.inputModi.keys())[self.inputMode_index]

        self.sa_speaker.talk(f"Eingabe auf {self.inputModi[self.inputMode]} umgestellt.")


    def mainProcess(self):

        '''
        Ziel: Mikrofon wird dauerhaft (10 min oder so) überwacht und auf das Schlüsselwort self.name gewartet.
        Daraufhin werden weitere Aufzeichnungen von Mikrofon auf Befehle überprüft.
        Bekannte Befehle werden ausgeführt, unbekannte werden ignoriert, 
        bzw. vielleicht nach wiederholtem Fehlschlagen wird man informiert, dass dies kein Befehl ist.
        Jedenfalls wird noch kurze Zeit (1 min) auf weitere Befehle gewartet und ggf. diese ausgeführt nach oberem Schema.
        Sobald nichts mehr gesagt wird, wird auf "Stand-By" geschaltet und man beginnt von Vorne.
        Evtl. wird sich nach 10min (siehe erster Punkt) das Programm terminieren.
        
        In Stichpunkten:
        - Mikofon abhören nach Schlüsselwort, dem eigenen Namen.    *
        > nicht erkannt -> evtl. nach 10 Min terminieren
        > erkannt: Befehl erwarten                                  **
            - Mikrofon abhören
            - prüfen auf bekannten Befehl
            > nicht erkannt -> weiter hören ohne Kommentar
                -> nach < 1 Min ohne Weitere Worte: "Ich höre zu"
                -> nach < 1 Min mit unbekannten Worten: informieren über Unklarheit
                -> nach 1 Min zurückkehren zum Stand-by Schlüsselwort (still oder mit Information darüber) ab *
            > erkannt -> Befehl ausführen
                -> Loop bei **
        '''

        welcomeBack = False
        
        while 1:
            if welcomeBack:
                print("Stand-by")
                welcomeBack = False
            
            if (self.speechRecogizer).listenForKeyword(waitingForSuccess = self.time_standBy_sec):
                
                # ggf. terminieren nach 10 Min -> implementieren in SpeechRec.py
                welcomeBack = True

                (self.sa_speaker).spokenToMe()

                startTimer = time.time()
                endTimer = startTimer
                while 1:
                    if self.kill:
                        return

                    duration = endTimer - startTimer
                    if duration >= self.time_listenCmd_sec:
                        print("{} Sekunden vorüber...".format(duration))
                        # Kehre zurück und warte auf das Schlüsselwort
                        break


                    speech = (self.speechRecogizer).listenFromMicrophone(phraseDuration=4)

                    if speech != "" and speech != None:
                        
                        (self.sa_speaker).outputDialog("Eingabe", speech)

                        if speech.lower() == "stopp":
                            self.terminateScilently()
                        
                        foundCommand = friday.findCommand(speech)
                        #print("Rückgabewert von 'findCommand':\n\t", foundCommand)
                    
                        if foundCommand == self.commandError:
                            # message = "Ich kenne diesen Befehl leider nicht."
                            # tts.textToSpeech(message)
                            pass
                        else:
                            startTimer = time.time()
                            
                            cmddict, cmd, arg = foundCommand
                            #print("Dictionary:\t", cmddict, "\nBefehl\t", cmd, "\nArgument(e)\t", arg)
                            friday.executeCommand(cmddict, cmd, arg=arg)
                    
                    endTimer = time.time()
            else:
                (self.sa_speaker).talk("Ich bin dann mal weg.")
                break

    def mainProcessWritten(self):
        
        while 1:

            if self.kill:
                return

            written = input("\nEingabe:\n")
            print("")
            if (self.sa_speaker).outputDialog != "terminal":
                (self.sa_speaker).outputDialog("Eingabe", written)

            if written != "" and written != None:
                
                if written.lower() == "stopp":
                    break

                ## nur temporär
                foundCommand = friday.findCommand(written)
                #print("Rückgabewert von 'findCommand':\n\t", foundCommand)
            
                if foundCommand == self.commandError:
                    # message = "Ich kenne diesen Befehl leider nicht."
                    # tts.textToSpeech(message)# for google:, self.tts_lang , saveOutput=False)
                    pass
                else:
                    cmddict, cmd, arg = foundCommand
                    #print("Dictionary:\t", cmddict, "\nBefehl\t", cmd, "\nArgument(e)\t", arg)
                    friday.executeCommand(cmddict, cmd, arg=arg)
                    continue

                if False:
                    foundCommand = friday.findCommandFromModule(written)
                    #print("Rückgabewert von 'findCommand':\n\t", foundCommand)
                
                    if foundCommand == self.commandError:
                        # message = "Ich kenne diesen Befehl leider nicht."
                        # tts.textToSpeech(message)# for google:, self.tts_lang , saveOutput=False)
                        continue
                    else:
                        cmddict, cmd, arg = foundCommand
                        #print("Dictionary:\t", cmddict, "\nBefehl\t", cmd, "\nArgument(e)\t", arg)
                        friday.executeCommandFromModule(cmddict, cmd, arg=arg)


# Hauptprogramm
if __name__ == '__main__':
    # Setze die Sprache, einfach in Kleinbuchstaben
    name = "Friday" # "Scotty"
    language = "deutsch"

    recDuration = 4 # später: freies Zuhören
    
    friday = SpeechAssistant(name, language, time_standBy_sec = None, time_listenCmd_sec = 60)

    friday.sa_speaker.welcome()

    if 1:
        friday.mainProcess()
    else:
        friday.mainProcessWritten()
    