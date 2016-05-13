#!/usr/bin/python
## get module list
import subprocess
import time
import os
import sys
import logging
import settings
import configuration #configuration of file paths


#### SAVE RESULT #####
def saveResult(output,b_type,kernel=''):
	default_stdout = sys.stdout
	result_file = open("result.log","a")
	sys.stdout = result_file
	if output is '':
		print('==========================================================')
		print(b_type+('-'+kernel if b_type=='NAS' else '')+' ERROR: RUNNING BENCHMARK FAILED')
		print('==========================================================')
	else:
		print('==========================================================')
		print('BENCHMARK RESULT FOR:'+b_type+(':'+kernel if b_type=='NAS' else ''))
		print('==========================================================')
		print(output)
		print('==========================================================')
	result_file.close()
	sys.stdout = default_stdout
###############

#### DEUBG ####
def printLog(message):
	prefix = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "]"
	logging.info(prefix + "  " + str(message)) 
###############

#### Start simulate ####
def run(sessionID):
	import settings
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

		print ' '.join(command)
		process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()

		# save output content to result file
		if app['type']=='NAS':
			saveResult(stdout,app['type'],app['kernel'])
		else:
			saveResult(stdout,app['type'])
		
		# printLog(stdout)
		printLog('\n'+stderr)

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
	if os.path.isfile(configuration.SESSION_PATH+'1/result.log'):
		os.remove(configuration.SESSION_PATH+'1/result.log')
	run('1')
if __name__ == "__main__":
    main(sys.argv)



