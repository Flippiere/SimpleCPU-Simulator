from simpleCPU_v1d_Custom_ISA_SIM import processorInstructions

class Processor:   
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
            
    def loadInstructions(self:object, file:str) -> None:
        instructions = open(file).readlines()
        array = []
        for line in instructions:
            if(line == '\n'):
                array.append("None")
            else:
                array.append(f"{line.split(',')[-1][:-1]}_{line.split(',')[0]}")
                
        self.instructions = array
                
        
         
    def execute(self: object, noOfExecutions=1) -> None:
        for x in range(noOfExecutions):
            
            self.instructionRegister = self.memory[self.programCounter]
            
            opcode = self.instructionRegister >> 12
            if(opcode == 15):
                opcode = opcode + (self.instructionRegister & 15)
                
            instruction = self.instructions[opcode]
            
            self.programCounter = (self.programCounter + 1) & 4095
            match instruction:
                case 'immediate_move':
                    processorInstructions.immediate_move(self)
                    
                case 'immediate_add':
                    processorInstructions.immediate_add(self)
                    
                case 'immediate_sub':
                    processorInstructions.immediate_sub(self)
                    
                case 'immediate_and':
                    processorInstructions.immediate_and(self)
                    
                case 'absolute_load':
                    processorInstructions.absolute_load(self)
                    
                case 'absolute_store':
                    processorInstructions.absolute_store(self)
                    
                case 'absolute_addm':
                    processorInstructions.absolute_addm(self)
                    
                case 'absolute_subm':
                    processorInstructions.absolute_subm(self)
                    
                case 'direct_jumpU':
                    processorInstructions.direct_jumpU(self)
                    
                case 'direct_jumpZ':
                    processorInstructions.direct_jumpZ(self)
                    
                case 'direct_jumpNZ':
                    processorInstructions.direct_jumpNZ(self)
                    
                case 'direct_jumpC':
                    processorInstructions.direct_jumpC(self)
                    
                case 'direct_call':
                    processorInstructions.direct_call(self)
                    
                case 'immediate_or':
                    processorInstructions.immediate_or(self)
                    
                case 'direct_ret':
                    processorInstructions.direct_ret(self)
                    
                case 'register_move':
                    processorInstructions.register_move(self)
                    
                case 'register_indirect_load':
                    processorInstructions.register_indirect_load(self)
                
                case 'register_indirect_store':
                    processorInstructions.register_indirect_store(self)
                
                case 'register_rol':
                    processorInstructions.register_rol(self)
                
                case 'register_ror':
                    processorInstructions.register_ror(self)
                
                case 'register_add':
                    processorInstructions.register_add(self)
                
                case 'register_sub':
                    processorInstructions.register_sub(self)
                
                case 'register_and':
                    processorInstructions.register_and(self)
                
                case 'register_or':
                    processorInstructions.register_or(self)
                
                case 'register_xor':
                    processorInstructions.register_xor(self)
                
                case 'register_asl':
                    processorInstructions.register_asl(self)
                
                case 'immediate_mul':
                    processorInstructions.immediate_mul(self)
                
                case 'immediate_div':
                    processorInstructions.immediate_div(self)
                
                case 'immediate_mod':
                    processorInstructions.immediate_mod(self)
                
                case 'immediate_xor':
                    processorInstructions.immediate_xor(self)
                
                case 'immediate_rol':
                    processorInstructions.immediate_rol(self)
                
                case 'immediate_ror':
                    processorInstructions.immediate_ror(self)
                
                case 'immediate_asl':
                    processorInstructions.immediate_asl(self)
                
                case 'immediate_nop':
                    processorInstructions.immediate_nop(self)
                
                case 'absolute_nop':
                    processorInstructions.absolute_nop(self)
                
                case 'direct_nop':
                    processorInstructions.direct_nop(self)
                
                case 'register_nop':
                    processorInstructions.register_nop(self)
                
                case 'register_indirect_nop':
                    processorInstructions.register_indirect_nop(self)
                
                case 'direct_sec':
                    processorInstructions.direct_sec(self)
                
                case 'direct_sez':
                    processorInstructions.direct_sez(self)
                
                case 'direct_retnp':
                    processorInstructions.direct_retnp(self)
                
                case 'register_mul':
                    processorInstructions.register_mul(self)
                
                case 'register_div':
                    processorInstructions.register_div(self)
                
                case 'register_mod':
                    processorInstructions.register_mod(self)
                
                case 'register_rol8':
                    processorInstructions.register_rol8(self)
                
                case 'register_asl8':
                    processorInstructions.register_asl8(self)
                
                case 'direct_clrLifo':
                    processorInstructions.direct_clrLifo(self)
                
                case 'immediate_xop1':
                    processorInstructions.immediate_xop1(self)
                
                case 'register_indirect_xop2':
                    processorInstructions.register_indirect_xop2(self)
                
                case 'register_xop3':
                    processorInstructions.register_xop3(self)
                
                case 'register_indirect_xop4':
                    processorInstructions.register_indirect_xop4(self)
                
                case 'register_xop5':
                    processorInstructions.register_xop5(self)
                    
                case 'None':
                    pass
