// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(LOOP)
	@KBD
	D=M // D = KBD
	@IS_NOT_PUSHED
	D;JEQ // if it is not pushed then goto IS_NOT_PUSHED
(IS_PUSHED)
	@i
	M=0 // i = 0
	@FILL_SCREEN
	0;JMP
(FILL_SCREEN)
	@i
	D=M // D = i
	@8192
	D=D-A
	@LOOP
	D;JEQ
	@i
	D=M
	@SCREEN
	A=A+D // SCREEN[i]
	M=-1
	@i
	M=M+1 // i++
	@FILL_SCREEN
	0;JMP
(IS_NOT_PUSHED)	
	@i
	M=0
	@CLEAR+SCREEN
	0;JMP
(CLEAR_SCREEN)
	@i
	D=M // D = i
	@8192
	D=D-A
	@LOOP
	D;JEQ
	@i
	D=M
	@SCREEN
	A=A+D // SCREEN[i]
	M=0
	@i
	M=M+1 // i++
	@CLEAR_SCREEN
	0;JMP

