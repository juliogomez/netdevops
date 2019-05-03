# Take snapshot of the operational state of the device
# and save the output to a file

*** Settings ***
# Importing test libraries, resource files and variable files.
Library        ats.robot.pyATSRobot
Library        genie.libs.robot.GenieRobot


*** Variables ***
# Define the pyATS testbed file to use for this run
${testbed}     ./default_testbed.yaml 

*** Test Cases ***
# Creating test cases from available keywords.

Connect
    # Initializes the pyATS/Genie Testbed
    use genie testbed "${testbed}"

    # Connect to both devices
    connect to device "nx-osv-1"
    connect to device "csr1000v-1"

Profile the devices
    Profile the system for "bgp;config;interface;platform;ospf;arp;routing;vrf;vlan" on devices "nx-osv-1;csr1000v-1" as "./good/good_snapshot"
