import os
import sys

import traceback

def findOwnPath():
    return sys.path[0] + "\\"

def separateFileAndDir(path : str):
    length = len(path)
    
    directory = ""
    file = path
    for i in range(0, length):
        pos = length-1 -i
        if path[pos] == "\\" or path[pos] == "/":
            directory = path[0:pos+1]
            file = path[pos+1:length]
            break
    
    return directory, file

def getFileEnding(path : str):
    directory, file = separateFileAndDir(path)
    
    length = len(file)
    
    for i in range(0, length):
        pos = length-1 -i
        if file[pos] == ".":
            return file[pos+1:length]
    return ""

def createFile(path : str, fileName : str):
    try:
        file = open(path+fileName, 'x')
        file.close()
        return 0
    except FileExistsError:
        return -1

def overwriteExistingFile(path, text):
    if checkExistingFile(path) == False:
        return -1
    
    with open(path, 'w') as file:
        file.write(text)
    
    return 0

def checkExistingFile(path : str):
    return os.path.exists(path)

def checkEmptyFile(path : str):
    if checkExistingFile(path) == True:
        size = os.path.getsize(path)
        if size > 0:
            return False

    return True

def addNewLine(path : str, lines : str or list):
    with open(path, 'a+') as file:
        if checkEmptyFile(path) == False:
            file.write("\n")

        # if type(lines) == list
        file.write(lines)

def readFile(path : str):
    with open(path, 'r') as file:
        lines = file.readlines()
        return lines

def printFile(path : str):
    lines = readFile(path)
    for line in lines:
        print(line, end="")
    print("")

def removeFile(path):
    if checkExistingFile(path) == False:
        return -1
    
    os.remove(path)
    return 0

def executeFile(path):
    if checkExistingFile(path) == False:
        return -1
    
    with open(path, 'r') as file:
        exec(file.read())
    
    return 0

if __name__ == '__main__':
    
    filePath = "C:\\Users\\marti\\Documents\\VSCode_Workspace\\Sprachassistent\\"
    fileName = "Test.pdf"

    # filePath = "C:\\Users\\marti\\Documents\\VSCode_Workspace\\"
    # fileName = "TicTacToe.py"
    
    
    
    # line = "Hallo, das ist ein Test \nmit einer neuen Zeile."
    line = """Hallo, das ist ein Test."""
    # createFile(filePath, "Text2.txt")
    
    # r = createFile(filePath, fileName)
    # print(r)
    # addNewLine(filePath + fileName, line)
    # overwriteExistingFile(filePath + fileName, line)
    # printFile(filePath+fileName)
    # print("Executing file:\n")
    # executeFile(filePath + fileName)
    # removeFile(filePath+fileName)

    end = getFileEnding("Was\\auch\\immer\\")
    print(end)

    # print(separateFileAndDir(filePath + fileName))