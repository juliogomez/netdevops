from genie.conf import Genie

testbed = '/pyats/demos/default_testbed.yaml'
testbed = Genie.init(testbed)

# select a specific device from the testbed definition
csr = testbed.devices['csr1000v-1']

# connect to that device
csr.connect()

# execute a command in that device
csr.execute('show version')