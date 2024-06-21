start:
 move ra 0x44
 call subone
 call halt
subone:
 move ra 0x01
 call subtwo
 move ra 0x01
 ret
subtwo:
 move ra 0x02
 call subthree
 move ra 0x02
 ret
subthree:
 move ra 0x03
 call subfour
 move ra 0x03
 ret
subfour:
 move ra 0x04
 call subfive
 move ra 0x04
 ret
subfive:
 move ra 0x05
 ret
halt:
 jumpu halt