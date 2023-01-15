import importlib
import numpy as np
from time import sleep

import matplotlib.pyplot as plt

import SA_Speaker as Speaker

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume





def getAndProcessInput(inputRequestText : str, castTo = 'str', errorType = Exception, errorMessage = None):
    """
    In dieser Methode wird versucht, die Eingabe über das Terminal in den gewünschten Datentyp zu casten (= umwandeln).
    Die Methode endet erst, wenn eine gültige Eingabe getätigt wurde; sie wird im gewünschten Datentypen zurückgegeben.
    
    Achtung: Beim Versuch zu casten können Fehler auftreten. Diese sollten nach Möglichkeit korrekt als Argument übergeben werden.
    Der standardmäßig abgefangene Fehler "Exception" ist sehr allgmein und gibt keinen Rückschluss auf das Problem.
    """
    
    dictOfErrorMessages = { 'str' : "",
                            'int' : "Bitte gib eine Ganzzahl (int) ein: ",
                            'float' : "Bitte gib eine Fließkommazahl (float) ein, mit Dezimalpunkt: ",
                            'bool' : "Bitte gib einen Wahrheitswert (True / False) ein: "
                        }
    operationErrorMessage = "Diese Operation zum Casten ist unbekannt."

    # Prüfe nach bekannter Operation zum Casten:
    while True:
        try:
            dictOfErrorMessages[castTo]
            break
        except KeyError:
            print(operationErrorMessage)
            while True:
                castTo = input("Operation zum Casten oder Liste aller möglichen Casts mit <help>: ").strip()
                if castTo == "help":
                    for cast in dictOfErrorMessages.keys():
                        print(cast + "\t", end='')
                    print("")
                    continue
                break

    if errorMessage == None:
        errorMessage = dictOfErrorMessages[castTo]
    
    # Erhalte und verarbeite die Eingabe über das Terminal:
    print(inputRequestText, end='')

    while True:
        input_ = input().strip()
        
        if castTo == 'str':
            return input_
        
        elif castTo == 'bool':
            if input_ == "False":
                return False
            elif input_ == "True":
                return True

            print(errorMessage, end='')

        else:
            try:
                converted = eval("{}(input_)".format(castTo))
                return converted
            except errorType:
                print(errorMessage, end='')

def importModule(module):
    try:
        return importlib.import_module(module)
    except ImportError:
        print("{} not found.}".format(module))

def reloadModule(module):
    importlib.reload(module)


# in klasse
# allgemeine initialisierung des Lautsprechers
# ggf reinitialisierung bei Speakerwechsel (automatische erkennung)
# abprüfen bei Min / max überschreitung

class SystemManager:
    def __init__(self):
        pass


def initDevVolume():
    devices = AudioUtilities.GetSpeakers()
    # print(devices)
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    return volume



def muteVolume():
    setVolume(0)


def setVolume(percent : int):
    volumeRef = initDevVolume()
    volRange = volumeRef.GetVolumeRange()
    print(volRange)
    minVol = volRange[0]
    maxVol = volRange[1]
    
    
    # volSteps = np.linspace(minVol, maxVol, 101)
    # for step in volSteps:
    #     step = np.round(step, 2)
    #     print(step)
    
    vol = minVol + convertFromPercent(percent, retZero=True) * (maxVol - minVol)
    print(f"to set: {vol}")
    volumeRef.SetMasterVolumeLevel(vol, None)

def getVolumePercent():
    volumeRef = initDevVolume()
    volume_dB = volumeRef.GetMasterVolumeLevel()
    # return volume_dB
    return convertToPercent(volume_dB)

def increaseVolume(step):
    currentVol = getVolumePercent()
    setVolume(currentVol + step)
    

def decreaseVolume(step):
    currentVol = getVolumePercent()
    setVolume(currentVol - step)


def testVolInput():
    while 1:
        inp = input("lautstärke in %: ").strip()
        if inp == "q":
            break
        
        try:
            vol = int(inp)
            setVolume(vol)
            print(getVolumePercent())
        except ValueError:
            pass

# umrechnung falsch
def convertToPercent(factor):
    volumeRef = initDevVolume()
    volRange = volumeRef.GetVolumeRange()
    print(volRange)
    minVol = volRange[0]
    maxVol = volRange[1]

    if factor == minVol:
        return 0

    return 10**(2 * (factor - minVol) / (maxVol - minVol))

def convertFromPercent(percent, retZero=False):
    if percent == 0:
        if retZero:
            return 0
        else:
            return None
    
    return np.log10(percent) / 2


if __name__ == '__main__':
    # speaker = Speaker.SA_Speaker("Sprecher", "de")

    # while False:
    #     inp = input("input: ").strip()
    #     if inp == "quit" or inp == "q":
    #         break
    #     elif inp == "reload" or inp == "r":
    #         reloadModule(Speaker)
    #         speaker = Speaker.SA_Speaker("Sprecher", "de")
    #         continue
        
    #     speaker.goodbyePerson("mich")
    #     print("")
    
    goal = 60 # % Lautstärke
    toll = 1

    volumeRef = initDevVolume()
    
    x = np.linspace(0,100, 101, dtype=int)
    y = np.zeros(101)
    # fig, ax = plt.subplots()
    log = False
    while True:
        plt.clf()
        n = 0
        inpt = input("Eingestellt in %: ")
        if inpt == "q":
            break
        


        try:
            n = int(inpt)
            y[n] = getVolumePercent()
        except Exception:
            if inpt == "log":
                log = True
            elif inpt == "notlog":
                log = False
            else:
                continue
        
        vmin, vmax = (volumeRef.GetVolumeRange()[0], volumeRef.GetVolumeRange()[1])

        if log:
            plt.xscale("log")
            plt.yscale("log")
        plt.plot(x, y, ".b")
        plt.pause(1/60)
    
    # for n in x:
    #     print(f"{n}% -> {y[n]}")
    
    
    
    # file = "C:/Users/marti/Documents/VSCode_Workspace/Sprachassistent/SpeakerVolValues.txt"
    # data = np.loadtxt(file)
    # x = data[:,0]
    # y = from_dB(data[:,1])
    # print(x,"\n", y)
    # # plt.xscale("log")
    # # plt.yscale("log")
    # plt.plot(x,y, ".b")
    # plt.show()

    # testVolInput()

    while 0:
        inp = input("Lautstärke ablesen?").strip()
        volumeRef = initDevVolume()
        volRange = volumeRef.GetVolumeRange()
        print(volRange)
        print(np.round(getVolumePercent()), "%\n")
        
# bei BenQ-Speaker: Logarithmischer Ferlauf mit Steigung = Potenz 0.9375?
# -> idee: automatisches Fitten einer Geraden an doppellogarithmische Werteauftragung
# -> daraus umwandlungspotenz bestimmen
# -> bei Standardspeaker halt mit verlust nähern