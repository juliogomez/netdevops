from ats.topology import loader
testbed = '/pyats/demos/default_testbed.yaml'
testbed = loader.load(testbed)

# select a specific device from the testbed definition
csr = testbed.devices['router1']
# connect to that device
csr.connect()
# execute a command in that device
csr.execute('show version')
