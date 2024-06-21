#!/usr/bin/python
import getopt
import sys
import re

#
# MAIN PROGRAM
#

# INSTR   IR15 IR14 IR13 IR12 IR11 IR10 IR09 IR08 IR07 IR06 IR05 IR04 IR03 IR02 IR01 IR00  
# MOVE    0    0    0    0    RD   RD   X    X    K    K    K    K    K    K    K    K
# ADD     0    0    0    1    RD   RD   X    X    K    K    K    K    K    K    K    K
# SUB     0    0    1    0    RD   RD   X    X    K    K    K    K    K    K    K    K
# AND     0    0    1    1    RD   RD   X    X    K    K    K    K    K    K    K    K

# LOAD    0    1    0    0    A    A    A    A    A    A    A    A    A    A    A    A
# STORE   0    1    0    1    A    A    A    A    A    A    A    A    A    A    A    A
# ADDM    0    1    1    0    A    A    A    A    A    A    A    A    A    A    A    A
# SUBM    0    1    1    1    A    A    A    A    A    A    A    A    A    A    A    A

# JUMPU   1    0    0    0    A    A    A    A    A    A    A    A    A    A    A    A
# JUMPZ   1    0    0    1    A    A    A    A    A    A    A    A    A    A    A    A
# JUMPNZ  1    0    1    0    A    A    A    A    A    A    A    A    A    A    A    A
# JUMPC   1    0    1    1    A    A    A    A    A    A    A    A    A    A    A    A  -- NOT IMPLEMENTED

# CALL    1    1    0    0    A    A    A    A    A    A    A    A    A    A    A    A

# OR      1    1    0    1    RD   RD   X    X    K    K    K    K    K    K    K    K
# XOP2    1    1    1    0    RD   RD   X    X    K    K    K    K    K    K    K    K  -- NOT IMPLEMENTED

# RET     1    1    1    1    X    X    X    X    X    X    X    X    0    0    0    0
# MOVE    1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    0    0    1
# LOAD    1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    0    1    0
# STORE   1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    0    1    1   
# ROL     1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    1    0    0

# ROR     1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    1    0    1  -- NOT IMPLEMENTED
# ADD     1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    1    1    0  -- NOT IMPLEMENTED
# SUB     1    1    1    1    RD   RD   RS   RS   X    X    X    X    0    1    1    1  -- NOT IMPLEMENTED
# AND     1    1    1    1    RD   RD   RS   RS   X    X    X    X    1    0    0    0  -- NOT IMPLEMENTED
# OR      1    1    1    1    RD   RD   RS   RS   X    X    X    X    1    0    0    1  -- NOT IMPLEMENTED
# XOR     1    1    1    1    RD   RD   RS   RS   X    X    X    X    1    0    1    0  -- NOT IMPLEMENTED
# ASL     1    1    1    1    RD   RD   RS   RS   X    X    X    X    1    0    1    1  

# XOP3    1    1    1    1    RD   RD   RS   RS   X    X    X    X    1    1    0    0  -- NOT IMPLEMENTED
# XOP4    1    1    1    1    RD   RD   RS   RS   X    X    X    X    1    1    0    1  -- NOT IMPLEMENTED
# XOP5    1    1    1    1    RD   RD   RS   RS   K    K    K    K    1    1    1    0  -- NOT IMPLEMENTED
# XOP6    1    1    1    1    RD   RD   RS   RS   K    K    K    K    1    1    1    1  -- NOT IMPLEMENTED



