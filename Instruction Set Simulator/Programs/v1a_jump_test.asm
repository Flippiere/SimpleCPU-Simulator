start:
  jumpu p3
p1:
  move 0x00
  jumpu p1
p2:
  move 0xff
  jumpnz p1
p3:
  sub 0x01
  jumpz p2
p4:
  add 0x02
  jumpnz p3
  jumpu p4
  
  