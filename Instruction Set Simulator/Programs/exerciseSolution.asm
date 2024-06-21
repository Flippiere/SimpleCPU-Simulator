start:
 move ra 0x1f
 move rc 0x0b
roller:
 rol ra
 sub rc 0x01
 jumpnz roller
nextSection:
 store ra 0x513
 store ra 0x52b
 store ra 0x52a
 store ra 0x52c
 store ra 0x543
halt:
 jumpu ra