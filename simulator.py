import random
import time
import sys
from firebase import firebase
from multiprocessing import Process, Value

# number of nodes in network
numNodes = 4500

# number of workers simulating clients
numWorkers = 30

# maximum page response time
maxPageLoadTime = 5

firebaseUrl = "<PUT YOUR FIREBASE URL HERE>"

def worker(num):
  fb = firebase.FirebaseApplication(firebaseUrl, None)
  values = Node.servers.values()
  while True:
    lb = random.choice(values)
    requestTime = (random.randrange(100)/100) * maxPageLoadTime
    lb.externalRequest(requestTime, fb)
    with count.get_lock():
      count.value += 1
    c = count.value
    rate = c/(time.time()-start)
    sys.stdout.write("\rRunning at " + str(rate) + " requests/second")
    sys.stdout.flush()

def wait(n):
  time.sleep(n)

def signalRequest(fb, start, end):
  fb.post(start+"/"+end, "request")

def signalResponse(fb, start, end):
  fb.post(start+"/"+end, "response")

class Node:
  servers = {}
  def __init__(self, name):
    self.name = name

  def internalRequest(self, payload):
    wait(payload)

  def externalRequest(self, payload, fb):
    if not hasattr(self, 'iter'):
      self.iter = Node.servers.itervalues()
    try:
      target = self.iter.next()
    except:
      if len(Node.servers) > 0:
        self.iter = Node.servers.itervalues()
        target = self.iter.next()
      else: raise LookupError("Not enough nodes")
    signalRequest(fb, self.name, target.name)
    target.internalRequest(payload)
    signalResponse(fb, self.name, target.name)

  @staticmethod
  def add_node():
    num = '%030x' % random.randrange(16**30)
    if not num in Node.servers:
      node = Node(num)
      Node.servers[num] = node
      return node
    else:
      return Node.add_node()

def setupNodes():
  for i in range(numNodes):
    Node.add_node()

if __name__ == '__main__':
  setupNodes()

  start = time.time()
  count = Value('i', 0)
  p = {}
  print "Press Enter to stop execution"
  for i in range(numWorkers):
    p[i]=Process(target=worker, args=(i,))
    p[i].start()

  raw_input("")
  for i in range(numWorkers):
    p[i].terminate()
