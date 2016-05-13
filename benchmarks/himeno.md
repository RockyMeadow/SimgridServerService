#Himeno Benchmark


[Himeno benchmark](http://accc.riken.jp/en/supercom/himenobmt/) has been developed by Dr. Ryutaro Himeno, Director of the Advanced Center for Computing and Communication. The main objective of himeno is to evaluate cpu performance of floating point operation by proceeding major loops of solving Poisson equation with Jacobi iteration method.


##Installation
1.  Download the source code:

	`$wget http://accc.riken.jp/en/wp-content/uploads/sites/2/2015/07/cc_himenobmtxp_mpi.zip`
        
2.  Unzip the file

	`$unzip cc_himenobmtxp_mpi.zip`
	`$cd cc_himenobmtxp_mpi`
	
3.  Change access permission and execute paramset.sh with following parameters

	`$chmod 755 paramset.sh`
	exp:`$./paramset.sh M 1 1 2`
	
	> **Note:** Parameter set for paramset.sh

	>`$./paramset.sh <grid size> <ID> <KD> <JD>`
	>
	> **ID**, **JD**, **KD** are partition sizes for I,J,K-dimensional	
	
	>| Grid size 	|              	|   	
	>|-----------	|--------------	|
	>| ssmall/XS 	| 32x32x64     	|   	
	>| small/S   	| 64x64x128    	|   	
	>| midium/M  	| 128x128x256  	|   	
	>| large/L   	| 256x256x512  	|   	
	>| elarge/XL 	| 512x512x1024 	|   	


4. You get the new "param.h"

5. Create a Makefile by using Makefile.sample

	`$cp Makefile.sample make`

6. Compile himenoBMTxps.c

	`$mpicc himenoBMTxps.c`

7. An executable file is created, then execute the program

	`$mpirun -np 2 ./a.out`
