
def split_and_strip(string : str, splitAt = None, stripOff = None) -> list:
    splitted = string.split(splitAt)
    return [s.strip(stripOff) for s in splitted]

def cast(string : str) -> int or float:
    castList = ["int", "float"]

    for cast in castList:
        try:
            return eval("{}(string)".format(cast))
        except ValueError:
            continue

    raise ValueError

def correctStringElements(string : str, false : str, correct : str) -> str:
        # evtl als tuple {false : correct}
        
        splitted = (string.lower()).split(false)
        print("before correct multi:\n", string, splitted)
        corrected = ""
        length = len(splitted)
        for i in range(length):
            corrected += splitted[i]
            if i != length - 1:
                corrected += correct

        return corrected



recursion = 0
def calcString(toCalc : str, op = '+') -> int or float:
    global recursion
    recursion += 1
    print("\nRekursion:", recursion)

    # toCalc = prepareInputSpeech(toCalc)

    splitted = split_and_strip(toCalc, splitAt=op)
    print("Splitted:", splitted)

    result = 0
    i = 0
    if op == '+':
        while i < len(splitted):
            try:
                if i == 0:
                    result = cast(splitted[0])
                else:
                    result += cast(splitted[i])
                print("i: {}{} -- result = {}".format(i, op, result))
                
            except (ValueError, TypeError):
                if i== 0:
                    result = calcString(splitted[i], op = '-')
                else:
                    result += calcString(splitted[i], op = '-')
            i += 1

    elif op == '-':
        while i < len(splitted):
            try:
                if i == 0:
                    result = cast(splitted[0])
                else:
                    result -= cast(splitted[i])
                print("i: {}{} -- result = {}".format(i, op, result))

            except (ValueError, TypeError):
                if i== 0:
                    result = calcString(splitted[i], op = '*')
                else:
                    result -= calcString(splitted[i], op = '*')
            
            i += 1

    elif op == '*':
        while i < len(splitted):
            print("SPLITTED:", splitted)
            if splitted[0] != '*':
                try:
                    if i == 0:
                        result = cast(splitted[0])
                    else:
                        result *= cast(splitted[i])
                    print("i: {}{} -- result = {}".format(i, op, result))
                    
                except (ValueError, TypeError):
                    if i== 0:
                        result = calcString(splitted[i], op = '/')
                    else:
                        result *= calcString(splitted[i], op = '/')
                i += 1

    elif op == '/':
        while i < len(splitted):
            try:
                if i == 0:
                    result = cast(splitted[0])
                else:
                    result /= cast(splitted[i])
                print("i: {}{} -- result = {}".format(i, op, result))
                
            except (ValueError, TypeError):
                if i== 0:
                    result = calcString(splitted[i], op = '^')
                else:
                    result **= calcString(splitted[i], op = '^')
                
                
            
            i += 1

    elif op == '^':
        while i < len(splitted):

            try:
                if i == 0:
                    result = cast(splitted[0])
                else:
                    result **= cast(splitted[i])
                print("i: {}{} -- result = {}".format(i, op, result))
                
            except (ValueError, TypeError):
                # if i== 0:
                #     result = calcString(splitted[i], op = '*')
                # else:
                #     result **= calcString(splitted[i], op = '*')
                return None
            i += 1

    # print(result)
    return result


def processStringEquation(equation : str, vars : tuple, params : tuple):
    """
    Arguments:
    equation -- string equation 
    var -- tuple: {<var> : <value(s)>}
    params -- tuple: {<var> : <value(s)>}, if multiple values, than arrays for each value will be returned
    """
    #equation = "3 * x + 3 - a"

    correctStringElements(equation, )



if __name__ == '__main__':
    pass