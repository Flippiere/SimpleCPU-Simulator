 start:
  move ra 0xff
  and ra 0xff
  store ra 0xff
  store ra 0xfe
  store ra 0xfd
 part1:
  move ra 0x00
  add ra 0x06
  sub ra 0x04
  and ra 0x00
  addm ra 0xf0
  subm ra 0xf0
  call subRoutine
  jumpu part2
 part2:
  move ra 0x00
  add ra 0x05
  jumpc wrongHalt
  load ra 0xff
  sub ra 0x01
  store ra 0xff
  jumpnz part1
  move ra 0xff
  and ra 0xff
  store ra 0xff
  load ra 0xfe
  sub ra 0x01
  store ra 0xfe
  jumpnz part1
  move ra 0xff
  and ra 0xff
  store ra 0xfe
  load ra 0xfd
  sub ra 0x01
  store ra 0xfd
  jumpnz part1
  jumpz halt
 wrongHalt:
  .data 0xfe
  .data 0xff
  .data 0xfe
  jumpu wrongHalt
 halt:
  jumpu halt
 subRoutine:
  move rb 0x7f
  or rb 0x7e
  rol rb
  add rb 0x01
  move rb 0x59
  move rc 0x5a
  store rb rc
  load rc rb
  add rc rb
  sub rc rb
  ror rc
  ret
  
