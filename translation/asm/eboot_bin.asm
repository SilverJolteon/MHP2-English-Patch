.psp

.open "build/ULJM05156/EBOOT.BIN", 0x088023AC
	; Guild Card English Keyboard	
	.org 0x088D91D8
		li 			a1, 0x2
		
	.org 0x088AED08 ; "Press the ○ button" Position
		li			a0, 0xAE
	.org 0x088ADD7C
		li			a0, 0xAE
	.org 0x088AD2D0
		li			a0, 0xAE
	.org 0x088AF1B4
		li			a0, 0xAE
		
	.org 0x088AD944 ; Character Select "Yes" Position
		li			a0, 0x15C
	.org 0x088AB5EC ; Character Select "No" Position
		addiu		v1, s4, 0x50
		
	.org 0x0882153C ; Armor resistance values text position
		addiu		v0, s4, 0x54
.close