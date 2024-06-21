start:
 move ra 0xff
 add rb 0x7f
 move rb ra
 move rc 0x45
 move rc ra
 add rb 0xff
 move ra rb
 load ra rb
 store ra rb
 load ra rb
 store rb ra
 load rb ra
halt:
 jumpu halt