#!/usr/bin/python
## get module list
import subprocess
import time
import os
import sys
import logging
import settings
## get configuration
import configuration

#### VAR  ####
command = ['smpirun']
external_config = {'running_power': '--cfg=smpi/running_power:58e9', 'benchmark_path': configuration.BIN_PATH+'ep.A.1'}
###############

#### SAVE RESULT #####
def saveResult(msg):
	default_stdout = sys.stdout
	result_file = open("result.log","a")
	sys.stdout = result_file
	print(msg)
	result_file.close()
	sys.stdout = default_stdout
###############

#### DEUBG ####
def printLog(message):
	prefix = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "]"
	logging.info(prefix + "  " + str(message)) 
###############

#### generate sccript ####
def genScript(config):
	return ['smpirun','-np',config['num_procs'],'-platform', 'platform.xml','-hostfile', 'hostfile', config['running_power'],config['benchmark_path']]
###############

#### Start simulate ####
def run(sessionID):
	import settings
	config = settings.parseConfigFile(sessionID)
	os.chdir(configuration.SESSION_PATH+sessionID)
	settings.checkBinaryFiles(config)

	privatize_global_var = ''
	g500_arg = ''
	for app in config['benchmark']:
		if app['type']=='NAS':
			b_filename = app['kernel']+'.'+app['class']+'.'+app['numprocs']
			if app['kernel'] != 'ep':
				privatize_global_var = '--cfg=smpi/privatize_global_variables:yes'
		if app['type']=='himeno':
			b_filename = 'himeno'+'.'+app['class']+'.'+app['numprocs']
		if app['type']=='graph500':
			b_filename = 'graph500_smpi_simple'
			g500_arg = app['scale']


		command = ['smpirun','-np',app['numprocs'],'-platform','platform.xml','-hostfile','hostfile']
		command.append(privatize_global_var)
		command.append(configuration.BIN_PATH+b_filename)
		command.append(g500_arg)
		
		print command
		process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		saveResult(stdout)
		# printLog(stdout)
		printLog(stderr)

		process_id = process.pid
		printLog("Start process " + str(process_id))
	printLog('Finish Simuation for session: '+sessionID)
#############



#### LOGGER ####
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler('main.log', 'a'))
#############

############## TEST ###################
def main(argv):
    run('1')
if __name__ == "__main__":
    main(sys.argv)



