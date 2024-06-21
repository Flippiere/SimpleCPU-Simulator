def isHex(string):
    for num in string:
        if(not ('0' <= num <= '9' or 'a' <= num <= 'f')):
            return False
    return True

def isDec(string):
    for num in string:
        if(not ('0' <= num <= '9')):
            return False
    return True

def stringToInstructionType(string):
    if(string.lower() in ['ra','rb','rc','rd']):
        return "register"
    elif(string[0:2] == '0x' and isHex(string[2:].lower()) or isDec(string.lower())):
        return "operand"
    
def getAdrModesFromInstrucs(string):
    adrModes = string[string.index("(")+1:string.index(")")].split(",")
    if('' in adrModes):
        adrModes.clear()
    return adrModes

def getAdrModesFromAsm(string):
    adrModesArray = []
    for a in string.split()[2:]:
        adrModesArray.append(stringToInstructionType(a))
    return adrModesArray
        
def getRegValue(string):
    return format(['ra','rb','rc','rd'].index(string.lower()),'02b')

def dynamicAssembler(insSet,asmFile,outputName):
    output = open(outputName,'w')
    for a in open(asmFile):
        if(a.count('#') >= 1):
            a = a[:a.index('#')]
        if(a.strip() == ''):
            continue
        if(a.split()[1] == ".data"):
            if(a.split()[2][0:2] == '0x' and isHex(a.split()[2][2:].lower())):
                output.write(f"{format(int(a.split()[0]),'04')} {format(int(a.split()[2],16)%((2**16)),'016b')}\n")
                continue
            if(isDec(a.split()[2])):
                output.write(f"{format(int(a.split()[0]),'04')} {format(int(a.split()[2],10)%((2**16)),'016b')}\n")
                continue
        for i in open(insSet):
            if(a.split()[1].lower() == i.split(",")[0].lower() and getAdrModesFromAsm(a) == getAdrModesFromInstrucs(i)):
                instruction = i.split(",")[-2]
                for (value, mode) in zip(a.split()[2:], getAdrModesFromAsm(a)):
                    if(mode == "register"):
                        instruction = instruction.replace('RR',getRegValue(value),1)
                    else:
                        bitWidth = instruction.count('K')
                        if(value[0:2] == '0x' and isHex(value[2:].lower())):
                            instruction = instruction.replace(f"{'K' * bitWidth}", format(int(value,16)%((2**(bitWidth))),f"0{bitWidth}b"), 1)
                        elif(isDec(value)):
                            instruction = instruction.replace(f"{'K' * bitWidth}", format(int(value,10)%((2**(bitWidth))),f"0{bitWidth}b"), 1)
                output.write(f"{format(int(a.split()[0]),'04')} {instruction}\n")
                break