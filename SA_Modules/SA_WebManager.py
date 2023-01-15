import validators

from selenium import webdriver

import os
from googlesearch.googlesearch import GoogleSearch

import  SA_Speaker

"""
IDEEN:
- Liste an Links auslagern in Textdatei
- on the fly Hinzufügen von neuen Webseiten
 -> Textfeld: Bezeichnung (evtl spracheingabe) + manuell getippter Link
 -> graphisch: Bezeichung (evtl Spracheingabe) + erkennt selbst offene Webseite 
"""


class SA_WebManager():
    def __init__(self, sa_name="Friday", sa_language="de"):
        self.driver = "" #self.openBrowser("firefox")

        self.name = sa_name
        self.tts_lang = sa_language
        self.initSpeechAssOpt()


        self.conf_not = 0 #"not"
        self.conf_before = 1 #"before"
        self.conf_after = 2 #"after"

        _before = self.conf_before
        _after = self.conf_after
        _not = self.conf_not
        # Alle Befehle: <Befehl> : [<ausführende Methode>, <Aktion bestätigen>]
        self.commands_0Arg = {}
        self.commands_1Arg = {
            "öffne" : [self.openWebsite_speech, _not],
            "suche" : [self.search, _not]
        }

    def shareCmds_dict(self) -> dict:
        return {0 : self.commands_0Arg, 1 : self.commands_1Arg}

    def initSpeechAssOpt(self):
        self.sa_speaker = SA_Speaker.SA_Speaker(self.name, self.tts_lang)


        # Alle Webseiten: <Bezeichnung> : <URL>
        self.webbrowser = {
            "firefox" : "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "chrome" : "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe", 
            "edge"  : "C:\\Users\\marti\\AppData\\Local\\Microsoft\\WindowsApps\\MicrosoftEdge.exe"
        }
        self.defaultBrowser = "firefox"

        self.website_url = {
            "youtube" : "https://www.youtube.com/",
            "google" : "https://www.google.de/",
            "studon" : "https://www.studon.fau.de/",
            "machine-learning" : "https://machine-learning-for-physicists.org/",
            "bing" : "https://www.bing.com/"
        }
        self.websiteError = "Webadresse nicht gefunden."


    
    def openBrowser(self, browser : str):
        if browser.lower() == "firefox":
            driver = webdriver.Firefox(executable_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe")

        return driver

    def openWebsite(self, url : str):
        self.driver.get(url)

    def search(self, request : str):
        print("Search for \'{}\'".format(request))
        response = GoogleSearch().search(request)
        print("Response object:", response)
        print(dir(response))
        print("Response results:", response.results)
        print("Total number of results:", response.total)
        for result in response.results:
            
            print("Title:", result.title)
            print("URL:", result.url)
            print("Content:", result.getText())


    # Sprachassistent:
    def analyzeWebcall(self, webcall : str) -> tuple:
        # Öffne YouTube in/mit Firefox
        #   -> webcall: Youtube in/mit Firefox
        #   -> website: Youtube
        #   -> key:     in / mit
        #   -> browser: Firefox

        website = webcall
        browser = ""

        listOfKeys = [" in ", " mit "]

        for k in listOfKeys:
            index = webcall.find(k)
            if index != -1:
                website = webcall[:index].strip()
                browser = webcall[index + len(k):].strip()

        return website, browser

    def openWebsite(self, url : str, browser = "") -> int:
        if url == "":
            return 
        
        if browser == "":
            browser = self.defaultBrowser
        
        browserEXE = ""
        try:
            # Entnehme den Programmpfad zum Browser
            browserEXE = self.webbrowser[browser.lower()]
        except KeyError:
            # Fehlermeldung
            warning = """Der Browser, """ + browser + """, konnte intern nicht gefunden werden.\n
                        Ich rufe den Standard-Browser auf."""
            (self.sa_speaker).talk(warning)
            
            # Frage nach Versuch mit Standardbrowser
            # nein: return
            # ja:
            browserEXE = self.webbrowser[self.defaultBrowser]

        cmd = '\"' + browserEXE + '\" \"' + url + '\"'
        os.popen(cmd)
        
        return 0

    def openWebsite_speech(self, webcall : str):
        # Analyse des Befehls nach Webadresse und Browser
        website, browser = self.analyzeWebcall(webcall)
        
        print ("Eingabe: Webseite:", website, "Browser:", browser)

        url = ""
        try:
            # Probiere, ob diese Webseite schon bekannt ist:
            url = self.website_url[website]
        except KeyError:
            ## TODO: Finde einen Weg die richtige Endung zu finden 
            ## -> probiere Liste durch (nicht aufrufen, nur prüfen)

            # Probiere, die Webseite trotzdem zu öffnen. 
            # Vorsicht, es können falsche Internetseiten geöffnet werden.
            
            ## ausgeschaltete Fehlermeldung
            # warning = """Die Webadresse, """ + website + """, konnte intern nicht gefunden werden. 
            #             Ich werde versuchen, sie trotzdem aufzurufen."""
            # (self.sa_speaker).talk(warning)
            # erwartet Ja oder Nein

            # TODO: prüfe, ob .org, .ru ... angeängt sind, wenn nicht, dann .com
            url = website + ".com"
        print ("Eingabe: Webseite:", website, "Browser:", browser)
        
        self.openWebsite(url, browser=browser)


## TODO: 

# Liste von bekannten Top-Level-Domains
TLDs = {"com" : "", "org" : "", "de" : "", "ru" : ""}

def checkURL(toCheck):
    
    try:
        return validators.url(toCheck)
    except validators.ValidationFailure:
        return False
        print("NOPE")


def checkTLD(toCheck):
    # toCheck ist z.B. "google.com"
    toCheck = toCheck.strip()
    index = toCheck.find(".")
    if index == -1:
        return False
    
    tld = toCheck[index+1:]
    try:
        TLDs[tld]
        return True
    except KeyError:
        return False

if __name__ == '__main__':
    # pass
    # url = "mozilla de"
    # # print(checkURL(url))
    # # print(checkTLD(url))

    wm = SA_WebManager()
    # wm.openWebsite("google.com")

    request = "Auto"

    wm.search(request)


