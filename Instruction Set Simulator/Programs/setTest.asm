start:
  move ra 0x7f
  store ra 0xff
  move ra 0x00
  sec 1
  sez 1
  jumpc 0xff