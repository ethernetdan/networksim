Potluck Network Simulator
=========================

A tool to simulate a Potluck server network

**Note:**
The simulator is a development tool to aide the creation of a Potluck network visualizer. While the end result is similar to how Potluck works, it is not intended to accurately simulate the way that Potluck routes traffic across the cluster.


Install
-------
```sh
git clone https://github.com/potlck/networksim.git
cd networksim
pip install -r requirements.txt
```

Configure
---------
In *simulator.py*:
```python
# number of nodes in network
numNodes = 4500

# number of workers simulating clients
numWorkers = 30

# maximum page response time
maxPageLoadTime = 5

firebaseUrl = "<PUT YOUR FIREBASE URL HERE>"
```
Set each parameter to your liking. It is recommended that you keep the following things in mind:
* Each worker runs on it's own process so performance is tied to your hardware. 
* You must have a single node otherwise things aren't going to work
* Currently only works with a Firebase with no access rules but it wouldn't be hard to get it to work with a token

**IMPORTANT:** The simulator will create a new reference called 'potluck' a level below the base reference defined in *firebaseUrl*. 

Run
---
```sh
python simulator.py
```
