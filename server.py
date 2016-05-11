import sys, glob, configuration, zipfile, random, string
from runsim import printLog
import os.path
sys.path.append('gen-py')

from system import *
from system.ttypes import *

# from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	    return ''.join(random.choice(chars) for _ in range(size))

class SimulationServiceHandler():

	def __init__(self):
		self.log = {}

	def ping(self):
		print('ping()')
		return 'ping from abc'

	def simulate(self ,sessionFile):
		printLog('Starting Simulation')
		simStatus = SessionStatus()
		if sessionFile is None:
			simStatus.StatusCode = 2
			printLog('No session file sent.')
			return simStatus

		#Check working directory
		printLog('Check working directory')
		working_dir = configuration.SESSION_PATH
		if os.path.isdir(working_dir):
			printLog(working_dir + " exists")
		else:
			printLog(working_dir + " not found. Create a new one.")
			os.makedirs(working_dir)

		#Allocate sessionID
		sessionID = id_generator()
		printLog('Allocated session '+str(sessionID))
		session_working_dir = working_dir + str(sessionID)
		os.makedirs(session_working_dir)
		printLog('Create session dir at '+session_working_dir)

		#Save session file	
		printLog('Save session file to working directory')
		zip_file = os.path.join(session_working_dir,"zipfile.zip")
		f_zip_file = open(zip_file,"wb")
		f_zip_file.write(sessionFile)
		f_zip_file.close()
		printLog('Finish saving zip file')

		#Extract session file
		with zipfile.ZipFile(zip_file,"r") as z:
			z.extractall(session_working_dir)
		printLog('Finish extracting file')

		#TODO: Handling config file
		# config = config_handler(sessionID)
		
		#TODO: Check binary benchmark application	

		#TODO: Run simulation

		#TODO: Save a PID of simulation process to a file

		#TODO: Save output result
		simStatus.StatusCode = 1
		simStatus.sessionID = sessionID
		return simStatus
	def getSessionStatus(sessionID):
		#Validate arguments

		#Check sessionID

		#Check PID
		pass

	def getResultFile(sessionID):
		printLog('Execute getResultFile function')
		result = Result()

		if sessionID is Node:
			result.StatusCode = 2
			result.benchmark_result = "sessionID not found"
			printLog(result.benchmark_result)
			return result
		if sessionID == '':
			result.StatusCode = 2
			result.benchmark_result = "sessionID not found"
			printLog(result.benchmark_result)
			return result

if __name__ == '__main__':
	handler = SimulationServiceHandler()
	processor = SimulationSystemService.Processor(handler)
	transport = TSocket.TServerSocket(port=configuration.SERVER_PORT)
	tfactory = TTransport.TBufferedTransportFactory()
	pfactory = TBinaryProtocol.TBinaryProtocolFactory()
	 
	server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
	 
	printLog("Starting SIMULATION server...")
	server.serve()
	printLog('done!')