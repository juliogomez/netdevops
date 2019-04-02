from ats.topology import loader
testbed = '/pyats/demos/devnet_sandbox.yaml'
testbed = loader.load(testbed)

# select a specific device from the testbed definition
csr = testbed.devices['csr1000v']
# connect to that device
csr.connect()
# execute a command in that device
csr.execute('show version')
