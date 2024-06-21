start:
 move ra 0x55
 move rb 0xaa
 xor ra rb
 add rb 0xff
 xor ra rb
 xor ra rb
 xor ra rb
halt:
 jumpu halt