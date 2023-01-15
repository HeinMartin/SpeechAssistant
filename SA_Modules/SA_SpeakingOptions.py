

class SA_SpeakingOptions:
    def __init__(self, ttsSpeaker):
        
        self.speaker = ttsSpeaker
        
        # Standardwerte für Sprechrate und -lautstärke
        self.speechVolStep = 0.1 # änderbar über Prozent
        self.speechRateStep = 20
        # alles ausserhalb dieser Werte ist schwachsinnig
        self.maxSpeechRate = 340
        self.minSpeechRate = 60
        
        self.fastSpeechRate = 240
        self.normalSpeechRate = 180
        self.slowSpeechRate = 140

       # Setze Sprechoptionen
    def increaseSpeechVolume(self, step = -1.0):# = self.speechVolStep):
        if (self.speaker).getSpeechVolume() >= (self.speaker).maxSpeechVolume:
            massage = "Ich kann nicht lauter sprechen."
            self.talk(massage)
            return
        
        if step < 0:
            step = self.speechVolStep

        (self.speaker).increaseSpeechVolume(step = step)

        self.confirmCmdExec()

    def decreaseSpeechVolume(self, step = -1.0):# = self.speechVolStep):
        if step < 0:
            step = self.speechVolStep
            
        (self.speaker).decreaseSpeechVolume(step = step)

    def increaseSpeechRate(self, step = -1.0):# = self.speechRateStep):
        if (self.speaker).getSpeechRate() == self.maxSpeechRate:
            massage = "Ich kann nicht schneller sprechen."
            self.talk(massage)
            return
        
        if step < 0:
            step = self.speechRateStep

        if (self.speaker).getSpeechRate() + step >= self.maxSpeechRate:
            (self.speaker).setSpeechRate(self.maxSpeechRate)
        else:
            (self.speaker).increaseSpeechRate(step = step)

        self.confirmCmdExec()

    def decreaseSpeechRate(self, step = -1.0):# = self.speechRateStep):
        if (self.speaker).getSpeechRate() == self.minSpeechRate:
            massage = "Ich kann nicht langsamer sprechen."
            self.talk(massage)
            return
        
        if step < 0:
            step = self.speechRateStep

        if (self.speaker).getSpeechRate() - step <= self.minSpeechRate:
            (self.speaker).setSpeechRate(self.minSpeechRate)
        else:
            (self.speaker).decreaseSpeechRate(step = step)

        self.confirmCmdExec()

    def speakSlowly(self):
        (self.speaker).setSpeechRate(self.slowSpeechRate)

    def speakNormally(self):
        (self.speaker).setSpeechRate(self.normalSpeechRate)

    def speakFast(self):
        (self.speaker).setSpeechRate(self.fastSpeechRate)


