import argparse
import time
from Resources.simpleCPU_v1a_SIM.processor_v1a import Processor_v1a as cpuA
from Resources.simpleCPU_v1d_SIM.processor_v1d import Processor_v1d as cpuD

def haltCheck(cpu) -> bool:
    if(cpu.memory[cpu.programCounter] >> 12 == 8 and cpu.memory[cpu.programCounter] & 4095 == cpu.programCounter):
        return True
    elif(cpu.memory[cpu.programCounter] == 0 and cpu.memory[cpu.programCounter + 1] == 0):
        return True
    else:
        return False
    
def main():
    parser = argparse.ArgumentParser(description = "SimpleCPU Simulator")

    parser.add_argument("-i", "--input", type = str, nargs = 1,
                        metavar = "input_file", default = None,
                        help = "Opens and reads the specified text file.")
    
    parser.add_argument("-o", "--output", type = str, nargs = 1,
                        metavar = "output_name", default = None,
                        help = "Name of file wrote to.")
    
    parser.add_argument("-v", "--version", type = str, nargs = 1,
                        metavar = "version", default = None,
                        help = "Version of SimpleCPU to be used.")
    
    parser.add_argument("-c", "--cycles", type = str, nargs = 1,
                        metavar = "cycles", default = None,
                        help = "Number of cycles to be executed")
     
    args = parser.parse_args()
    
    if(args.version == None or args.version[0].lower() == "v1d"):
        halt = False
        cpu = cpuD()
        cpu.loadMem(args.input[0])
        cycles = 0
        startTime = time.time()
        if(args.cycles == None):
            while(not halt):
                cpu.execute()
                halt = haltCheck(cpu)
                cycles = cycles + 1
        else:
            cpu.execute(noOfExecutions=int(args.cycles[0]))
            cycles = args.cycles[0] 
        endTime = time.time()
        print(cpu.registers)
        print(f"Instruction Count: {cycles}")
        print(f"Time Taken: {endTime - startTime}")
        
    elif(args.version[0].lower() == "v1a"):
        halt = False
        cpu = cpuA()
        cpu.loadMem(args.input[0])
        cycles = 0
        startTime = time.time()
        if(args.cycles == None):
            while(not halt):
                cpu.execute()
                halt = haltCheck(cpu)
                cycles = cycles + 1
        else:
            cpu.execute(numberOfExecutions=int(args.cycles[0]))
            cycles = args.cycles[0] 
        endTime = time.time()
        print(f"Accumulator: {cpu.accumulator}")
        print(f"Instruction Count: {cycles}")
        print(f"Time Taken: {endTime - startTime}")
        
    else:
        print("invalid simpleCPU version")
        
    if(args.output != None):
        file = open(args.output[0],"w")
        for x in range(len(cpu.memory)):
            file.write(f"{format(x,'04')} {format(cpu.memory[x],'016b')}\n")
    
if __name__ == "__main__":
    main()