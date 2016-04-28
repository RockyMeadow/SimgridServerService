#!/usr/bin/python
## get module list
import subprocess
import time
import sys

#### DEUBG ####
def printlog(message):
	prefix = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "]"
	print prefix + "  " + str(message)

###############

print(sys.argv)
#variable
numprocs = 1
platformfile = "cluster.xml"
hostfile = "cluster-hostfile"
session_id = 1
filepath = "/home/rockymeadow/GR/system/sessions/"+str(session_id)

#command
command = ['smpirun','-np',str(numprocs),'-platform', 'sessions/1/'+platformfile,'-hostfile', 'sessions/1/'+hostfile, '--cfg=smpi/running_power:58e9','./bin/ep.A.1']
printlog("Running command "+''.join(command))
#call smpi command
process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print stdout
print stderr
process_id = process.pid
printlog("Start process" + str(process_id))