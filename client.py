#!/usr/bin/env python


import sys, glob
import threading
sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib.*')[0])

from connector import SimulationSystemService
from connector.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:

  # Make socket
  transport = TSocket.TSocket('localhost', 26102)

  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)

  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  # Create a client to use the protocol encoder
  client = SimulationSystemService.Client(protocol)

  # Connect!
  transport.open()

  # result = client.ping()
  # print result
  # print client.ping()
  
  mystatus = SessionStatus()
  sessionFile = open('/home/rockymeadow/session.zip','rb') 
  content = sessionFile.read()
  sessionFile.close()
  mystatus = client.simulate(content)
  sessionID = mystatus.output
  print str(mystatus.status)
  print sessionID
  
  # print('Get Status:')
  # sessionID = '2XUA4E5HQF'
  # currentStatus = client.getSessionStatus(sessionID)
  # print str(currentStatus.status)
  # print currentStatus.output

  # print client.ping()
  
  # Close!
  transport.close()

except Thrift.TException, tx:
  print '%s' % (tx.message)
