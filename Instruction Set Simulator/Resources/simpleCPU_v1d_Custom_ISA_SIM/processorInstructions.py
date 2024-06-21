def immediate_move(self: object) -> None:
    value = self.instructionRegister & 255
    if(value >= 128):
        value = value + int((2 ** 16) - (2 ** (16 - 8)))
    register = (self.instructionRegister & self.registerMask) >> 10
    self.registers[register] = value

def immediate_add(self: object) -> None:
    value = self.instructionRegister % 256
    if(value >=128):
        value = value + int((2 ** 16) - (2 ** (16 - 8)))
    register = (self.instructionRegister & self.registerMask) >> 10
    if((self.registers[register] + value) >= (2 ** 16)):
        self.carry = 1
    else:
        self.carry = 0
    result = (self.registers[register] + value) & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result

def immediate_sub(self: object) -> None:
    value = self.instructionRegister & 255
    if(value >= 128):
        value = value + int((2 ** 16) - (2 ** (16 - 8)))
    register = (self.instructionRegister & self.registerMask) >> 10
    if((self.registers[register] - value) < 0):
        self.carry = 0
    else:
        self.carry = 0
    result = (self.registers[register] - value) % (2 ** 16)
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result
    
def immediate_and(self: object) -> None:
    value = self.instructionRegister & 255
    register = (self.instructionRegister & self.registerMask) >> 10
    result = self.registers[register] & value
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.carry = 0
    self.registers[register] = result
    
def absolute_load(self: object) -> None:
    address = self.instructionRegister & 4095
    self.registers[0] = self.memory[address]
    
def absolute_store(self: object) -> None:
    address = self.instructionRegister & 4095
    self.memory[address] = self.registers[0]

def absolute_addm(self: object) -> None:
    address = self.instructionRegister & 4095
    if((self.registers[0] + self.memory[address]) >= (2 ** 16)):
        self.carry = 1
    else:
        self.carry = 0
    result = (self.registers[0] + self.memory[address]) & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[0] = result
    
def absolute_subm(self: object) -> None:
    address = self.instructionRegister & 4095
    if((self.registers[0] + self.memory[address]) < 0):
        self.carry = 0
    else:
        self.carry = 0
    result = (self.registers[0] - self.memory[address]) & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[0] = result
    
def direct_jumpU(self: object) -> None:
    address = self.instructionRegister & 4095
    self.programCounter = address
    
def direct_jumpZ(self: object) -> None:
    address = self.instructionRegister & 4095
    if(self.zero == 1):
        self.programCounter = address
        
def direct_jumpNZ(self: object) -> None:
    address = self.instructionRegister & 4095
    if(self.zero == 0):
        self.programCounter = address
        
def direct_jumpC(self: object) -> None:
    address = self.instructionRegister & 4095
    if(self.carry == 1):
        self.programCounter = address
        
def direct_call(self: object) -> None:
    address = self.instructionRegister & 4095
    self.pcLifoStack[self.pcPointer] = self.programCounter
    self.programCounter = address
    self.pcPointer = (self.pcPointer + 1) % 4
    
def immediate_or(self: object) -> None:
    value = self.instructionRegister & 255
    register = (self.instructionRegister & self.registerMask) >> 10
    result = self.registers[register] | value
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.carry = 0
    self.registers[register] = result
    
def direct_ret(self: object) -> None:
    self.pcPointer = (self.pcPointer - 1) % 4
    address = self.pcLifoStack[self.pcPointer]
    self.programCounter = address    
    
