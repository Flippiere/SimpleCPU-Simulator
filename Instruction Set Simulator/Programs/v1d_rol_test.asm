start:
 rol ra
 rol ra
 move ra 0x7f
 rol ra
 rol ra
 rol ra
 rol ra
 move ra 0x0f
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 rol ra
 move rb 0x01
 move rc 0x10
rolloop:
 rol rb
 sub rc 0x01
 jumpnz rolloop
halt:
 jumpu halt