import sys
import os.path
import string
import random
import zipfile
from subprocess import Popen, PIPE

# import local module
import configuration
import settings
from runsim import printLog

sys.path.append('gen-py')

from connector import *
from connector.ttypes import *

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
        print'ping()'
        return 'ping from server'

    def simulate(self, sessionFile):
        printLog('Starting Simulation')
        simStatus = SessionStatus()
        if sessionFile is None:
            simStatus.status = 2
            simStatus.output = 'Session file not found.'
            printLog('Session file not found.')
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
        zip_file = os.path.join(session_working_dir, "zipfile.zip")
        f_zip_file = open(zip_file, "wb")
        f_zip_file.write(sessionFile)
        f_zip_file.close()
        printLog('Finish saving zip file')

        #Extract session file
        with zipfile.ZipFile(zip_file, "r") as z:
            z.extractall(session_working_dir)
        printLog('Finish extracting file')

        command = ['python', 'runsim.py', sessionID]
        process = Popen(command)

        simStatus.status = 0
        simStatus.output = sessionID
        return simStatus

    def getSessionStatus(self, sessionID):
        printLog('Initilaze getting session status function.')
        simStatus = SessionStatus()

        #Validate argument
        if sessionID is None:
            simStatus.status = 2
            simStatus.output = 'session ID is missing.'
            printLog(status.output)
            return simStatus

        if sessionID == '':
            simStatus.status = 2
            simStatus.output = 'session ID is empty.'
            printLog(status.output)

        # try:
        printLog('Get status for session: '+str(sessionID))
        session_working_dir = configuration.SESSION_PATH+str(sessionID)
        if os.path.isdir(session_working_dir):
            printLog(session_working_dir+' exists')
        else:
            simStatus.status = 2
            simStatus.output = 'Unable to find working directory for session '+str(sessionID)
            printLog(simStatus.output)
            return simStatus
        # Check status based on result logging
        if not os.path.isfile(session_working_dir+'/result.log'):
            simStatus.status = 0
            simStatus.output = 'Simulation is in progress. '+str(sessionID)
            printLog(simStatus.output)
            return simStatus
        else:
            benchmark_list = settings.parseConfigFile(sessionID)['benchmark']
            finished_list = settings.getFinishedBencharkList(sessionID)
            if not finished_list:
                simStatus.status = 0
                simStatus.output = 'Simulation is in progress '+str(sessionID)
                printLog(status.output)
                return simStatus
            else:
                for benchmark in benchmark_list:
                    if not (benchmark['type'] if benchmark['type'] != 'NAS' else 'NAS:'+benchmark['kernel']) in finished_list:
                        simStatus.status = 0
                        simStatus.output = 'Simulation is in progress '+str(sessionID)
                        printLog(simStatus.output)
                        return simStatus
                simStatus.status = 1
                simStatus.output = 'Simulation is finished '+str(sessionID)
                printLog(simStatus.output)
                return simStatus
        # except IOError as e:
        #   simStatus.status = 2
        #   simStatus.output = "I/O error({0}): {1}".format(e.errno, e.strerror)
        #   printLog(simStatus.output)

  #     except ValueError as e:
  #         simStatus.status = 2
  #         simStatus.output = "Value error({0}: {1})".format(e,errno. e.strerror)
        #   printLog.(simStatus.output)

  #     except:
  #         simStatus.status = 2
  #         simStatus.output = 'Unexpected error'
  #         printLog(simStatus.output)
        #   pprint(sys.exc_info())

        # printLog('Finish getSessionStatus')

        # return simStatus

    def getResultFile(self, sessionID):
        printLog('Execute getResultFile function')
        result = Result()

        if sessionID is None:
            result.status = 2
            result.benchmark_result = "sessionID not found"
            printLog(result.benchmark_result)
            return result
        if sessionID == '':
            result.StatusCode = 2
            result.benchmark_result = "sessionID not found"
            printLog(result.benchmark_result)
            return result

        result.status = settings.getSimulationStatus(sessionID)    
        if result.status == 0:
            result.benchmark_result = "Simulation session is not finished."
            printLog(result.benchmark_result)
            return result

        else:
            os.chdir(configuration.SESSION_PATH+sessionID)

            zip_filename = '/tmp/'+sessionID+'-result.zip'
            result_filename = 'result.log'
            zip_command = ['zip', zip_filename, result_filename]

            print ' '.join(zip_command) 

            process = Popen(' '.join(zip_command), shell=True)
            process.wait()
            printLog('Success compress result file to ' + zip_filename)

            with open(zip_filename,'rb') as file:
                # result.benchmark_result = file.readlines()
                result.resultfile = file.read()
                result.benchmark_result = 'You just got a successful simulation. Be gratefulb'
                printLog('Send back simulation result for session: '+sessionID)
                return result

if __name__ == '__main__':
    handler = SimulationServiceHandler()
    processor = SimulationSystemService.Processor(handler)
    transport = TSocket.TServerSocket(port=configuration.SERVER_PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
     
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
     
    printLog("Starting SIMULATION server at port:" + str(configuration.SERVER_PORT))
    server.serve()
    printLog('done!')