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
		
	; Unable to send guild card
	.org 0x088E0840
		li			a2, 0x80
	.org 0x088E08AC
		li			a2, 0x70
	.org 0x088E08C0
		li			a1, 0x90
	
	.org 0x088AED08 ; "Press the ○ button" Position
		li			a0, 0xAE
	.org 0x088ADD7C
		li			a0, 0xAE
	.org 0x088AD2D0
		li			a0, 0xAE
	.org 0x088AF1B4
		li			a0, 0xAE
	.org 0x088E08C8
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
		
	; Monster List
	.org 0x0881C060 ; Max Length Crown Sprite X Position
		addiu		v1, v1, 0x4E
	.org 0x0881C0B8 ; Min Length Crown Sprite X Position
		addiu		v1, v1, 0x4E
	.org 0x0881C1AC ; Monster Icon Background X Position
		addiu		v1, v1, 0x98
	.org 0x0881C1D8 ; Monster Icon X Position
		addiu		v1, v1, 0xAC
	.org 0x08911560 ; Monster List BG X Position
		.dh 0xE0
	.org 0x08911568 ; Monster List BG Width
		.dh 0x21
	
	.org 0x0889D340 ; sceUtilityNetconfInitStart - Guildhall "Connecting" message
		sw			s4, -0x4470(v0)
	.org 0x088AF9FC ; sceUtilitySavedataInitStart - "Game data corrupted" message
		sw			s4, 0x1C(s1)
	.org 0x088AFD98 ; sceUtilityMsgDialogInitStart - Error code message
		sw			s4, 0x68C(s1)
	.org 0x088AFE2C ; sceUtilityMsgDialogInitStart - Error with "No Monster Hunter Freedom Unite Game data was found."
		sw			s4, 0x68C(s0)
		
	; --------------------------------------
	; ~C02%s Formatted Strings - Copied from Freedom 2 [USA]
	; --------------------------------------
	.org 0x08850B7C
		lh			a0, 0xA(s0)
		li			v1, 0x0894058C
		sll			a0, a0, 0x1
		addu		v1, v1, a0
		lui			v0, 0x895
		lhu			a1, 0x0(v1)
		jal			0x08848E74
		lw			a0, 0x5F24(v0)
		move		s1, v0
		lui			v0, 0x895
		lw			a0, 0x5F24(v0)
		jal			0x08848E80
		lhu			a1, 0x8(s0)
		move		a1, s1
		move		a2, v0
		jal			0x08810F00
		addiu		a0, sp, 0x40
		nop
		nop
	.org 0x08851184
		li			a1, 0
		lh			a0, 0xA(s1)
		li			v1, 0x0894058C
		sll			a0, a0, 0x1
		addu		v1, v1, a0
		lui			v0, 0x895
		lhu			a1, 0x0(v1)
		jal			0x08848E74
		lw			a0, 0x5F24(v0)
		move		s0, v0
		lui			v0, 0x895
		lw			a0, 0x5F24(v0)
		jal			0x08848E80
		lhu			a1, 0x8(s1)
		lui			v1, 0x089E
		lh			a1, 0x28(sp)
		lh			a2, 0x2A(sp)
		lw			a0, -0x3368(v1)
		move		a3, s0
		j			ParseText
		nop
	.org 0x0880CD60
	ParseText:
		jal			0x08880DFC
		move		t0, v0
		j			0x0885160C
		nop
	.org 0x08850DE8
		jal			0x0887FDF0
	; --------------------------------------		
.close