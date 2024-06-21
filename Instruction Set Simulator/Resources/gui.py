import copy
import subprocess
import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
import time
import simpleCPUv1d_as as assembler
import dynamicAssembler

from simpleCPU_v1a_SIM.processor_v1a import Processor_v1a as cpuA
from simpleCPU_v1d_SIM.processor_v1d import Processor_v1d as cpuD
from simpleCPU_v1d_Custom_ISA_SIM.customProcessor import Processor as cpuCustom

registerAddressing = ["immediate","immediate","immediate","immediate",
                      "absolute","absolute","absolute","absolute",
                      "direct","direct","direct","direct",
                      "direct","immediate","immediate","direct",
                      "register","register_indirect","register_indirect","register",
                      "register","register","register","register",
                      "register","register","register","register_indirect",
                      "register","register_indirect","register",]


class App:
    def __init__(self, root):
        root.title("SimpleCPUSim")
        width=720
        height=550
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        self.cycles = 0
        self.running = False
        self.selected = ""
        self.cpu = cpuA()
        self.speedT = 0
        self.input = 0
        self.lastInput = 0
        self.alphabet = ['A','B','C','D']
        self.GPIOConnected = False
        
        versionLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        versionLabel["font"] = ft
        versionLabel["fg"] = "#333333"
        versionLabel["text"] = "SimpleCPU version:"
        versionLabel.place(x=20,y=10,width=140,height=50)
        
        memoryLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        memoryLabel["font"] = ft
        memoryLabel["fg"] = "#333333"
        memoryLabel["text"] = "Memory:"
        memoryLabel.place(x=461,y=53,width=140,height=50)
        
        registerLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        registerLabel["font"] = ft
        registerLabel["fg"] = "#333333"
        registerLabel["text"] = "Registers:"
        registerLabel.place(x=218,y=53,width=140,height=50)
        
        instRegisterLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        instRegisterLabel["font"] = ft
        instRegisterLabel["fg"] = "#333333"
        instRegisterLabel["text"] = "Instruction Register:"
        instRegisterLabel.place(x=250,y=173,width=140,height=50)
        
        pcLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        pcLabel["font"] = ft
        pcLabel["fg"] = "#333333"
        pcLabel["text"] = "Program Counter:"
        pcLabel.place(x=244,y=253,width=140,height=50)

        self.memoryList=tk.Listbox(root)
        self.memoryList["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        self.memoryList["font"] = ft
        self.memoryList["fg"] = "#333333"
        self.memoryList.place(x=500,y=100,width=200,height=370)
        scrollbar = tk.Scrollbar(self.memoryList)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 
        scrollbar.config(command = self.memoryList.yview)

        self.v1aBox=tk.Checkbutton(root)
        ft = tkFont.Font(family='Arial',size=10)
        self.v1aBox["font"] = ft
        self.v1aBox["fg"] = "#333333"
        self.v1aBox["text"] = "v1a"
        self.v1aBox.place(x=10,y=60,width=70,height=25)
        self.v1aBox["offvalue"] = "0"
        self.v1aBox["onvalue"] = "1"
        self.v1aBox["command"] = self.v1aCommand

        self.v1dBox=tk.Checkbutton(root)
        ft = tkFont.Font(family='Arial',size=10)
        self.v1dBox["font"] = ft
        self.v1dBox["fg"] = "#333333"
        self.v1dBox["text"] = "v1d"
        self.v1dBox.place(x=90,y=60,width=70,height=25)
        self.v1dBox["offvalue"] = "0"
        self.v1dBox["onvalue"] = "1"
        self.v1dBox["command"] = self.v1dCommand

        self.registerList=tk.Listbox(root)
        self.registerList["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        self.registerList["font"] = ft
        self.registerList["fg"] = "#333333"
        self.registerList.place(x=250,y=100,width=145,height=70)
        
        self.instRegisterList=tk.Listbox(root)
        self.instRegisterList["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        self.instRegisterList["font"] = ft
        self.instRegisterList["fg"] = "#333333"
        self.instRegisterList.place(x=250,y=220,width=145,height=30)
        
        self.pcList=tk.Listbox(root)
        self.pcList["borderwidth"] = "1px"
        ft = tkFont.Font(family='Arial',size=10)
        self.pcList["font"] = ft
        self.pcList["fg"] = "#333333"
        self.pcList.place(x=250,y=300,width=145,height=30)

        stepButton=tk.Button(root)
        stepButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        stepButton["font"] = ft
        stepButton["fg"] = "#000000"
        stepButton["text"] = "Step"
        stepButton.place(x=540,y=490,width=70,height=25)
        stepButton["command"] = self.stepButton

        executeButton=tk.Button(root)
        executeButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        executeButton["font"] = ft
        executeButton["fg"] = "#000000"
        executeButton["text"] = "Run"
        executeButton.place(x=620,y=490,width=70,height=25)
        executeButton["command"] = self.executeButton
        
        pauseButton=tk.Button(root)
        pauseButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        pauseButton["font"] = ft
        pauseButton["fg"] = "#000000"
        pauseButton["text"] = "Pause"
        pauseButton.place(x=460,y=490,width=70,height=25)
        pauseButton["command"] = self.pauseButton
        
        dumpMemoryButton=tk.Button(root)
        dumpMemoryButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        dumpMemoryButton["font"] = ft
        dumpMemoryButton["fg"] = "#000000"
        dumpMemoryButton["text"] = "Dump Memory"
        dumpMemoryButton.place(x=390,y=441,width=100,height=25)
        dumpMemoryButton["command"] = self.dumpMem
        
        speedLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        speedLabel["font"] = ft
        speedLabel["fg"] = "#333333"
        speedLabel["text"] = "Speed:"
        speedLabel.place(x=20,y=430,width=50,height=50)
        
        self.speed = tk.Spinbox(root, from_=1, to=25,state='readonly')
        ft = tkFont.Font(family='Arial',size=10)
        self.speed["font"] = ft
        self.speed.place(x=20,y=480,width=70,height=25)
        
        self.instructionsLabel=tk.Label(root, anchor='w')
        ft = tkFont.Font(family='Arial',size=12)
        self.instructionsLabel["font"] = ft
        self.instructionsLabel["fg"] = "#333333"
        self.instructionsLabel["text"] = f"Instruction Count: {self.cycles}"
        self.instructionsLabel.place(x=250,y=10,width=250,height=50)
        
        self.timeLabel=tk.Label(root)
        ft = tkFont.Font(family='Arial',size=12)
        self.timeLabel["font"] = ft
        self.timeLabel["fg"] = "#333333"
        self.timeLabel["text"] = f"Time: {self.speedT}"
        self.timeLabel.place(x=200,y=480,width=140,height=50)
        
        self.menubar = tk.Menu(root)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        idemenu = tk.Menu(self.menubar, tearoff=0)
        instmenu = tk.Menu(self.menubar, tearoff=0)
        peripmenu = tk.Menu(self.menubar, tearoff=0)
        
        filemenu.add_cascade(label="Open", command=self.openfile)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_cascade(label="IDE", menu=idemenu)
        idemenu.add_command(label="New Window", command=self.openIDEWindow)
        instmenu.add_command(label="New Window", command=self.openISSWindow)
        peripmenu.add_command(label="GPIO", command=self.openGPIOWindow)
        self.menubar.add_cascade(label="Intruction Set", menu=instmenu)
        self.menubar.add_cascade(label="Peripherals", menu=peripmenu)
        self.menubar.entryconfig("File", state="disable")
        self.menubar.entryconfig("Peripherals", state="disable")

        root.config(menu=self.menubar)

    def v1aCommand(self):
        self.customCPU = False
        self.running = False
        self.menubar.entryconfig("File", state="normal")
        self.menubar.entryconfig("Peripherals", state="normal")
        self.cycles = 0
        self.speedT = 0
        self.instructionsLabel["text"] = f"Instruction Count: {self.cycles}"
        self.v1dBox=tk.Checkbutton(root)
        ft = tkFont.Font(family='Arial',size=10)
        self.v1dBox["font"] = ft
        self.v1dBox["fg"] = "#333333"
        self.v1dBox["text"] = "v1d"
        self.v1dBox.place(x=90,y=60,width=70,height=25)
        self.v1dBox["offvalue"] = "0"
        self.v1dBox["onvalue"] = "1"
        self.v1dBox["command"] = self.v1dCommand
        self.cpu = cpuA()
        self.registerList.delete(0,99999)
        self.memoryList.delete(0,4095)
        self.pcList.delete(0,1)
        self.instRegisterList.delete(0,1)
        if(self.selected != "v1a"):
            for x in range(len(self.cpu.memory)):
                self.memoryList.insert('end',f"{x}: {format(self.cpu.memory[x], '#06x')}")
            self.registerList.insert('end',f"ACC: {format(self.cpu.accumulator, '#04x')}")
            self.instRegisterList.insert('end',f"IR: {format(self.cpu.instructionRegister, '#06x')}")
            self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
            self.selected = "v1a"
        else:
            self.selected = ""
            self.menubar.entryconfig("File", state="disable")
            self.menubar.entryconfig("Peripherals", state="disable")
            
        self.selectISLabel.destroy()
        self.currentISLabel.destroy()
        self.selectISButton.destroy()
        
    def v1dCommand(self):
        self.customCPU = False
        self.running = False
        self.cycles = 0
        self.speedT = 0
        self.instructionsLabel["text"] = f"Instruction Count: {self.cycles}"
        self.v1aBox=tk.Checkbutton(root)
        ft = tkFont.Font(family='Arial',size=10)
        self.v1aBox["font"] = ft
        self.v1aBox["fg"] = "#333333"
        self.v1aBox["text"] = "v1a"
        self.v1aBox.place(x=10,y=60,width=70,height=25)
        self.v1aBox["offvalue"] = "0"
        self.v1aBox["onvalue"] = "1"
        self.v1aBox["command"] = self.v1aCommand
        self.cpu = cpuD()
        self.instRegisterList.delete(0,1)
        self.pcList.delete(0,1)
        self.registerList.delete(0,99999)
        self.memoryList.delete(0,4095)
        if(self.selected != "v1d"):
            
            self.selectISLabel=tk.Label(root, anchor='w')
            ft = tkFont.Font(family='Arial',size=10)
            self.selectISLabel["font"] = ft
            self.selectISLabel["fg"] = "#333333"
            self.selectISLabel["text"] = "Instruction Set:"
            self.selectISLabel.place(x=30,y=120,width=130,height=25)
            
            self.currentISLabel=tk.Label(root, anchor='w')
            ft = tkFont.Font(family='Arial',size=10)
            self.currentISLabel["font"] = ft
            self.currentISLabel["fg"] = "#333333"
            self.currentISLabel["text"] = "Default"
            self.currentISLabel.place(x=30,y=150,width=130,height=25)
            
            self.selectISButton=tk.Button(root)
            self.selectISButton["bg"] = "#e9e9ed"
            ft = tkFont.Font(family='Arial',size=10)
            self.selectISButton["font"] = ft
            self.selectISButton["fg"] = "#000000"
            self.selectISButton["text"] = "Select Instruction Set"
            self.selectISButton.place(x=30,y=180,width=150,height=25)
            self.selectISButton["command"] = self.mainSetCPUIS
                
            self.menubar.entryconfig("File", state="normal")
            self.menubar.entryconfig("Peripherals", state="normal")
            self.instRegisterList.insert('end',f"IR: {format(self.cpu.instructionRegister, '#06x')}")
            self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
            for x in range(len(self.cpu.memory)):
                self.memoryList.insert('end',f"{x}: {format(self.cpu.memory[x], '#06x')}")
            for x in range(len(self.cpu.registers)):
                self.registerList.insert('end',f"register {self.alphabet[x]}: {format(self.cpu.registers[x], '#06x')}")
            self.selected = "v1d"
        else:
            self.selectISLabel.destroy()
            self.currentISLabel.destroy()
            self.selectISButton.destroy()
            self.selected = ""
            self.menubar.entryconfig("File", state="disable")
            self.menubar.entryconfig("Peripherals", state="disable")

    def haltCheck(self) -> bool:
        if(not self.customCPU):
            if(self.cpu.memory[self.cpu.programCounter] >> 12 == 8 and self.cpu.memory[self.cpu.programCounter] & 4095 == self.cpu.programCounter):
                return True
            elif(self.cpu.memory[self.cpu.programCounter] == 0 and self.cpu.memory[self.cpu.programCounter + 1] == 0):
                return True
            else:
                return False
        else:
            if(self.cpu.instructions[int(self.cpu.memory[self.cpu.programCounter] >> 12)] == "direct_jumpU" and self.cpu.memory[self.cpu.programCounter] & 4095 == self.cpu.programCounter):
                return True
            elif(self.cpu.memory[self.cpu.programCounter] == 0 and self.cpu.memory[self.cpu.programCounter + 1] == 0):
                return True
            else:
                return False

    def openfile(self):
        filename = askopenfilename(parent=root)
        self.cycles = 0
        self.speedT = 0
        self.instructionsLabel["text"] = f"Instruction Count: {self.cycles}"
        self.memoryList.delete(0,99999)
        self.cpu.reset()
        self.cpu.loadMem(filename)
        for x in range(len(self.cpu.memory)):
            self.memoryList.insert('end',f"{x}: {format(self.cpu.memory[x], '#06x')}")
        self.memoryList.insert('end',"")

    def stepButton(self):
        if(not self.haltCheck()):
            self.cycles = self.cycles + 1
            if(self.input != self.lastInput):
                self.cpu.memory[int(self.GPIOAddressBox.get())] = (self.cpu.memory[int(self.GPIOAddressBox.get())] & 65280) + self.input
                self.lastInput = self.input
            
            self.cpu.execute()
            
            if(self.GPIOConnected):
                self.GPIOUpdateOutput()
                
            self.instructionsLabel["text"] = f"Instruction Count: {self.cycles}"
            self.timeLabel["text"] = f"Time: {self.speedT}"[0:12]
            self.instRegisterList.delete(0,1)
            self.instRegisterList.insert('end',f"IR: {format(self.cpu.instructionRegister, '#06x')}")
            self.pcList.delete(0,1)
            self.registerList.delete(0,3)
            if(self.selected == "v1d"):
                self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
                for x in range(len(self.cpu.memory)):
                     if(self.cpu.memory[x] != int(self.memoryList.get(x)[-4:],16)):
                         self.memoryList.delete(x)
                         self.memoryList.insert(x,f"{x}: {format(self.cpu.memory[x], '#06x')}")
                for x in range(len(self.cpu.registers)):
                    self.registerList.insert('end',f"register {self.alphabet[x]}: {format(self.cpu.registers[x], '#06x')}")
            elif(self.selected == "v1a"):
                for x in range(len(self.cpu.memory)):
                    if(self.cpu.memory[x] != int(self.memoryList.get(x)[-4:],16)):
                         self.memoryList.delete(x)
                         self.memoryList.insert(x,f"{x}: {format(self.cpu.memory[x], '#06x')}")
                self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
                self.registerList.insert('end',f"ACC: {format(self.cpu.accumulator, '#04x')}")
        
    def executeButton(self):
        self.executeAll()
        
    def pauseButton(self):
        self.pause()
    
    def executeStep(self):
        if(not self.haltCheck()):
            cpuBeforeStep = copy.deepcopy(self.cpu)
            count =  2 ** (int(self.speed.get()) - 1)
            startTime = time.time()
            if(self.input == self.lastInput):
                self.cpu.execute(count)
            else:
                for x in range(count):
                    if(self.GPIOAddressBox.get() != ''):
                        self.cpu.memory[int(self.GPIOAddressBox.get())] = (self.cpu.memory[int(self.GPIOAddressBox.get())] & 65280) + self.input
                        self.lastInput = self.input
                        self.cpu.execute()
            endTime = time.time()
            self.speedT = self.speedT + (endTime - startTime)
            
            if((endTime - startTime) < 0.0001):
                time.sleep(0.6/(count+1))
                
            if(self.haltCheck()):
                self.cpu = copy.deepcopy(cpuBeforeStep)
                for x in range(count):
                    if(self.input != self.lastInput):
                        if(self.GPIOAddressBox.get() != ''):
                            self.cpu.memory[int(self.GPIOAddressBox.get())] = (self.cpu.memory[int(self.GPIOAddressBox.get())] & 65280) + self.input
                            self.lastInput = self.input
                    self.cpu.execute()
                    self.cycles = self.cycles + 1
                    if(self.haltCheck()):
                        self.running = False
                        break
                        
            if(self.running == True):
                self.cycles = self.cycles + count
                
            if(self.GPIOConnected):
                self.GPIOUpdateOutput()
                
            self.instructionsLabel["text"] = f"Instruction Count: {self.cycles}"
            self.timeLabel["text"] = f"Time: {self.speedT}"[0:12]
            self.instRegisterList.delete(0,1)
            self.instRegisterList.insert('end',f"IR: {format(self.cpu.instructionRegister, '#06x')}")
            self.pcList.delete(0,1)
            self.registerList.delete(0,3)
            if(self.selected == "v1d"):
                self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
                for x in range(len(self.cpu.memory)):
                     if(self.cpu.memory[x] != int(self.memoryList.get(x)[-4:],16)):
                         self.memoryList.delete(x)
                         self.memoryList.insert(x,f"{x}: {format(self.cpu.memory[x], '#06x')}")
                for x in range(len(self.cpu.registers)):
                    self.registerList.insert('end',f"register {self.alphabet[x]}: {format(self.cpu.registers[x], '#06x')}")
            elif(self.selected == "v1a"):
                for x in range(len(self.cpu.memory)):
                    if(self.cpu.memory[x] != int(self.memoryList.get(x)[-4:],16)):
                         self.memoryList.delete(x)
                         self.memoryList.insert(x,f"{x}: {format(self.cpu.memory[x], '#06x')}")
                self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
                self.registerList.insert('end',f"ACC: {format(self.cpu.accumulator, '#04x')}")
        
    def executeAll(self):
        self.running = True
        
    def pause(self):
        self.running = False
        
    def openGPIOWindow(self):
        self.GPIOConnected = True
        self.GPIOWindow = tk.Toplevel(root)
        self.GPIOWindow.title("SimpleCPUSim - GPIO")
        width=720
        height=550
        screenwidth = self.GPIOWindow.winfo_screenwidth()
        screenheight = self.GPIOWindow.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2 + 10, (screenheight - height) / 2 + 10)
        self.GPIOWindow.geometry(alignstr)
        self.GPIOWindow.resizable(width=False, height=False)
        
        self.GPIOInputLabel = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInputLabel["font"] = ft
        self.GPIOInputLabel["fg"] = "#000000"
        self.GPIOInputLabel["text"] = "Input:"
        self.GPIOInputLabel.place(x=40,y=20)
        
        self.GPIOOutputLabel = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOOutputLabel["font"] = ft
        self.GPIOOutputLabel["fg"] = "#000000"
        self.GPIOOutputLabel["text"] = "Output:"
        self.GPIOOutputLabel.place(x=40,y=220)
        
        self.GPIOInputAddressLabel = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInputAddressLabel["font"] = ft
        self.GPIOInputAddressLabel["fg"] = "#000000"
        self.GPIOInputAddressLabel["text"] = "Address:"
        self.GPIOInputAddressLabel.place(x=520,y=35)
        
        self.GPIOOutputAddressLabel = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOOutputAddressLabel["font"] = ft
        self.GPIOOutputAddressLabel["fg"] = "#000000"
        self.GPIOOutputAddressLabel["text"] = "Address:"
        self.GPIOOutputAddressLabel.place(x=520,y=235)
    
        self.GPIOInput0 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput0["font"] = ft
        self.GPIOInput0["fg"] = "#000000"
        self.GPIOInput0["text"] = "0"
        self.GPIOInput0.place(x=103,y=85)
        
        self.GPIOInput0Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput0Button["font"] = ft
        self.GPIOInput0Button["fg"] = "#000000"
        self.GPIOInput0Button["text"] = "0"
        self.GPIOInput0Button["command"] = lambda bit=self.GPIOInput0 : self.GPIOSwitch(bit)
        self.GPIOInput0Button.place(x=95,y=115,width=32,height=32)
        
        self.GPIOInput1 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput1["font"] = ft
        self.GPIOInput1["fg"] = "#000000"
        self.GPIOInput1["text"] = "0"
        self.GPIOInput1.place(x=166,y=85)
        
        self.GPIOInput1Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput1Button["font"] = ft
        self.GPIOInput1Button["fg"] = "#000000"
        self.GPIOInput1Button["text"] = "1"
        self.GPIOInput1Button["command"] = lambda bit=self.GPIOInput1 : self.GPIOSwitch(bit)
        self.GPIOInput1Button.place(x=158,y=115,width=32,height=32)
        
        self.GPIOInput2 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput2["font"] = ft
        self.GPIOInput2["fg"] = "#000000"
        self.GPIOInput2["text"] = "0"
        self.GPIOInput2.place(x=229,y=85)
        
        self.GPIOInput2Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput2Button["font"] = ft
        self.GPIOInput2Button["fg"] = "#000000"
        self.GPIOInput2Button["text"] = "2"
        self.GPIOInput2Button["command"] = lambda bit=self.GPIOInput2 : self.GPIOSwitch(bit)
        self.GPIOInput2Button.place(x=221,y=115,width=32,height=32)
        
        self.GPIOInput3 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput3["font"] = ft
        self.GPIOInput3["fg"] = "#000000"
        self.GPIOInput3["text"] = "0"
        self.GPIOInput3.place(x=292,y=85)
        
        self.GPIOInput3Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput3Button["font"] = ft
        self.GPIOInput3Button["fg"] = "#000000"
        self.GPIOInput3Button["text"] = "3"
        self.GPIOInput3Button["command"] = lambda bit=self.GPIOInput3 : self.GPIOSwitch(bit)
        self.GPIOInput3Button.place(x=284,y=115,width=32,height=32)
        
        self.GPIOInput4 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput4["font"] = ft
        self.GPIOInput4["fg"] = "#000000"
        self.GPIOInput4["text"] = "0"
        self.GPIOInput4.place(x=355,y=85)
        
        self.GPIOInput4Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput4Button["font"] = ft
        self.GPIOInput4Button["fg"] = "#000000"
        self.GPIOInput4Button["text"] = "4"
        self.GPIOInput4Button["command"] = lambda bit=self.GPIOInput4 : self.GPIOSwitch(bit)
        self.GPIOInput4Button.place(x=347,y=115,width=32,height=32)
        
        self.GPIOInput5 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput5["font"] = ft
        self.GPIOInput5["fg"] = "#000000"
        self.GPIOInput5["text"] = "0"
        self.GPIOInput5.place(x=418,y=85)
        
        self.GPIOInput5Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput5Button["font"] = ft
        self.GPIOInput5Button["fg"] = "#000000"
        self.GPIOInput5Button["text"] = "5"
        self.GPIOInput5Button["command"] = lambda bit=self.GPIOInput5 : self.GPIOSwitch(bit)
        self.GPIOInput5Button.place(x=410,y=115,width=32,height=32)
        
        self.GPIOInput6 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput6["font"] = ft
        self.GPIOInput6["fg"] = "#000000"
        self.GPIOInput6["text"] = "0"
        self.GPIOInput6.place(x=481,y=85)
        
        self.GPIOInput6Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput6Button["font"] = ft
        self.GPIOInput6Button["fg"] = "#000000"
        self.GPIOInput6Button["text"] = "6"
        self.GPIOInput6Button["command"] = lambda bit=self.GPIOInput6 : self.GPIOSwitch(bit)
        self.GPIOInput6Button.place(x=473,y=115,width=32,height=32)
        
        self.GPIOInput7 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOInput7["font"] = ft
        self.GPIOInput7["fg"] = "#000000"
        self.GPIOInput7["text"] = "0"
        self.GPIOInput7.place(x=544,y=85)
        
        self.GPIOInput7Button = tk.Button(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.GPIOInput7Button["font"] = ft
        self.GPIOInput7Button["fg"] = "#000000"
        self.GPIOInput7Button["text"] = "7"
        self.GPIOInput7Button["command"] = lambda bit=self.GPIOInput7 : self.GPIOSwitch(bit)
        self.GPIOInput7Button.place(x=536,y=115,width=32,height=32)
        
        self.GPIOOutput0 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput0["font"] = ft
        self.GPIOOutput0["fg"] = "#000000"
        self.GPIOOutput0["text"] = "0"
        self.GPIOOutput0.place(x=103,y=385)
        
        self.GPIOOutput0display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput0display["font"] = ft
        self.GPIOOutput0display["bg"] = "#000000"
        self.GPIOOutput0display["text"] = ""
        self.GPIOOutput0display.place(x=97,y=325,height=32,width=32)
        
        self.GPIOOutput1 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput1["font"] = ft
        self.GPIOOutput1["fg"] = "#000000"
        self.GPIOOutput1["text"] = "1"
        self.GPIOOutput1.place(x=166,y=385)
        
        self.GPIOOutput1display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput1display["font"] = ft
        self.GPIOOutput1display["bg"] = "#000000"
        self.GPIOOutput1display["text"] = ""
        self.GPIOOutput1display.place(x=160,y=325,height=32,width=32)
        
        self.GPIOOutput2 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput2["font"] = ft
        self.GPIOOutput2["fg"] = "#000000"
        self.GPIOOutput2["text"] = "2"
        self.GPIOOutput2.place(x=229,y=385)
        
        self.GPIOOutput2display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput2display["font"] = ft
        self.GPIOOutput2display["bg"] = "#000000"
        self.GPIOOutput2display["text"] = ""
        self.GPIOOutput2display.place(x=223,y=325,height=32,width=32)
        
        self.GPIOOutput3 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput3["font"] = ft
        self.GPIOOutput3["fg"] = "#000000"
        self.GPIOOutput3["text"] = "3"
        self.GPIOOutput3.place(x=292,y=385)
        
        self.GPIOOutput3display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput3display["font"] = ft
        self.GPIOOutput3display["bg"] = "#000000"
        self.GPIOOutput3display["text"] = ""
        self.GPIOOutput3display.place(x=286,y=325,height=32,width=32)
        
        self.GPIOOutput4 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput4["font"] = ft
        self.GPIOOutput4["fg"] = "#000000"
        self.GPIOOutput4["text"] = "4"
        self.GPIOOutput4.place(x=355,y=385)
        
        self.GPIOOutput4display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput4display["font"] = ft
        self.GPIOOutput4display["bg"] = "#000000"
        self.GPIOOutput4display["text"] = ""
        self.GPIOOutput4display.place(x=349,y=325,height=32,width=32)
        
        self.GPIOOutput5 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput5["font"] = ft
        self.GPIOOutput5["fg"] = "#000000"
        self.GPIOOutput5["text"] = "5"
        self.GPIOOutput5.place(x=418,y=385)
        
        self.GPIOOutput5display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput5display["font"] = ft
        self.GPIOOutput5display["bg"] = "#000000"
        self.GPIOOutput5display["text"] = ""
        self.GPIOOutput5display.place(x=412,y=325,height=32,width=32)
        
        self.GPIOOutput6 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput6["font"] = ft
        self.GPIOOutput6["fg"] = "#000000"
        self.GPIOOutput6["text"] = "6"
        self.GPIOOutput6.place(x=481,y=385)
        
        self.GPIOOutput6display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput6display["font"] = ft
        self.GPIOOutput6display["bg"] = "#000000"
        self.GPIOOutput6display["text"] = ""
        self.GPIOOutput6display.place(x=475,y=325,height=32,width=32)
        
        self.GPIOOutput7 = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput7["font"] = ft
        self.GPIOOutput7["fg"] = "#000000"
        self.GPIOOutput7["text"] = "7"
        self.GPIOOutput7.place(x=544,y=385)
        
        self.GPIOOutput7display = tk.Label(self.GPIOWindow)
        ft = tkFont.Font(family='Arial',size=16)
        self.GPIOOutput7display["font"] = ft
        self.GPIOOutput7display["bg"] = "#000000"
        self.GPIOOutput7display["text"] = ""
        self.GPIOOutput7display.place(x=538,y=325,height=32,width=32)
                
        self.GPIOAddressBox = tk.Spinbox(self.GPIOWindow,from_=0,to=len(self.cpu.memory)-1,textvariable=tk.DoubleVar(value=len(self.cpu.memory)-2))
        self.GPIOAddressBox.place(x=580,y=35,width=92,height=26)
        
        self.GPIOAddressBoxOutput = tk.Spinbox(self.GPIOWindow,from_=0,to=len(self.cpu.memory)-1,textvariable=tk.DoubleVar(value=len(self.cpu.memory)-1))
        self.GPIOAddressBoxOutput.place(x=580,y=235,width=92,height=26)
        
    def openIDEWindow(self):
        self.newWindow = tk.Toplevel(root)
        self.newWindow.title("SimpleCPUSim - IDE")
        width=720
        height=550
        screenwidth = self.newWindow.winfo_screenwidth()
        screenheight = self.newWindow.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2 + 10, (screenheight - height) / 2 + 10)
        self.newWindow.geometry(alignstr)
        self.newWindow.resizable(width=False, height=False)
        self.path = "newFile.asm"
        self.isPath = None
        self.m4path = None
        
        self.macroLabel = tk.Label(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.macroLabel["font"] = ft
        self.macroLabel["fg"] = "#000000"
        self.macroLabel["text"] = "Macro file selected:"
        self.macroLabel.place(x=20,y=50)
        
        self.macroSelectedLabel = tk.Label(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.macroSelectedLabel["font"] = ft
        self.macroSelectedLabel["fg"] = "#000000"
        self.macroSelectedLabel["text"] = "None"
        self.macroSelectedLabel.place(x=20,y=75)
        
        self.macroSelectButton = tk.Button(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.macroSelectButton["bg"] = "#e9e9ed"
        self.macroSelectButton["font"] = ft
        self.macroSelectButton["fg"] = "#000000"
        self.macroSelectButton["text"] = "Select .m4 file"
        self.macroSelectButton["command"] = self.ideLoadM4
        self.macroSelectButton.place(x=20,y=105,width=90,height=25)
        
        self.macroClearButton = tk.Button(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.macroClearButton["bg"] = "#e9e9ed"
        self.macroClearButton["font"] = ft
        self.macroClearButton["fg"] = "#000000"
        self.macroClearButton["text"] = "Reset"
        self.macroClearButton["command"] = self.ideResetM4
        self.macroClearButton.place(x=20,y=135,width=90,height=25)
        
        self.IDEISLabel = tk.Label(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.IDEISLabel["font"] = ft
        self.IDEISLabel["fg"] = "#000000"
        self.IDEISLabel["text"] = "Instruction Set Selected:"
        self.IDEISLabel.place(x=20,y=180)
        
        self.IDEISSelectedLabel = tk.Label(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.IDEISSelectedLabel["font"] = ft
        self.IDEISSelectedLabel["fg"] = "#000000"
        self.IDEISSelectedLabel["text"] = "Default"
        self.IDEISSelectedLabel.place(x=20,y=205)
        
        self.IDEISSelectButton = tk.Button(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.IDEISSelectButton["bg"] = "#e9e9ed"
        self.IDEISSelectButton["font"] = ft
        self.IDEISSelectButton["fg"] = "#000000"
        self.IDEISSelectButton["text"] = "Select .is file"
        self.IDEISSelectButton["command"] = self.ideLoadIS
        self.IDEISSelectButton.place(x=20,y=235,width=90,height=25)
        
        self.IDEISClearButton = tk.Button(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.IDEISClearButton["bg"] = "#e9e9ed"
        self.IDEISClearButton["font"] = ft
        self.IDEISClearButton["fg"] = "#000000"
        self.IDEISClearButton["text"] = "Reset"
        self.IDEISClearButton["command"] = self.ideResetIS
        self.IDEISClearButton.place(x=20,y=265,width=90,height=25)
        
        self.fileLabel = tk.Label(self.newWindow)
        ft = tkFont.Font(family='Arial',size=10)
        self.fileLabel["font"] = ft
        self.fileLabel["fg"] = "#000000"
        self.fileLabel["text"] = "newFile.asm"
        self.fileLabel.place(x=180,y=20)
        
        self.newFileButton = tk.Button(self.newWindow)
        self.newFileButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        self.newFileButton["font"] = ft
        self.newFileButton["fg"] = "#000000"
        self.newFileButton["text"] = "New file"
        self.newFileButton["command"] = self.ideNewFile
        self.newFileButton.place(x=550,y=50,width=90,height=25)
        
        self.loadFileButton = tk.Button(self.newWindow)
        self.loadFileButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        self.loadFileButton["font"] = ft
        self.loadFileButton["fg"] = "#000000"
        self.loadFileButton["text"] = "Load file"
        self.loadFileButton["command"] = self.ideLoadFile
        self.loadFileButton.place(x=550,y=80,width=90,height=25)
        
        self.saveFileButton = tk.Button(self.newWindow)
        self.saveFileButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        self.saveFileButton["font"] = ft
        self.saveFileButton["fg"] = "#000000"
        self.saveFileButton["text"] = "Save file"
        self.saveFileButton["command"] = self.ideSaveFile
        self.saveFileButton.place(x=550,y=110,width=90,height=25)
        
        self.saveFileAsButton = tk.Button(self.newWindow)
        self.saveFileAsButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        self.saveFileAsButton["font"] = ft
        self.saveFileAsButton["fg"] = "#000000"
        self.saveFileAsButton["text"] = "Save file as"
        self.saveFileAsButton["command"] = self.ideSaveAsFile
        self.saveFileAsButton.place(x=550,y=140,width=90,height=25)
        
        self.usev1aAssembler = False
        self.v1aAssemblerBox = tk.Checkbutton(self.newWindow)
        self.v1aAssemblerBox["font"] = ft
        self.v1aAssemblerBox["fg"] = "#333333"
        self.v1aAssemblerBox["text"] = "v1a Assembler"
        self.v1aAssemblerBox.place(x=20,y=470,width=120,height=25)
        self.v1aAssemblerBox["offvalue"] = "0"
        self.v1aAssemblerBox["onvalue"] = "1"
        self.v1aAssemblerBox["command"] = self.changeAssemblerState

        self.saveFileButton["fg"] = "#000000"
        self.saveFileButton["text"] = "Save file"
        self.saveFileButton["command"] = self.ideSaveFile
        self.saveFileButton.place(x=550,y=110,width=90,height=25)
        
        self.AssembleButton = tk.Button(self.newWindow)
        self.AssembleButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        self.AssembleButton["font"] = ft
        self.AssembleButton["fg"] = "#000000"
        self.AssembleButton["text"] = "Assemble"
        self.AssembleButton["command"] = self.ideAssemble
        self.AssembleButton.place(x=550,y=475,width=90,height=25)
        
        self.TextBox = tk.Text(self.newWindow, height = 450, width = 350)
        self.TextBox.place(x=180,y=50,height = 450, width = 350)
        
    def openISSWindow(self):
        self.issWindow = tk.Toplevel(root)
        self.issWindow.title("SimpleCPUSim - Customise Instruction Set")
        width=900
        height=620
        screenwidth = self.issWindow.winfo_screenwidth()
        screenheight = self.issWindow.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2 + 10, (screenheight - height) / 2 + 10)
        self.issWindow.geometry(alignstr)
        self.issWindow.resizable(width=False, height=False)
        self.insSelLabel = tk.Label(self.issWindow)
        self.insSelLabelLabel = tk.Label(self.issWindow)
        self.insSelLabelLabel["text"] = "Selected instruction:"
        self.insSelLabelLabel.place(x=330,y=180)
        
        instructions=open("Resources/instructionFormats","r")
        
        
        self.instructions = tk.Listbox(self.issWindow)
        self.instructions["borderwidth"] = "1px"
        ft = tkFont.Font(family='Courier New',size=10)
        self.instructions["font"] = ft
        self.instructions["fg"] = "#333333"
        scrollbar = tk.Scrollbar(self.instructions)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 
        self.instructions.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command = self.memoryList.yview)
        self.instructions.place(x=50,y=50,height = 450, width = 250)
        
        for x in instructions:
            array = x.split(",")
            self.instructions.insert('end',f"{array[0]}{' '*(8-len(array[0]))}{array[-1]}")
        
        self.iSet = tk.Listbox(self.issWindow)
        self.iSet["borderwidth"] = "1px"
        ft = tkFont.Font(family='Courier New',size=10)
        self.iSet["font"] = ft
        self.iSet["fg"] = "#333333"
        scrollbar = tk.Scrollbar(self.iSet)
        scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH) 
        scrollbar.config(command = self.memoryList.yview)
        self.iSet.place(x=500,y=50,height = 450, width = 350)
        
        selectInstructionButton = tk.Button(self.issWindow)
        selectInstructionButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        selectInstructionButton["font"] = ft
        selectInstructionButton["fg"] = "#000000"
        selectInstructionButton["text"] = "Select"
        selectInstructionButton["command"] = self.showSelected
        selectInstructionButton.place(x=125,y=520,width=80,height=30)

        assignInstructionButton = tk.Button(self.issWindow)
        assignInstructionButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        assignInstructionButton["font"] = ft
        assignInstructionButton["fg"] = "#000000"
        assignInstructionButton["text"] = "Assign"
        assignInstructionButton["command"] = self.assignSelected
        assignInstructionButton.place(x=640,y=520,width=80,height=30)
        
        exportButton = tk.Button(self.issWindow)
        exportButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Arial',size=10)
        exportButton["font"] = ft
        exportButton["fg"] = "#000000"
        exportButton["text"] = "Export to .is file"
        exportButton["command"] = self.saveISFile
        exportButton.place(x=315,y=570,width=160,height=30)
        
        for x in range(31):
            if(x < 15):
                self.iSet.insert('end',f"[{registerAddressing[x]}]{' '*(23-len(registerAddressing[x]))}{format(x,'04b')} :")
            else:
                self.iSet.insert('end',f"[{registerAddressing[x]}]{' '*(19-len(registerAddressing[x]))}1111+{format(x-15,'04b')}:")

    def showSelected(self):
        self.instructionSelected = self.iSet.selection_get()
        self.insSelLabel["text"] = self.instructionSelected
        self.insSelLabel.place(x=350,y=200)
        
    def assignSelected(self):
        self.opcodeSelected = self.iSet.selection_get()
        selection = self.iSet.curselection()
        if(self.instructionSelected.split()[1] == self.opcodeSelected.split()[0].replace('[','').replace(']','')):
            self.iSet.delete(selection)
            self.iSet.insert(selection, f"{self.opcodeSelected[0:31]} {self.instructionSelected.split()[0]}")
            
    def saveISFile(self):
        instructions = open("Resources/instructionFormats","r")
        file = filedialog.asksaveasfile(mode="w",defaultextension='.is',filetypes=[("Instruction Set","*.is")])
        for i in self.iSet.get(0,30):
            instructions = open("Resources/instructionFormats","r")
            wroteInstruction = False
            for inst in instructions:
                if(i[1:(i.index(']'))] == inst.split(",")[-1].strip() and i[(i.index(':')+2):(len(i))] == inst.split(",")[0]):
                    inst.split(",")[-2]
                    instruction = f"{inst.split(',')[-2][0:4].replace('XXXX',i.split()[1][0:4])}{inst.split(',')[-2][4:12]}{inst.split(',')[-2][12:16].replace('XXXX',i.split()[1][5:9])}".ljust(16,'0')
                    line = f"{inst[0:inst.index(')')+1]},{instruction},{inst.split(',')[-1]}"
                    file.write(line.ljust(16))  
                    wroteInstruction = True
            if(wroteInstruction == False):
                file.write('\n')
                
    def ideLoadFile(self):
        if(self.path != "newFile.asm" or ""):
            loadedFile = open(self.path,'r')
            for (x,y) in zip(self.TextBox.get(0.0,tk.END).splitlines(),loadedFile.readlines()):
                if(x.strip() != y.strip()):
                    userInput = tk.messagebox.askokcancel("Unsaved Changes", "The current file contains changes not currently saved, are you sure you want to continue?")
                    if(not userInput):
                        return "cancel function"
        self.path = askopenfilename(parent=root,defaultextension='.asm',filetypes=[("Assembly machine code","*.asm"),("Macro file","*.m4")])
        file = open(self.path,'r')
        self.TextBox.delete('1.0',tk.END)
        for x in file:
            self.TextBox.insert(tk.END,x)
        self.fileLabel["text"] = self.path.split('/')[-1]
        if(self.path[-4:] != '.asm'):
            self.AssembleButton["state"] = "disabled"
        else:
            self.AssembleButton["state"] = "active"
        
    def ideNewFile(self):
        if(self.path != "newFile.asm" or ""):
            loadedFile = open(self.path,'r')
            for (x,y) in zip(self.TextBox.get(0.0,tk.END).splitlines(),loadedFile.readlines()):
                if(x.strip() != y.strip()):
                    userInput = tk.messagebox.askokcancel("Unsaved Changes", "The current file contains changes not currently saved, are you sure you want to continue?")
                    if(not userInput):
                        return "cancel function"
        self.TextBox.delete('1.0',tk.END)
        file = filedialog.asksaveasfile(mode="w",defaultextension='.asm',filetypes=[("Assembly machine code","*.asm"),("Macro file","*.m4")])
        self.path = file.name
        self.fileLabel["text"] = file.name.split('/')[-1]
        if(self.path[-4:] != '.asm'):
            self.AssembleButton["state"] = "disabled"
        else:
            self.AssembleButton["state"] = "active"
            
    def ideSaveFile(self):
        file = open(self.path,'w')
        strings = self.TextBox.get('1.0',tk.END)
        for x in strings[0:-1]: # -1 prevents adding a new blank line
            file.write(x)
        file.close()
        
    def ideSaveAsFile(self):
        file = filedialog.asksaveasfile(mode="w",defaultextension='.asm',filetypes=[("Assembly machine code","*.asm"),("Macro file","*.m4")])
        strings = self.TextBox.get('1.0',tk.END)
        self.path = file.name
        self.fileLabel["text"] = file.name.split('/')[-1]
        for x in strings[0:-1]: # -1 prevents adding a new blank line
            file.write(x)
        if(self.path[-4:] != '.asm'):
            self.AssembleButton["state"] = "disabled"
        else:
            self.AssembleButton["state"] = "active"
            
    def ideLoadM4(self):
        self.m4path = askopenfilename(parent=root,defaultextension='.m4',filetypes=[("Macro file","*.m4")])
        self.macroSelectedLabel["text"] = self.m4path.split('/')[-1]
        
    def ideResetM4(self):
        self.m4path = None
        self.macroSelectedLabel["text"] = "None"
        
    def ideLoadIS(self):
        self.isPath = askopenfilename(parent=root,defaultextension='.is',filetypes=[("Instruction set file","*.is")])
        self.IDEISSelectedLabel["text"] = self.isPath.split('/')[-1]
        
    def ideResetIS(self):
        self.isPath = None
        self.IDEISSelectedLabel["text"] = "Default"
        
    def changeAssemblerState(self):
        if(self.usev1aAssembler == False):
            self.usev1aAssembler = True
        else:
            self.usev1aAssembler = False
        
    def ideAssemble(self):
        finalFile = filedialog.asksaveasfilename(defaultextension='.dat',filetypes=[("file","*.dat")])
        file = open("temp.asm",'w')
        strings = self.TextBox.get('1.0',tk.END)
        for x in strings[0:-1]: # -1 prevents adding a new blank line
            file.write(x)
        file.close()
        if(self.m4path != None):
            result = subprocess.run(["m4", self.m4path, "temp.asm"],capture_output=True)
            file = open("temp2.asm",'w')
            file.write(result.stdout.decode("ascii"))
            file.close()
        if(self.usev1aAssembler == True and self.path[-4:] == '.asm' and self.m4path == None):
            assembler.simpleCPUv1d_as(f"-i temp.asm -p 1")
            dynamicAssembler.dynamicAssembler("Resources/simpleCPU_v1a.is",'tmp.asm',finalFile)
        elif(self.usev1aAssembler == True and self.path[-4:] == '.asm' and self.m4path != None):
            assembler.simpleCPUv1d_as(f"-i temp2.asm -p 1")
            dynamicAssembler.dynamicAssembler("Resources/simpleCPU_v1a.is",'tmp.asm',finalFile)
        elif(self.isPath == None and self.path[-4:] == '.asm' and self.m4path == None):
            assembler.simpleCPUv1d_as(f"-i temp.asm -p 1")
            dynamicAssembler.dynamicAssembler("Resources/simpleCPU_v1d.is",'tmp.asm',finalFile)
        elif(self.isPath != None and self.path[-4:] == '.asm'and self.m4path == None):
            assembler.simpleCPUv1d_as(f"-i temp.asm -p 1")
            dynamicAssembler.dynamicAssembler(self.isPath,'tmp.asm',finalFile)
        elif(self.isPath == None and self.path[-4:] == '.asm'and self.m4path != None):
            assembler.simpleCPUv1d_as(f"-i temp2.asm -p 1")
            dynamicAssembler.dynamicAssembler("Resources/simpleCPU_v1d.is",'tmp.asm',finalFile)
        elif(self.isPath != None and self.path[-4:] == '.asm' and self.m4path != None):
            assembler.simpleCPUv1d_as(f"-i temp2.asm -p 1")
            dynamicAssembler.dynamicAssembler(self.isPath,'tmp.asm',finalFile)
            
    def GPIOSwitch(self, bit):
        if(bit["text"] == "0"):
            bit["text"] = "1"
        else:
            bit["text"] = "0"
        self.input = 0
        if(self.GPIOInput0["text"] == "1"):
            self.input += 1
        if(self.GPIOInput1["text"] == "1"):
            self.input += 2
        if(self.GPIOInput2["text"] == "1"):
            self.input += 4
        if(self.GPIOInput3["text"] == "1"):
            self.input += 8
        if(self.GPIOInput4["text"] == "1"):
            self.input += 16
        if(self.GPIOInput5["text"] == "1"):
            self.input += 32
        if(self.GPIOInput6["text"] == "1"):
            self.input += 64
        if(self.GPIOInput7["text"] == "1"):
            self.input += 128
            
    def GPIOUpdateOutput(self):
        if(self.GPIOAddressBoxOutput.get() == ''):
            return None
        output = self.cpu.memory[int(self.GPIOAddressBoxOutput.get())]
        if(output & 1 > 0):
            self.GPIOOutput0display["bg"] = "#F00"
        else:
            self.GPIOOutput0display["bg"] = "#000"
        if(output & 2 > 0):
            self.GPIOOutput1display["bg"] = "#F00"
        else:
            self.GPIOOutput1display["bg"] = "#000"
        if(output & 4 > 0):
            self.GPIOOutput2display["bg"] = "#F00"
        else:
            self.GPIOOutput2display["bg"] = "#000"
        if(output & 8 > 0):
            self.GPIOOutput3display["bg"] = "#F00"
        else:
            self.GPIOOutput3display["bg"] = "#000"
        if(output & 16 > 0):
            self.GPIOOutput4display["bg"] = "#F00"
        else:
            self.GPIOOutput4display["bg"] = "#000"
        if(output & 32 > 0):
            self.GPIOOutput5display["bg"] = "#F00"
        else:
            self.GPIOOutput5display["bg"] = "#000"
        if(output & 64 > 0):
            self.GPIOOutput6display["bg"] = "#F00"
        else:
            self.GPIOOutput6display["bg"] = "#000"
        if(output & 128 > 0):
            self.GPIOOutput7display["bg"] = "#F00"
        else:
            self.GPIOOutput7display["bg"] = "#000"
            
    def dumpMem(self):
        file = filedialog.asksaveasfile(mode="w",defaultextension='.dat',filetypes=[("file","*.dat")])
        for x in range(len(self.cpu.memory)):
            file.write(f"{format(x,'04')} {format(self.cpu.memory[x],'016b')}\n")
            
            
    def mainSetCPUIS(self):
        self.mainISSelected = askopenfilename(parent=root,defaultextension='.is',filetypes=[("Instruction Set File","*.is")])
        if(self.mainISSelected != ''):
            self.customCPU = True
            self.instRegisterList.delete(0,1)
            self.pcList.delete(0,1)
            self.registerList.delete(0,99999)
            self.memoryList.delete(0,4095)
            self.cpu = cpuCustom()
            self.cpu.loadInstructions(self.mainISSelected)

            self.menubar.entryconfig("File", state="normal")
            self.instRegisterList.insert('end',f"IR: {format(self.cpu.instructionRegister, '#06x')}")
            self.pcList.insert('end',f"PC: {self.cpu.programCounter}")
            for x in range(len(self.cpu.memory)):
                self.memoryList.insert('end',f"{x}: {format(self.cpu.memory[x], '#06x')}")
            for x in range(len(self.cpu.registers)):
                self.registerList.insert('end',f"register {self.alphabet[x]}: {format(self.cpu.registers[x], '#06x')}")
            
            self.currentISLabel["text"] = self.mainISSelected.split('/')[-1]
                 
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    while(root.winfo_exists()):
        if(app.running == True):
            app.executeStep()
        root.update()