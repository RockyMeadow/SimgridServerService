c NPROCS = 1 CLASS = S
c  
c  
c  This file is generated automatically by the setparams utility.
c  It sets the number of processors and the class of the NPB
c  in this directory. Do not modify it by hand.
c  
        integer nprocs_compiled
        parameter (nprocs_compiled = 1)
        integer nx_default, ny_default, nz_default
        parameter (nx_default=32, ny_default=32, nz_default=32)
        integer nit_default, lm, lt_default
        parameter (nit_default=4, lm = 5, lt_default=5)
        integer debug_default
        parameter (debug_default=0)
        integer ndim1, ndim2, ndim3
        parameter (ndim1 = 5, ndim2 = 5, ndim3 = 5)
        logical  convertdouble
        parameter (convertdouble = .false.)
        character*11 compiletime
        parameter (compiletime='13 May 2016')
        character*5 npbversion
        parameter (npbversion='3.3.1')
        character*6 cs1
        parameter (cs1='smpiff')
        character*9 cs2
        parameter (cs2='$(MPIF77)')
        character*6 cs3
        parameter (cs3='(none)')
        character*6 cs4
        parameter (cs4='(none)')
        character*2 cs5
        parameter (cs5='-g')
        character*6 cs6
        parameter (cs6='(none)')
        character*6 cs7
        parameter (cs7='randi8')
