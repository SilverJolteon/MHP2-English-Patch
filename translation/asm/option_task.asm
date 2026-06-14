.psp

.open "build/ULJM05156/option_task.bin", 0x09923B00
	.org 0x099244FC ; Font Width
		li a1, 0xE
	.org 0x09924524 ; Alignment Offset
		nop
	.org 0x09924574 ; "MIN" X Position
		li a1, 0x10B
.close