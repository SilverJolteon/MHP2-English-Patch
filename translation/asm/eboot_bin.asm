.psp

.open "build/ULJM05156/EBOOT.BIN", 0x088023AC
	; Guild Card English Keyboard	
	.org 0x088D91D8
		li 			a1, 0x2
		
	; Guild Card Message Character width	
	.org 0x088DC5D8
		sllv		v0, v0, zero
	.org 0x088DD9C0
		sllv		v0, v0, zero
		
	; Guild Card Message Lines
	.org 0x088DC5C0
		andi		v1, s3, 0x1F
	.org 0x088DC5E8
		sra			v0, s3, 0x5
	.org 0x088DD9A8
		andi		v1, s3, 0x1F
	.org 0x088DD9D0
		sra			v0, s3, 0x5
		
	; Guild Card Header BG Width
	.org 0x088DD1D4
		li			a3, 0x10C
	
	.org 0x088DD690 ; Weapon Usage Text Position
		li			a1, 0x81
	
	; Guild Card Treasure Page
	.org 0x088DDC70 ; "Treasures" X Position
		li			a1, 0x9A
	.org 0x088DDFA4 ; Area Names Max Length
		sb			zero, 0x94(v0)
	.org 0x088DDF5C ; Change string pointer offset
		lbu			a0, 0x0(fp)
		li			v1, 0x99A7640
	.org 0x088DDF78 ; Jump to lobby_task.ovl function
		jal			0x0993C338
		lw			a0, -0xB30(v0)
	.org 0x08947AEC
		.dh 0xA8 ; Mountains
		.dh 0xA5 ; Jungle
		.dh 0xA6 ; Desert
		.dh 0xA7 ; Swamp
		.dh 0xAA ; Forest&Hills
		.dh 0xA9 ; Volcano
		
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
		
	.org 0x0882153C ; Armor resistance values text X pos
		addiu		v0, s4, 0x54
	.org 0x088218B4 ; Armor "Hunter Type" value text X pos
		addiu		fp, s4, 0x62
	.org 0x08823EF4 ; Armor slots X pos
		addiu		v0, s5, 0x31
.close