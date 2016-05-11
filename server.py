import sys, glob, configuration, simulate, zipfile, config_handler
import os.path
sys.path.append('gen-py')
sys.path.insert(0, glob.glob('../../lib/py/build/lib.*')[0])

from system import SimulationSystemService
from system.ttypes import *

# from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class SimulationServiceHandler(object):

	def __init__(self):
		self.log = {}

	def simulate(self ,sessionFile):
		printlog('Starting Simulation')
		simStatus = SessionStatus()
		if sessionFile is None:
			simStatus.statusCode = 2
			printlog('No session file sent.')
			return simStatus

		#Check working directory
		printlog('Check working directory')
		working_dir = configuration.SESSION_PATH
		if os.path.isdir(working_dir):
			printlog(working_dir + " exists")
		else
			printlog(working_dir + " not found. Create a new onw.")
			os.makedirs(working_dir)

		#Allocate sessionID
		sessionID = RandomStringGenerator().get_random_with_time()
		printlog('Allocated session '+str(sessionID))
		session_working_dir = working_dir + str(sessionID)
		os.makedirs(session_working_dir)
		printlog('Create session dir at '+session_working_dir)

		#Save session file
		# Not tested
		printlog('Save session file to working directory')
		zip_file = os.path.join(session_working_dir,"session.zip")
		f_zip_file = open(zip_file,"wb")
		f_zip_file.write(sessionFile)
		f_zip_file.close()
		printlog('Finish saving zip file')

		#Extract session file
		with zipfile.Zipfile(zip_file,"r") as z:
			z.extractall(session_working_dir)
		printlog('Finish extracting file')

		#TODO: Handling config file
		# config = config_handler(sessionID)
		
		#TODO: Check binary benchmark application	
		
		#TODO: Run simulation

		#TODO: Save a PID of simulation process to a file

		#TODO: Save output result

	def getSessionStatus(sessionID):
		#Validate arguments

		#Check sessionID

		#Check PID
		pass

	def getResultFile(sessionID):
		printlog('Execute getResultFile function')
		result = Result()

		if sessionID is Node:
			result.statusCode = 2
			result.benchmark_result = "sessionID not found"
			printlog(result.benchmark_result)
			return result
		if sessionID == '':
			result.statusCode = 2
			result.benchmark_result = "sessionID not found"
			printlog(result.benchmark_result)
			return result
		try:
			printlog("")

handler = SimulationServiceHandler()
processor = SimulationSystemService.Processor(handler)
transport = TSocket.TServerSocket(port=configuration.SERVER_PORT)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
 
server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
 
print "Starting python server..."
server.serve()
print "done!"