import unittest
from simpleCPU_v1a_SIM.processor_v1a import Processor_v1a as processor

class simpleCPUv1aTests(unittest.TestCase):
    
    def testMove(self):
        cpu = processor()
        cpu.loadMem('Resources/tests/v1aTests/v1a_move_test.dat')
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xff",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x80",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x08",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x7f",16))
        
    def testAdd(self):
        cpu = processor()
        cpu.loadMem('Resources/tests/v1aTests/v1a_add_test.dat')
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x0f",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x1e",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x2d",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x2c",16))
        
    def testSub(self):
        cpu = processor()
        cpu.loadMem('Resources/tests/v1aTests/v1a_sub_test.dat')
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x05",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x03",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xfa",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xfb",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xfb",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xda",16))
        
    def testAnd(self):
        cpu = processor()
        cpu.loadMem('Resources/tests/v1aTests/v1a_and_test.dat')
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xaa",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xaa",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x0a",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        
    def testJump(self):
        cpu = processor()
        cpu.loadMem('Resources/tests/v1aTests/v1a_jump_test.dat')
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x05",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x06",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x07",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x08",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x05",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x06",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x03",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x04",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x01",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x02",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x01",16))
        cpu.execute()
        self.assertEqual(cpu.programCounter, int("0x02",16))
        
    def testMem(self):
        cpu = processor()
        cpu.loadMem('Resources/tests/v1aTests/v1a_mem_test.dat')
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x7f",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x7f",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x31",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x31",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x7f",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xff",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xff",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xfe",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0xff",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x01",16))
        cpu.execute()
        self.assertEqual(cpu.accumulator, int("0x00",16))
        
if __name__ == '__main__':
    unittest.main()