def simpleCPUv1d_as(argv):

  if len(sys.argv) <= 1:
    print ("Usage: simpleCPUv1d_as.py -i <input_file.asm>")
    print ("                          -o <output_file>") 
    print ("                          -a <address_offset>")
    print ("                          -p <number_of_passes>")
    return

  # init variables #
  version = '1.0'
  source_filename = 'default.asm'
  tmp_filename = 'tmp.asm'
  word_filename = 'default.asc'
  mem_filename = 'default.mem'
  data_filename = 'default.dat' 
  mif_filename = 'default.mif' 

  address = 0
  byte_count = 0

  s_config = 'a:i:o:p:'
  l_config = ['address', 'input', 'output', 'pass']

  input_file_present = False

  instruction_address = 0
  instruction_count   = 0

  label_dictionary = {}

  reg_names = ['ra', 'rb', 'rc', 'rd'];

  # Assembler Mode
  # Mode = 0 : full function, normal two pass
  # Mode = 1 : first pass only, generate tmp.asm file
  # Mode = 2 : second pass only, process "tmp.asm" file

  mode = 0

  # capture commandline options #
  try:
    options, remainder = getopt.getopt(sys.argv[1:], s_config, l_config)
  except getopt.GetoptError as m:
    print ("Error: "+m)
    return

  # extract options #
  for opt, arg in options:
    if opt in ('-o', '--output'):
      if ".asc" in arg:
        word_filename = arg
      elif ".dat" in arg:
        data_filename = arg
      elif ".mem" in arg:
        mem_filename = arg
      else:
        word_filename = arg + ".asc"
        data_filename = arg + ".dat"
        mem_filename = arg + ".mem"
        mif_filename = arg + ".mif"
    elif opt in ('-i', '--input'):
      input_file_present = True
      if ".asm" in arg:
        source_filename = arg
      else:
        source_filename = arg + ".asm"
    elif opt in ('-a', '--address'):
      address = int(arg)
    elif opt in ('-p', '--pass'):
      mode = int(arg)
   
  # exit if no input file present # 
  if input_file_present:

    # open files #
    try:
      source_file = open(source_filename, "r")
    except IOError: 
      print("Error: Input file does not exist.")
      return 

    try:
      word_file = open(word_filename, "w")
      mem_file = open(mem_filename, "w")
      data_file = open(data_filename, "w")
      mif_file = open(mif_filename, "w")
      tmp_file = open(tmp_filename, "w")
    except IOError: 
      print("Error: Could not open output files")
      return 

    # scan through code looking for labels

    if mode != 2:
      instruction_address = address
    
      while True:
        line = source_file.readline()
        if line == '': 
          break
        if line[0] == '\r' or line[0] == '\n' or line[0] =='#':
          continue
        else:
          if ":" in line:
            key = re.sub(':\n', '', ((line.replace(" ", "")).replace("\t", "")).replace("\r", ""))
            label_dictionary[key] = instruction_address
          else:
            text = re.sub('\s+', ' ', line)
            words = text.split(' ')
            if words[1] != "":
              instruction_address += 1  

      #for name in label_dictionary:
      #  print name

      source_file.close()     
      source_file = open(source_filename, "r")

      # generate tmp file with addresses for checking etc#

      instruction_address = address
      while True:
        line = source_file.readline()
        if line == '': 
          break
        if line[0] == '\r' or line[0] == '\n' or line[0] =='#':
          tmp_file.write( line )
        else:
          text = re.sub('\s+', ' ', line)
          words = text.split(' ')
          
          #print words  
          if ":" in text:
            continue
          elif words[1] == '':
            continue
          else:

            outputString = str.format('{:03}', instruction_address) + " "
            instruction_address += 1 

            for i in range(0, len(words)):
              if words[i] in label_dictionary:
                key = words[i]
                outputString = outputString + " " + str(label_dictionary[key])
              else:
                if words[i] != '':
                  outputString = outputString + " " + words[i]

            outputString = outputString + "\n"
            tmp_file.write( outputString )

      # limit test #
      if address >  4095:
        print("Error: program bigger than 4096 instruction limit")
        return 

    tmp_file.close()
  
    if mode == 1:
      print("Exit: first pass complete")
      return
      
    # open TMP file #

    if mode == 2:
      try:
        tmp_file = open(source_filename, "r")
      except IOError: 
        print("Error: could not output temp file")
        return 
    else:
      try:
        tmp_file = open(tmp_filename, "r")
      except IOError: 
        print("Error: could not output temp file")
        return 

    instruction_count = 0
    instruction_address = address

    # write start address to file #
    word_file.write(str.format('{:04X}', instruction_address) + ' ')

    # write mif header to file #

    mif_file.write("DEPTH = 32;           -- The size of memory in words")
    mif_file.write("WIDTH = 16;           -- The size of data in bits")
    mif_file.write("ADDRESS_RADIX = HEX;  -- The radix for address values")
    mif_file.write("DATA_RADIX = BIN;     -- The radix for data values")
    mif_file.write("CONTENT               -- start of (address : data pairs)")
    mif_file.write("BEGIN")

    while True:
      line = tmp_file.readline()
      if line == '':
        break 

      if line[0] =='\r' or line[0] =='\n' or line[0] =='#' or line[0] ==' ':
        pass
      else:
        text = re.sub('\s+', ' ', line.lower())
        words = text.split(' ')

        instr = 0
        imm   = False
        reg   = False
        addr  = False
        data  = False

        #print words
        if words[0].isdigit():

          # match opcode #
          if words[1]   == "move":
            if (words[2] in reg_names) and  (words[3] in reg_names):
              reg = True
              instr = int('1111000000000001', 2)

              if (words[2] == "ra"):
                instr = instr | int('0000000000000000', 2)
              elif (words[2] == "rb"):
                instr = instr | int('0000010000000000', 2)
              elif (words[2] == "rc"):
                instr = instr | int('0000100000000000', 2)
              elif (words[2] == "rd"):
                instr = instr | int('0000110000000000', 2)
              else:
                print("Error: invalid register")
                print(words)
                return

              if (words[3] == "ra"):
                instr = instr | int('0000000000000000', 2)
              elif (words[3] == "rb"):
                instr = instr | int('0000000100000000', 2)
              elif (words[3] == "rc"):
                instr = instr | int('0000001000000000', 2)
              elif (words[3] == "rd"):
                instr = instr | int('0000001100000000', 2)
              else:
                print("Error: invalid register")
                print(words)
                return

            elif (words[2] == "ra"): 
              imm = True
              instr = int('0000000000000000', 2)
            elif (words[2] == "rb"):
              imm = True
              instr = int('0000010000000000', 2)
            elif (words[2] == "rc"):
              imm = True
              instr = int('0000100000000000', 2)
            elif (words[2] == "rd"):
              imm = True
              instr = int('0000110000000000', 2)
            else:
              print("Error: invalid register")
              print(words)
              return
              
          elif words[1] == "add":
            imm = True
            if (words[2] == "ra"): 
              instr = int('0001000000000000', 2)
            elif (words[2] == "rb"):
              instr = int('0001010000000000', 2)
            elif (words[2] == "rc"):
              instr = int('0001100000000000', 2)
            elif (words[2] == "rd"):
              instr = int('0001110000000000', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == "sub":
            imm = True
            if (words[2] == "ra"): 
              instr = int('0010000000000000', 2)
            elif (words[2] == "rb"):
              instr = int('0010010000000000', 2)
            elif (words[2] == "rc"):
              instr = int('0010100000000000', 2)
            elif (words[2] == "rd"):
              instr = int('0010110000000000', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == "and":
            imm = True
            if (words[2] == "ra"): 
              instr = int('0011000000000000', 2)
            elif (words[2] == "rb"):
              instr = int('0011010000000000', 2)
            elif (words[2] == "rc"):
              instr = int('0011100000000000', 2)
            elif (words[2] == "rd"):
              instr = int('0011110000000000', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == "load":
            if (words[2] in reg_names) and  (words[3][1:3] in reg_names):
              reg = True
              instr = int('1111000000000010', 2)    

              if (words[2] == "ra"):
                instr = instr | int('0000000000000000', 2)
              elif (words[2] == "rb"):
                instr = instr | int('0000010000000000', 2)
              elif (words[2] == "rc"):
                instr = instr | int('0000100000000000', 2)
              elif (words[2] == "rd"):
                instr = instr | int('0000110000000000', 2)
              else:
                print("Error: invalid register") 
                print(words)
                return

              if (words[3][1:3] == "ra"):
                instr = instr | int('0000000000000000', 2)
              elif (words[3][1:3] == "rb"):
                instr = instr | int('0000000100000000', 2)
              elif (words[3][1:3] == "rc"):
                instr = instr | int('0000001000000000', 2)
              elif (words[3][1:3] == "rd"):
                instr = instr | int('0000001100000000', 2)
              else:
                print("Error: invalid register") 
                print(words) 
                return

            elif (words[2] == "ra"): 
              addr = True
              instr = int('0100000000000000', 2)
            else:
              print("Error: invalid register") 
              print(words) 
              return

          elif words[1] == "store":
            if (words[2] in reg_names) and  (words[3][1:3] in reg_names):
              #print words[2], words[3][1:3]
              reg = True
              instr = int('1111000000000011', 2)
              if (words[2] == "ra"):
                instr = instr | int('0000000000000000', 2) 
              elif (words[2] == "rb"):
                instr = instr | int('0000010000000000', 2)
              elif (words[2] == "rc"):
                instr = instr | int('0000100000000000', 2)
              elif (words[2] == "rd"):
                instr = instr | int('0000110000000000', 2)
              else:
                print("Error: invalid register") 
                print(words) 
                return

              if (words[3][1:3] == "ra"):
                instr = instr | int('0000000000000000', 2)
              elif (words[3][1:3] == "rb"):
                instr = instr | int('0000000100000000', 2)
              elif (words[3][1:3] == "rc"):
                instr = instr | int('0000001000000000', 2)
              elif (words[3][1:3] == "rd"):
                instr = instr | int('0000001100000000', 2)
              else:
                print("Error: invalid register") 
                print(words) 
                return

            elif (words[2] == "ra"): 
              addr = True
              instr = int('0101000000000000', 2)
            else:
              print("Error: invalid register") 
              print(words) 
              return

          elif words[1] == "addm":
            addr = True
            if (words[2] == "ra"): 
              instr = int('0110000000000000', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == "subm":
            addr = True
            if (words[2] == "ra"): 
              instr = int('0111000000000000', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == "jump":
            addr = True 
            instr = int('1000000000000000', 2)
          elif words[1] == "jumpu":
            addr = True
            instr = int('1000000000000000', 2)
          elif words[1] == "jumpz":
            addr = True
            instr = int('1001000000000000', 2)
          elif words[1] == "jumpnz":
            addr = True
            instr = int('1010000000000000', 2)
          elif words[1] == "call":
            addr = True
            instr = int('1100000000000000', 2)
          elif words[1] == "ret":
            instr = int('1111000000000000', 2)

          elif words[1] == "rol":
            reg = True
            if (words[2] == "ra"): 
              instr = int('1111000000000100', 2)
            elif (words[2] == "rb"):
              instr = int('1111010000000100', 2)
            elif (words[2] == "rc"):
              instr = int('1111100000000100', 2)
            elif (words[2] == "rd"):
              instr = int('1111110000000100', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == "asl":
            reg = True
            if (words[2] == "ra"): 
              instr = int('1111000000001011', 2)
            elif (words[2] == "rb"):
              instr = int('1111010000001011', 2)
            elif (words[2] == "rc"):
              instr = int('1111100000001011', 2)
            elif (words[2] == "rd"):
              instr = int('1111110000001011', 2)
            else:
              print("Error: invalid register") 
              print(words) 
              return

          elif words[1] == "or":
            imm = True
            if (words[2] == "ra"): 
              instr = int('1101000000000000', 2)
            elif (words[2] == "rb"):
              instr = int('1101010000000000', 2)
            elif (words[2] == "rc"):
              instr = int('1101100000000000', 2)
            elif (words[2] == "rd"):
              instr = int('1101110000000000', 2)
            else:
              print("Error: invalid register") 
              print(words)
              return

          elif words[1] == ".data":
            data = True
            instr = int('0000000000000000', 2)
          else:
            print("Error: invalid opcode")
            print(words) 
            return

          length = 0 
          for i in range(len(words)):
            length = length + 1
            if words[i] == "#":
              break
            

          #print reg, imm, addr, data, words, length

          if (length < 3):
            print("Error: invalid operand (len<3)")
            print(words)
            return

          elif (length > 3):
            if (length == 5) and imm:   
              data = words[3].rstrip()     
            elif (length == 5) and addr:
              data = words[3].rstrip()
            elif (length == 4) and addr:
              data = words[2].rstrip()
            elif (length == 4) and data:
              data = words[2].rstrip()
            elif reg:
              data = "0"
            else:
              print("Error: invalid operand (len)")
              print(words) 
              return

            max_addr = 4096
            if imm:
              max_value = 2048

            operand = 0
            if '0x' not in data:
              operand = int(data) 
            else:
              operand = int(data, 16) 

            if addr and (operand > max_addr):
              print("Error: invalid address (>MAX)")
              print(words)
              return

            instr = instr | operand

          #print str.format('{:016b}', instr) 
          data_file.write(str.format('{:04}', instruction_count) + ' ')
          bin_value = str.format('{:016b}', instr) 
          data_file.write( bin_value )
          data_file.write("\n")

          # update EPROM files #
          data_string = str.format('{:04X}', instr ) + ' '
          word_file.write(data_string)

          # update mem file
          mem_file.write('@' + str.format('{:04X}', (instruction_count * 2)) + ' ')
          mem_file.write(data_string[3] + data_string[2] + data_string[1] + data_string[0] + "\n")
          
          #update mif file
          mif_file.write(str.format('{:04}', instruction_count) + ' ')
          mif_file.write( str.format('{:016b}', instr) + ";\n"  )

          instruction_count += 1
          byte_count += 1

          if byte_count == 16:
            byte_count = 0
            word_file.write("\n")

            instruction_address += 16
            addressString = str.format('{:04X}', instruction_address) + ' '
            word_file.write(addressString)

    mif_file.write( "END;\n" )

    # close files #
    source_file.close() 
    word_file.close()
    mem_file.close()
    mif_file.close()
    data_file.close()
    tmp_file.close()

    # display info #
    outputString = "Number of instructions : " + str(instruction_count)
    print( outputString )

    #if instruction_count > 0:
    #  max_address = instruction_count + address - 1
    #outputString = "Address range : " + str(address) + " to " + str(max_address)
    #print( outputString )

  else:
    print("Error: Input file not specified")
    return 

if __name__ == '__main__':
  simpleCPUv1d_as(sys.argv)

