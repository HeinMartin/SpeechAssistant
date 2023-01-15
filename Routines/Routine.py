import sys

sys.path.append("C:\\Users\\marti\\Documents\\VSCode_Workspace\\Sprachassistent\\SA_Modules")
sys.path.append("C:\\Users\\marti\\Documents\\VSCode_Workspace\\Sprachassistent")
import SA_Speaker
import SA_WebManager as SA_WebM

import playsound

class RoutineManager:
    def __init__(self) -> None:
        pass
    def intrudorAlarm(self):
        sa_speaker = SA_Speaker.SA_Speaker("Friday", "de")

        def thiefDefense_exec():
            """ Grillt den Einbrecher durch 1000°C heiße Bodenheizung während epische Kampfmusik spielt! """
            
            msg = "Einbrecher-Abwehr-Protokoll wird ausgeführt"
            sa_speaker.talk(msg)

            # print("Starte epische Kampfmusik!")
            # webManager.openWebsite("https://www.youtube.com/watch?v=P_gcNzSb0OI")
            playsound.playsound('C:\\Users\\marti\\Documents\\VSCode_Workspace\\Sprachassistent\\Routines\\Skyrim_Epic_Battle_Music.mp3', False)
            
            msg = "Haltet ein krimineller Abschaum! Ihr habt gegen das Gesetz verstoßen! Was sagt Ihr zu eurer Verteidigung?"
            sa_speaker.talk(msg)

            # print("Bodenheizung auf 1000°C gesetzt!")
            sa_speaker.talk("Bodenheizung auf 1000°C gesetzt!")

            inp = input("Abbruch: <q>")
            while inp != "q":
                inp = input("Abbruch: <q>")



        cmd = "Einbrecher alarm" # "Starte Einbrecher-Abwehr-Protokoll"
        thiefDefense = Routine("Einbrecher-Abwehr-Protokoll", cmd, thiefDefense_exec)

        # printDict(thiefDefense.describtion(), inline=False)
        thiefDefense.execute()
        # print("Zahl an Argumenten:", thiefDefense.countArgs())

class Routine:
    ## TODO: 
    # Routine sollte bestehen aus:
    # - Bezeichnung / Aufruf
    # - Liste an Ausführungen

    ## sind Routinen == Befehle? oder sind Befehle grundlegender?

    def __init__(self, rName : str, cmd : str, exec) -> None:
        self.name = rName
        self.cmd = cmd
        self.exec = exec
        self.numberOfArgs = self.countArgs()

    def countArgs(self):
        numb = 0
        
        if self.exec.__code__.co_argcount != None:
            numb += self.exec.__code__.co_argcount
        if self.exec.__kwdefaults__ != None:
            numb += self.exec.__kwdefaults__

        return numb


    # def execute(self, params):
    #     self.exec(params)

    def execute(self):
        self.exec()

    def describtion(self):
        return {"Name" : self.name,
                "Aufruf" : f"\"{self.cmd}\"",
                "Ausführung" : self.exec.__doc__.strip()}
        
        # print("Name:", self.name)
        # print("Aufruf:", f"\"{self.cmd}\"")
        # print("Ausführung:", self.exec.__doc__)

    


def printDict(d : dict, inline = True):
    end = "\n"
    if inline:
        end = ", "
    
    for key, value in d.items():
        print(key + " : " + value, end=end)


if __name__ == "__main__":
    def routineExec(call : str):
        """ Schreibe \"{call} ausgefuehrt!\". """
        if call == None or call.strip() == "":
            call = "Routine"
        print(f"{call} ausgeführt!")

    routine = Routine("myRoutine", "aktivieren", routineExec)

    print("Zahl an Argumenten:", routine.countArgs())
    # routine.execute("Order 66")
    # routine.describtion()


    