class Processor_v1a:
    def __init__(self: object) -> None:
        self.instructionRegister = 0
        self.programCounter = 0
        self.accumulator = 0
        self.memory = [0] * 256
        
    def reset(self: object) -> None:
        self.instructionRegister = 0
        self.programCounter = 0
        self.accumulator = 0
        self.memory = [0] * 256
        
    def loadMem(self: object, file: str) -> None:
        code = open(file, 'r')
        address = 0
        while(address < 256):
            value = code.readline()
            
            if not value:
                break
            
            if(file.endswith('.txt')):
                self.memory[address] = int(value,2) % 65536
                
            elif(file.endswith('.dat')):
                value = value.split(" ")
                self.memory[address] = int(value[1],2) % 65536
            
            address = address + 1
            
    def execute(self: object, numberOfExecutions=1) -> None:
        for x in range(numberOfExecutions):
            self.instructionRegister = self.memory[self.programCounter]
            opcode = int((self.instructionRegister & 61440) / 4096)
            self.pcIncrement()
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
                    
                case 11: #1011 [unused]
                    pass
                
                case 12: #1100 [unused]
                    pass
                
                case 13: #1101 [unused]
                    pass
                
                case 14: #1110 [unused]
                    pass
                
                case 15: #1111 [unused]
                    pass
        
    def pcIncrement(self: object) -> None:
        self.programCounter = (self.programCounter + 1) & 255
        
    def immediate_move(self: object) -> None:
        value = self.instructionRegister & 255
        self.accumulator = value
    
    def immediate_add(self: object) -> None:
        value = self.instructionRegister & 255
        self.accumulator = (self.accumulator + value) & 255
    
    def immediate_sub(self: object) -> None:
        value = self.instructionRegister & 255
        self.accumulator = (self.accumulator - value) & 255
        
    def immediate_and(self: object) -> None:
        value = self.instructionRegister % 256
        self.accumulator = self.accumulator & value
        
    def absolute_load(self: object) -> None:
        address = self.instructionRegister & 255
        self.accumulator = self.memory[address]
        
    def absolute_store(self: object) -> None:
        address = self.instructionRegister & 255
        self.memory[address] = self.accumulator
    
    def absolute_addm(self: object) -> None:
        address = self.instructionRegister & 255
        self.accumulator = (self.accumulator + self.memory[address]) & 255
        
    def absolute_subm(self: object) -> None:
        address = self.instructionRegister & 255
        self.accumulator = (self.accumulator - self.memory[address]) & 255
        
    def direct_jumpU(self: object) -> None:
        address = self.instructionRegister & 255
        self.programCounter = address
        
    def direct_jumpZ(self: object) -> None:
        address = self.instructionRegister & 255
        if(self.accumulator == 0):
            self.programCounter = address
            
    def direct_jumpNZ(self: object) -> None:
        address = self.instructionRegister & 255
        if(self.accumulator != 0):
            self.programCounter = address