.psp

.open "build/ULJM05156/demo_task.bin", 0x09923B00
	.org 0x09924824 ; Press Start Position
		li			a1, 0x1A	
		
	.org 0x09924F24 ; Title Menu Position
		li			a1, 0x28
		jal			0x0887FCFC
		li			a2, 0x14
.close