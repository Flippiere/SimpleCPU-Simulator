start:
 jumpz six
 jumpc five
 jumpnz four
 jumpu halt
one:
 move ra 0x01
 sub ra 0x02
 jumpnz five
 jumpu one
two:
 move ra 0xff
 add ra 0x04
 jumpc one
 jumpu halt
three:
 move ra 0x03
 sub ra 0x04
 jumpnz two
 jumpu halt
four:
 move ra 0x04
 sub ra 0x04
 jumpz three
 jumpu halt
five:
 move ra 0x05
six:
 move ra 0x06
halt:
 jumpu halt