def register_move(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    self.registers[destinationRegister] = self.registers[sourceRegister]
    
def register_indirect_load(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    self.registers[destinationRegister] = self.memory[self.registers[sourceRegister] & 4095]
    
def register_indirect_store(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    self.memory[self.registers[sourceRegister] & 4095] = self.registers[destinationRegister]
    
def register_rol(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    newValue = self.registers[destinationRegister] << 1
    if(newValue >= (2 ** 16)):
        newValue = newValue + 1
        self.carry = 1
    else:
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def register_ror(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    if(self.registers[destinationRegister] % 2 == 1):
        newValue = (self.registers[destinationRegister] >> 1) + 2 ** 15
        self.carry = 1
    else:
        newValue = (self.registers[destinationRegister] >> 1)
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def register_add(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    result = self.registers[sourceRegister] + self.registers[destinationRegister]
    if(result >= (2 ** 16)):
        result = result & 65535
        self.carry = 1
    else:
        self.carry = 0
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def register_sub(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    result = self.registers[destinationRegister] - self.registers[sourceRegister]
    if(result < 0):
        result = result & 65535
        self.carry = 0
    else:
        self.carry = 0
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def register_and(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    result = self.registers[sourceRegister] & self.registers[destinationRegister]
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.carry = 0
    self.registers[destinationRegister] = result
    
def register_or(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    result = self.registers[sourceRegister] | self.registers[destinationRegister]
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.carry = 0
    self.registers[destinationRegister] = result

def register_xor(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    result = self.registers[destinationRegister] ^ self.registers[sourceRegister]
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.carry = 0
    self.registers[destinationRegister] = result
    
def register_asl(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    result = self.registers[destinationRegister] << 1
    if(result >= (2 ** 16)):
        result = result & 65535
        self.carry = 1
    else:
        self.carry = 0
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def immediate_xop1(self: object) -> None:
    pass

def register_indirect_xop2(self: object) -> None:
    pass

def register_xop3(self: object) -> None:
    pass

def register_indirect_xop4(self: object) -> None:
    pass

def register_xop5(self: object) -> None:
    pass
    
#New Instructions 

#Multiplies a register value by a given 8-bit value
def immediate_mul(self: object) -> None:
    value = self.instructionRegister & 255
    register = (self.instructionRegister & self.registerMask) >> 10
    if((self.registers[register] * value) >= (2 ** 16)):
        self.carry = 1
    else:
        self.carry = 0
    result = (self.registers[register] * value) & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result

#Divides a register value by a given 8-bit value
def immediate_div(self: object) -> None:
    value = self.instructionRegister & 255
    register = (self.instructionRegister & self.registerMask) >> 10
    if(value == 0):
        self.registers[register] = 65535
    else:
        if((self.registers[register] / value) - (self.registers[register] // value) > 0):
            self.carry = 1
        else:
            self.carry = 0
        result = (self.registers[register] // value) & 65535
        if(result == 0):
            self.zero = 1
        else:
            self.zero = 0
        self.registers[register] = result
    
#Performs Modulo on a register with a given 8-bit value
def immediate_mod(self: object) -> None:
    value = self.instructionRegister & 255
    register = (self.instructionRegister & self.registerMask) >> 10
    if(value == 0):
        self.registers[register] = 0
    else:
        if((self.registers[register] / value) >= 1):
            self.carry = 1
        else:
            self.carry = 0
        result = (self.registers[register] % value) & 65535
        if(result == 0):
            self.zero = 1
        else:
            self.zero = 0
        self.registers[register] = result
    
def immediate_xor(self: object) -> None:
    value = self.instructionRegister & 255
    register = (self.instructionRegister & self.registerMask) >> 10
    self.carry = 0
    result = (self.registers[register] ^ value) & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result

#version of the rol instruction that lets the user specify how many spaces are shifted    
def immediate_rol(self: object) -> None:
    value = self.instructionRegister & 15
    register = (self.instructionRegister & self.registerMask) >> 10
    newValue = self.registers[register] << value
    if(newValue >= (2 ** 16)):
        newValue = (newValue & ((2 ** 16) - 1)) + (newValue // (2 ** 16))
        self.carry = 1
    else:
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result

#version of the ror instruction that lets the user specify how many spaces are shifted 
def immediate_ror(self: object) -> None:
    value = self.instructionRegister & 15
    register = (self.instructionRegister & self.registerMask) >> 10
    newValue = (self.registers[register] >> value) + (self.registers[register] >> (16 - value))
    if(newValue >= (2 ** 16)):
        self.carry = 1
    else:
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result

#version of the asl instruction that lets the user specify how many spaces are shifted      
def immediate_asl(self: object) -> None:
    value = self.instructionRegister & 16
    register = (self.instructionRegister & self.registerMask) >> 10
    newValue = self.registers[register] << value
    if(newValue >= (2 ** 16)):
        self.carry = 1
    else:
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[register] = result
    
#No operation
def immediate_nop(self: object) -> None:
    pass

#No operation
def absolute_nop(self: object) -> None:
    pass

#No operation
def direct_nop(self: object) -> None:
    pass

#No operation
def register_nop(self: object) -> None:
    pass

#No operation
def register_indirect_nop(self: object) -> None:
    pass

#Sets the Carry flag
def direct_sec(self: object) -> None:
    self.carry = (self.instructionRegister & 2048) >> 11

#Sets the Zero flag
def direct_sez(self: object) -> None:
    self.zero = (self.instructionRegister & 2048) >> 11
    
#Pops Lifo Stack, without jumping to address
def direct_pop(self: object) -> None:
    self.pcPointer = (self.pcPointer - 1) % 4
    
#Return witout popping the lifo stack
def direct_retnp(self: object) -> None:
    address = self.pcLifoStack[self.pcPointer]
    self.programCounter = address    
    
def register_mul(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    result = self.registers[sourceRegister] * self.registers[destinationRegister]
    if(result >= (2 ** 16)):
        result = result & 65535
        self.carry = 1
    else:
        self.carry = 0
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def register_div(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    if(self.registers[sourceRegister] == 0):
        self.registers[destinationRegister] = 65535
    else:
        result = self.registers[destinationRegister] // self.registers[sourceRegister]
        if((self.registers[destinationRegister] / self.registers[sourceRegister]) - result > 0):
            self.carry = 1
        else:
            self.carry = 0
        if(result == 0):
            self.zero = 1
        else:
            self.zero = 0
        self.registers[destinationRegister] = result & 65535
        
def register_mod(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    sourceRegister = (self.instructionRegister & self.register2Mask) >> 8
    if(self.registers[sourceRegister] == 0):
        self.registers[destinationRegister] = 0
    else:
        result = self.registers[destinationRegister] % self.registers[sourceRegister]
        if((self.registers[destinationRegister] / self.registers[sourceRegister]) > 1):
            self.carry = 1
        else:
            self.carry = 0
        if(result == 0):
            self.zero = 1
        else:
            self.zero = 0
        self.registers[destinationRegister] = result & 65535

#Rolls a given register left 8 times
def register_rol8(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    newValue = self.registers[destinationRegister] << 8
    if(newValue >= (2 ** 16)):
        newValue = (newValue & ((2 ** 16) - 1)) + (newValue // (2 ** 16))
        self.carry = 1
    else:
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result

#Performs an arithemtic shift left that shifts 8 bits on a given register
def register_asl8(self: object) -> None:
    destinationRegister = (self.instructionRegister & self.registerMask) >> 10
    newValue = self.registers[destinationRegister] << 8
    if(newValue >= (2 ** 16)):
        self.carry = 1
    else:
        self.carry = 0
    result = newValue & 65535
    if(result == 0):
        self.zero = 1
    else:
        self.zero = 0
    self.registers[destinationRegister] = result
    
def direct_clrLifo(self: object) -> None:
    self.pcLifoStack = [0,0,0,0]
    
#   This instruction has been removed due to not adhering to the principles of simpleCPU - only one register is normally written to in a cycle        
#    def register_clrReg(self: object) -> None:
#        self.registers = [0] * 4