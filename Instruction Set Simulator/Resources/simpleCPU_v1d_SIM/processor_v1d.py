#!/usr/bin/env pypy

class Processor_v1d:   
    def __init__(self: object) -> None:
        self.instructionRegister = 0
        self.programCounter = 0
        self.pcLifoStack = [0,0,0,0]
        self.pcPointer = 0
        self.registers = [0] * 4
        self.memory = [0] * 4096
        
        self.zero = 0
        self.carry = 0
        self.overflow = 0
        self.positive = 0
        self.negative = 0
        
        # value equivalent to '1111000000000000' that can be used to isolate the opcode with an '&' operation
        self.leftOpcodeMask = int((2 ** 16) - (2 ** (16 - 4)))
        
        # value equivalent to '0000110000000000' that can be used to isolate the register with an '&' operation
        self.registerMask = int((2 ** (16 - 4)) - (2 ** (16 - 4 - 2)))
        
        # value equivalent to '0000001100000000' that can be used to isolate the register with an '&' operation
        self.register2Mask = int((2 ** (16 - 4 - 2)) - (2 ** (16 - 4 - 2 - 2)))
        
    def reset(self: object) -> None:
        self.instructionRegister = 0
        self.programCounter = 0
        self.pcLifoStack = [0,0,0,0]
        self.pcPointer = 0
        self.registers = [0] * 4
        self.memory = [0] * 4096
        
        self.zero = 0
        self.carry = 0
        self.overflow = 0
        self.positive = 0
        self.negative = 0
        
    def loadMem(self: object, file: str) -> None:
        code = open(file, 'r')
        address = 0
        while(address < len(self.memory) - 1):
            value = code.readline()
            
            if not value:
                break
            
            if(file.endswith('.txt')):
                self.memory[address] = int(value,2) % 65536
                
            elif(file.endswith('.dat')):
                value = value.split(" ")
                self.memory[address] = int(value[1],2) % 65536
            
            address = address + 1
         
    def execute(self: object, noOfExecutions=1) -> None:
        for x in range(noOfExecutions):
            self.instructionRegister = self.memory[self.programCounter]
            opcode = self.instructionRegister >> 12
            self.programCounter = (self.programCounter + 1) & 4095
            match opcode:
                case 0: #0000 [immediate]
                    self.immediate_move()
                    
                case 1: #0001 [immediate]
                    self.immediate_add()
                    
                case 2: #0010 [immediate]
                    self.immediate_sub()
                    
                case 3: #0011 [immediate]
                    self.immediate_and()
                    
                case 4: #0100 [absolute]
                    self.absolute_load()
                    
                case 5: #0101 [absolute]
                    self.absolute_store()
                    
                case 6: #0110 [absolute]
                    self.absolute_addm()
                    
                case 7: #0111 [absolute]
                    self.absolute_subm()
                    
                case 8: #1000 [direct]
                    self.direct_jumpU()
                    
                case 9: #1001 [direct]
                    self.direct_jumpZ()
                    
                case 10: #1010 [direct]
                    self.direct_jumpNZ()
                    
                case 11: #1011 [direct]
                    self.direct_jumpC()
                    
                case 12: #1100 [direct]
                    self.direct_call()
                    
                case 13: #1101 [immediate]
                    self.immediate_or()
                    
                case 14: #1110 [immediate]
                    self.immediate_xop1()
                    
                case 15: #1111
                    #All instruction with left and right opcode bits
                    opcode = self.instructionRegister & 15
                    match opcode:
                        case 0: #1111 + 0000 [direct]
                            self.direct_ret()
                            
                        case 1: #1111 + 0001 [register]
                            self.register_move()
                            
                        case 2: #1111 + 0010 [register indirect]
                            self.register_indirect_load()
                            
                        case 3: #1111 + 0011 [register indirect]
                            self.register_indirect_store()
                            
                        case 4: #1111 + 0100 [register]
                            self.register_rol()
                            
                        case 5: #1111 + 0101 [register]
                            self.register_ror()
                            
                        case 6: #1111 + 0110 [register]
                            self.register_add()
                            
                        case 7: #1111 + 0111 [register]
                            self.register_sub()
                            
                        case 8: #1111 + 1000 [register]
                            self.register_and()
                            
                        case 9: #1111 + 1001 [register]
                            self.register_or()
                            
                        case 10: #1111 + 1010 [register]
                            self.register_xor()
                            
                        case 11: #1111 + 1011 [register]
                            self.register_asl()
                            
                        case 12: #1111 + 1100 [register indirect]
                            self.register_indirect_xop2()
                        
                        case 13: #1111 + 1101 [register]
                            self.register_xop3()
                        
                        case 14: #1111 + 1110 [register indirect]
                            self.register_indirect_xop4()
                            
                        case 15: #1111 + 1111 [register]
                            self.register_xop5()

    #CPU FUNCTIONS
        
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