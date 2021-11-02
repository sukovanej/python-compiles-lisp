DEFAULT_TEMPLATE = """
section .text          ;Code Segment
   global _start
	
_start:                ;User prompt
{}
   ; Exit code
   mov eax, 1
   mov ebx, 0
   int 80h
"""
