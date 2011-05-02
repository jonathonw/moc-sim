Supported Processes
=======
Valid Process Declarations for the XML parser

Untimed MoC:
-------------------
 *  Zip 
 
	(partition constant 1, partition constant 2, input 1, input 2, output1)
	
 *  UnZip 
 
	(input 1, output 1, output 2)
	
 *  Mealy 
 
	(partition function, output function, next state function, initial state, input 1, output 1)
	
 *	Map
 
	(partition constant, output function, input 1, output 1)
	
 *	Scan
 
	(partition function, next state function, initial state, input 1, output 1)
	
 *	Scand
 
	(partition function, next state function, initial state, input 1, output 1)
	
 *  Source 
 
	(next state function, initial state, output 1)
	
 *  Init 
 
	(initial value, input 1, output 1)
	
Timed MoC:
-------------------
 *  Zip 
 
	(partition constant 1, partition constant 2, input 1, input 2, output1)
	
 *  UnZip 
 
	(input 1, output 1, output 2)
	
 *  Mealy 
 
	(partition function, output function, next state function, initial state, input 1, output 1)
	
 *  Source 
 
	(next state function, initial state, output 1)
	
 *  Init 
 
	(initial value, input 1, output 1)
	
Synchronous MoC:
-------------------
 *  Zip 
 
	(input 1, input 2, output1)
	
 *  UnZip 
 
	(input 1, output 1, output 2)
	
 *  Mealy 
 
	(output function, next state function, initial state, input 1, output 1)
	
 *	Map
 
	(output function, input 1, output 1)
	
 *	Scan
 
	(partition function, next state function, initial state, input 1, output 1)
	
 *	Scand
 
	(next state function, initial state, input 1, output 1)
	
 *  Source 
 
	(next state function, initial state, output 1)
	
 *  Init 
 
	(initial value, input 1, output 1)
	
Interfaces:
-------------------
 *  StripS2U 
 
	(input 1,output 1)
	
 *  StripT2U 
 
	(input 1,output 1)
	
 *  StripT2S 
 
	(partition constant,input 1,output 1)
	
 *  InsertS2T 
 
	(partition constant,input 1,output 1)
	
 *  InsertU2T
 
	(partition constant,input 1,output 1)
	
 *  InsertU2S
 
	(partition constant,input 1,output 1)
 
 Splitter:
-------------------
 *  Splitter 
 
	(input 1, output 1, output 2)