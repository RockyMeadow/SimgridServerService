#!/usr/bin/python
## get module list
import subprocess
import time
import os
import sys
import logging
#local modules
import settings
import configuration


#### SAVE RESULT #####
def saveResult(output,b_type,kernel=''):
	# default_stdout = sys.stdout
	result_file = open("result.log","a")
	# sys.stdout = result_file
	if output is '':
		result_file.write('==========================================================\n')
		result_file.write(b_type+('-'+kernel if b_type=='NAS' else '')+': RUNNING BENCHMARK FAILED\n')
		result_file.write('==========================================================\n')
	else:
		result_file.write('==========================================================\n')
		result_file.write(b_type+(':'+kernel if b_type=='NAS' else '')+': BENCHMARK RESULT\n')
		result_file.write('==========================================================\n')
		result_file.write(output)
		result_file.write('==========================================================\n')
	result_file.close()
	# sys.stdout = default_stdout
###############

#### DEUBG ####
def printLog(message):
	prefix = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "] "
	# logging.info(prefix + "  " + str(message)) 
	print(prefix+message)
###############

#### Start simulate ####
def run(sessionID):
	config = settings.parseConfigFile(sessionID)

	if not os.path.isdir(configuration.SESSION_PATH):
		printLog('SESSIONS directory not found. Create new directory.')
		os.makedirs(configuration.SESSION_PATH)

	os.chdir(configuration.SESSION_PATH+sessionID)
	settings.checkBinaryFiles(config)

	extra_arg = ''
	g500_arg = ''

	for app in config['benchmark']:
		if app['type']=='NAS':
			b_filename = app['kernel']+'.'+app['class']+'.'+app['numprocs']
			g500_arg = ''
			if app['kernel'] != 'ep':
				extra_arg = '--cfg=smpi/privatize_global_variables:yes'
		if app['type']=='himeno':
			b_filename = 'himeno'+'.'+app['class']+'.'+app['numprocs']
			extra_arg = '--cfg=surf/precision:1e-9'
			g500_arg = ''
		if app['type']=='graph500':
			b_filename = 'graph500_smpi_simple'
			g500_arg = app['scale']


		command = ['smpirun','-np',app['numprocs'],'-platform','platform.xml','-hostfile','hostfile']
		command.append(extra_arg)
		command.append(configuration.BIN_PATH+b_filename)
		command.append(g500_arg)

		print ' '.join(command) # uncomment this to debug command output
		process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		
		# Save pid to check progess 
		process_id = process.pid

		# Interact with process, read data from stdout and stderr
		# pid_file = open(os.path.join(configuration.SESSION_PATH,sessionID,process))
		stdout, stderr = process.communicate()

		# save output content to result file
		output = (stdout,stderr)
		if app['type']=='NAS':
			saveResult('\n'.join(output),app['type'],app['kernel'])
		else:
			saveResult('\n'.join(output),app['type'])
		
		# printLog('\n'+stdout)
		# printLog('\n'+stderr)

		process_id = process.pid
		printLog("Finish process " + str(process_id))
#############



#### LOGGER ####
# logging.basicConfig(level=logging.INFO, format='%(message)s')
# logger = logging.getLogger()
# logger.addHandler(logging.FileHandler('main.log', 'a'))
#############

############## MAIN ###################
def main(argv):
	print(sys.argv)
	sessionID = sys.argv[1]
	run(sessionID)
	printLog('\033[92m'+'Finish Simuation for session: '+sessionID+'\033[0m')
if __name__ == "__main__":
    main(sys.argv)



