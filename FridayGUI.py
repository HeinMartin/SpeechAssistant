from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image

"""
- Visualisiere Friday: beim sprechen etwas optisches anzeigen (wellen o.Ä.)
- Anzeige, wenn Friday zuhört --> allgmein zustand anzeigen
- Textfeld mit Dialogprotokoll --> ggf dann in Datei speichern
- 
"""

class AssistantGUI:
    def __init__(self, name : str, langugage : str):
        # generiere das Fenster
        # mit allen inhalten (Methoden)

        root = Tk()
        # root.wm_attributes('-fullscreen', 'true')
        root.title("Friday")
        root.geometry("1000x600")

        ## icon ## 
        #root.iconbitmap(<path>)

        dialogBox = Text(root, width=60, height=10)
        dialogBox.grid(row=0, column=0)


        root.mainloop()


    def outputDialog(self, dialog : str, person : str):
        pass

    def animateAssistant(self, talk : str):
        pass

    def animateSpeakingInput(self, speech : str):
        pass


if __name__ == '__main__':
    fridayGUI = AssistantGUI("Friday", "de")

