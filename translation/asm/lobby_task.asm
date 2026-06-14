.psp

.open "build/ULJM05156/lobby_task.bin", 0x09923B00
	; Quest Menu Positioning
	.org 0x099A69B0 ; Reward
		.dh 0x14F
	.org 0x099A69BC ; ContractFee
		.dh 0x14F
	.org 0x099A69C8 ; Time Limit
		.dh 0x14F
	.org 0x099A69D4 ; Location
		.dh 0x14F
		
	; Gathering Hall Room Select	
	.org 0x09939FD0
		li a1, 0x4D ; BG X Position
		li a2, 0x06 ; BG Y Position
		li a3, 0x146 ; BG Width
		li t0, 0x104 ; BG Height
	.org 0x099A6130
		.dh 0xA0 ; Title X Position
		.dh 0x15 ; Title Y Position
		.dh 0x6B ; Left Room Column X Position
		.dw 0x00100038
		.dh 0x5B ; Left Room Column Cursor X Position
		.dh 0xFF ; Right Room Column X Position
		.dh 0xEE ; Right Room Column Cursor X Position
	
	; Chest UI
	.org 0x099ABE08 ; BG Width
		.dh 0x09
.close