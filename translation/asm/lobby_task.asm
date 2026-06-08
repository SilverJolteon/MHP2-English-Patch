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
		
		
	
.close