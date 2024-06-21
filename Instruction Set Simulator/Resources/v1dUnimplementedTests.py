import unittest
import random
from simpleCPU_v1d_SIM.processor_v1d import Processor_v1d as processor

def random8bit():
    return random.randrange(0,255)

def random16bit():
    return random.randrange(0,65535)

class simpleCPUv1dTests(unittest.TestCase):
    
    def testRegDirectOr(self):
        for x in range(10000):
            cpu = processor()
            regValue = random16bit()
            cpu.registers[0] = regValue
            operand = random8bit()
            cpu.memory[0] = int("1101000000000000",2) + operand
            cpu.execute()
            self.assertEqual(cpu.registers[0], regValue | operand)
            
    def testRegRor(self):
        for x in range(10000):
            cpu = processor()
            regValue = random16bit()
            cpu.registers[0] = regValue
            cpu.registers[1] = regValue
            cpu.memory[0] = int("1111000000000101",2)
            cpu.execute()
            for y in range(15):
                cpu.programCounter = 0
                cpu.memory[0] = int("1111010000000100",2)
                cpu.execute()      
            self.assertEqual(cpu.registers[0], cpu.registers[1])
            
    def testRegAdd(self):
        for x in range(10000):
            cpu = processor()
            regValue1 = random16bit()
            regValue2 = random16bit()
            cpu.registers[0] = regValue1
            cpu.registers[1] = regValue2
            cpu.memory[0] = int("1111000100000110",2)
            cpu.execute()   
            self.assertEqual(cpu.registers[0], (regValue1 + regValue2) & 65535)
    
    def testRegSub(self):
        for x in range(10000):
            cpu = processor()
            regValue1 = random16bit()
            regValue2 = random16bit()
            cpu.registers[0] = regValue1
            cpu.registers[1] = regValue2
            cpu.memory[0] = int("1111000100000111",2)
            cpu.execute()   
            self.assertEqual(cpu.registers[0], (regValue1 - regValue2) & 65535)
            
    def testRegAnd(self):
        for x in range(10000):
            cpu = processor()
            regValue1 = random16bit()
            regValue2 = random16bit()
            cpu.registers[0] = regValue1
            cpu.registers[1] = regValue2
            cpu.memory[0] = int("1111000100001000",2)
            cpu.execute()   
            self.assertEqual(cpu.registers[0], (regValue1 & regValue2))
            
    def testRegXor(self):
        for x in range(10000):
            cpu = processor()
            regValue1 = random16bit()
            regValue2 = random16bit()
            cpu.registers[0] = regValue1
            cpu.registers[1] = regValue2
            cpu.memory[0] = int("1111000100001010",2)
            cpu.execute()   
            self.assertEqual(cpu.registers[0], (regValue1 ^ regValue2))
    
    def testRegAsl(self):
        for x in range(10000):
            cpu = processor()
            regValue = random16bit()
            cpu.registers[0] = regValue
            cpu.registers[1] = regValue
            cpu.memory[0] = int("1111000000001011",2)
            cpu.memory[1] = int("1111010000000100",2)
            cpu.execute()
            cpu.execute()  
            self.assertEqual(cpu.registers[0], cpu.registers[1] & 65534)
            
if __name__ == '__main__':
    unittest.main()