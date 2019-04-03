from ats.topology import loader
from genie.conf import Genie
from genie.abstract import Lookup
from genie.libs import ops

# we define a function to get all interface counters for a device
def get_interface_counters(dev):
    """
    returns parsed and normalized interface counters
    """
    # Device must be connected so that a lookup can be performed
    if not dev.is_connected():
        dev.connect()

    # Load the appropriate platform parsers dynamically
    abstract = Lookup.from_device(dev)

    # Find the Interface Parsers for this device
    # The directory syntax is .
    # here the class is capitalized but the directory/files arent.
    intf = abstract.ops.interface.interface.Interface(dev)

    # Parse required commands, and return structured data
    intf.learn()
    return intf.info

# define where the testbed definition file is
testbed = '/pyats/demos/default_testbed.yaml'
# load the pyATS testbed
testbed = loader.load(testbed)
# load the Genie testbed from the pyATS one
testbed = Genie.init(testbed)

# select a device from the testbed
csr = testbed.devices['csr1000v-1']
# call our function to obtain counters for all interfaces from that device
csr_interface_details = get_interface_counters(csr)
print(csr_interface_details)

# select a different device from the testbed, with a different CLI
nx = testbed.devices['nx-osv-1']
# use the same function to obtain the counters for all interfaces from that device
nx_interface_details = get_interface_counters(nx)
print(nx_interface_details)

# now we will look for CRC error in ANY interface from ANY device... 
all_interfaces = dict()
all_interfaces['csr'] = csr_interface_details
all_interfaces['nxos'] = nx_interface_details

for device, interface_details in all_interfaces.items():
    for interface, details in interface_details.items():
        counters = details.get('counters')
        if counters:
            if 'in_crc_errors' in counters:
                counters = details['counters']
                crc = counters['in_crc_errors']
                print("Device: {} Interface: {} CRC Errors: {}".format(device, interface, crc))
