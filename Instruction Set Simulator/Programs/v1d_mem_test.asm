start:
 move ra 0xff
 store ra 0xfff
 move ra 0xf0
 store ra 0xffe
 move ra 0x00
 store ra 0x000
 load ra 0x000
 load ra 0xffe
 load ra 0xfff
 move ra 0x00
 addm ra 0x000
 addm ra 0xfff
 addm ra 0xffe
 addm ra 0xfff
 addm ra 0xffe
 addm ra 0xfff
 addm ra 0xffe
 addm ra 0xfff
 addm ra 0x000
 move ra 0x00
 subm ra 0x000
 subm ra 0xfff
 subm ra 0xffe
 subm ra 0xfff
 subm ra 0xffe
 subm ra 0xfff
 subm ra 0xffe
 subm ra 0xfff
 subm ra 0x000
halt:
 jumpu halt