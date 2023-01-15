#import SystemManager as sm
import SA_Speaker
import Math
import numpy as np

class SA_Math:
    def __init__(self, sa_name = "Friday", sa_language = "de"):
        
        self.name = sa_name
        self.tts_lang = sa_language

        self.sa_speaker = SA_Speaker.SA_Speaker(self.name, self.tts_lang)

        self.conf_not = 0 #"not"
        self.conf_before = 1 #"before"
        self.conf_after = 2 #"after"

        _before = self.conf_before
        _after = self.conf_after
        _not = self.conf_not
        # Alle { Befehle: <Befehl> : [<ausführende Methode>, <Aktion bestätigen>] }
        self.commands_0Arg = {}
        self.commands_1Arg = {
                            # "Rechner" : [self.doAll, _not],
                            "rechne" : [self.doAll, _not]
                            }

    def shareCmds_dict(self) -> dict:
        return {0 : self.commands_0Arg, 1 : self.commands_1Arg}

    def speakDecimals(self, speech : str, idxDec : int) -> str:

        i = idxDec + 2
        length = len(speech)

        while i < length:
            print("dec:\n\t", i, speech)
            try:
                Math.cast(speech[i])

                if i == length-1:
                    speech = speech[0:i] + " " + speech[-1]
                else:
                    speech = speech[0:i] + " " + speech[i:]
                
                length = len(speech)
                i += 2
            except:
                break


        return speech

    def prepareOuputSpeech(self, speech : str) -> str:
        
        length = len(speech)
        i = 0
        while i < length:
            print(i, len(speech), speech)
            subst = ""
            if speech[i] == "*":
                subst = "mal"
            elif speech[i] == "/":
                subst = "durch"
            elif speech[i] == "-":
                subst = "minus"
            elif speech[i] == ".":
                subst = "komma"
            elif speech[i] == "^":
                subst = "hoch"

                speech = self.speakDecimals(speech, i)

            else:
                i += 1
                continue
            
        
            speech = speech[0:i] + subst + speech[i+1:]
            length = len(speech)

            i += 1
        
        return speech

    def prepareInputSpeech(self, speech : str) -> str:
        # delete unnecessary string fragments
        try:
            Math.cast(speech.strip()[0])
        except ValueError:
            if speech.strip()[0] != "-":
                speech = speech[1:].strip()
        

        # Multiplication sign
        speech = Math.correctStringElements(speech, "x", "*")
        # decimal dot
        speech = Math.correctStringElements(speech, ",", ".")
        # power sign
        speech = Math.correctStringElements(speech, "hoch", "^")
        speech = Math.correctStringElements(speech, "**", "^")

        return speech



    def returnResult(self, speech : str, result : float):
        # print(res)
        speechSpeak = self.prepareOuputSpeech(speech)
        resultSpeak = self.prepareOuputSpeech(str(result))
        
        print("Output: {} = {}".format(speech, str(result)))
        
        speakOut = "{} ergibt {}".format(speechSpeak, resultSpeak)
        printOut = "{} ergibt {}".format(speech, result)


        self.sa_speaker.talk(speakOut, specialOutput = printOut)


    def doAll(self, speech : str):
        print("Aufbereitung:")
        speech = self.prepareInputSpeech(speech)
        print("korrigiert:", speech)

        print("\nBerechnung:")
        res = Math.calcString(speech)
        
        print("\nWidergabe:")
        self.returnResult(speech, res)



if __name__ == '__main__':
    m = SA_Math()

    # s = " 3 +20"

    # m.doAll(s)

    ## Versuch, händisch die Rechnungen aus Zeichenketten zu erhalten und auszuführen.
    """ A:
    5 * 3 + 7 / 2       || +
    [5 * 3], '+', [7 / 2]   || /
    [[5 * 3]], '+', [[7], '/', [2]]   || *
    [[[5], '*', [3]]], '+', [[[7], '/', [2]]]
    """
    """ B:
    5 * 3 + 7 / 2   || + 
    [5 * 3], '+', [7 / 2]   || <
    5 * 3       |   7 / 2   || * | /       (+)
    [5], '*', [3]       |   [7], '/', [2]           (+)
    15 r        |       3.5 r           (+)
    [15], '+', [3.5]
    18.5 r


    speech aufteilen
    iterieren über jedes aufgeteilte, und nach weiterer Operatrion aufteilen
    etc.
    Zahlen erhalten
    Operationen revers anwenden  // Operationen zahlen hinzufügen und python selbst rechnen lassen

    alternativ:
    - teile speech bei jedem leerzeichen und speichere in <splitted>
    - caste Zahlen
    - führe direkt 
    gehe über jedes Element im String
    - 


    """




    ops = ['-', '+', '/', '*']
    ops_inv = ['*', '/', '+', '-']
    
    #speech = "5,3 * 3 + 7 / 2"
    speech = "2 - 3**3 / 1"
    # convert all kommas to dots
    # speech = m.correctFloats(speech)

    
    print(speech)
    m.doAll(speech)



    
