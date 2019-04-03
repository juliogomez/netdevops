# pyATS and Genie

## Introduction

pyATS is an Automation Test System written in Python. It provides the core infrastructure to define topologies, connect to network devices and run the required tests.

Genie builds on top of pyATS and it is fully integrated to provide model automation tests. It focuses on test cases for features (ie. BGP, HSRP, OSPF), and abstracts how this information is obtained from underlying devices. 

Together, pyATS and Genie enable you to create network test cases that provide __stateful__ validation of devices operational status. You can use them to validate how a new feature or product will affect your network, compare the status of your network before/after a change, customize your network monitoring based on your own business drivers.

The solution provides visibility on network devices health, by focusing not only on the _configurational_ state, but also on the _operational_ status.

It is agnostic and extensible, so any type of system could potentially be included by developing the right set of libraries. 

It can be integrated into CICD pipelines (implemented via integration servers like GitLab or Jenkins), other frameworks (like Robot, for almost-natural language stateful tests definition), or even interact with ChatBots (ChatOps).

It also integrates _beautifully_ with VIRL topologies, so you can focus only on what you want to test.

[pyATS Documentation](https://developer.cisco.com/docs/pyats)

The network topology you will use for testing is called the _testbed_, and it includes your devices and links. It is defined in a YAML file, and as long as pyATS is implemented in Python, _everything is an object_... including the testbed.

Your network devices are also objects in pyATS, so you can perform operations on them using _methods_:

* connect()
* ping(destination)
* execute('show version')
* configure('no ip domain lookup')

The output from these commands will be parsed by the system into structured data, so you can extract business-relevant data from them.

## Demos

Let's see it working.

The first thing you need to decide is _how_ you want to run pyATS: natively in your own system, or in a Docker container.

For the first option you should use a Python 3.X [virtual environment](https://virtualenv.pypa.io/en/latest/), so you don't clog your system, and then install the required tools (see [doc](https://developer.cisco.com/docs/pyats/#!python-virtual-environment)). 

However it is easier to run it [in a Docker container](https://developer.cisco.com/docs/pyats/#!docker-container), as the available image includes all required software, libraries and dependencies. So we will use this option for our demos.

Before starting please clone this repo in your local workstation, so you can execute the different scripts we will use during the demos.

```
$ git clone https://github.com/juliogomez/netdevops.git
$ cd netdevops/pyats
```

The sandbox you have reserved includes a _big_ VIRL server we will use to run some simulated devices for our demos. In order to easily manage it we will use a very handy utility called [virlutils](https://github.com/CiscoDevNet/virlutils).

You can install it in your workstation with:

```
$ pip install virlutils
```

Once done, please create a VIRL init file...

```
$ vi ~/.virlrc
```

... with the following content:

```
VIRL_USERNAME=guest
VIRL_PASSWORD=guest
VIRL_HOST=10.10.20.160
```

And then start a new terminal window in your workstation, so that it reads the new VIRL init file.

Now you are able to search for some example pre-defined simulated topologies that could be useful for testing.

```
$ virl search
```

You may even filter them, and for example look for the ones using _IOS_.

```
$ virl search ios
Displaying 1 Results For ios
╒════════════════════════╤═════════╤══════════════════════╕
│ Name                   │   Stars │ Description          │
╞════════════════════════╪═════════╪══════════════════════╡
│ virlfiles/2-ios-router │       0 │ hello world virlfile │
╘════════════════════════╧═════════╧══════════════════════╛
```

That is a simple template for a 2 IOS-routers simulation (kind of like a _hello-world for virlutils_).

Make sure you are connected to your sandbox VPN and then download the VIRL topology specified below, so that you can start it in your server.

```
$ virl pull virlfiles/genie_learning_lab
Pulling from virlfiles/genie_learning_lab
Saved topology as topology.virl
$ virl up
Creating default environment from topology.virl
Localizing {{ gateway }} with: 172.16.30.254
```

Now you have your VIRL simulation running in the sandbox server.

```
$ virl ls
Running Simulations
╒══════════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation               │ Status   │ Launched                   │ Expires   │
╞══════════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ netdevops_default_oAmstu │ ACTIVE   │ 2019-04-03T10:54:44.416113 │           │
╘══════════════════════════╧══════════╧════════════════════════════╧═══════════╛
```

You can also see the status of its included nodes.

```
$ virl nodes
Here is a list of all the running nodes
╒════════════╤══════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node       │ Type     │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞════════════╪══════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ csr1000v-1 │ CSR1000v │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.129        │ N/A                │
├────────────┼──────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ nx-osv-1   │ NX-OSv   │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.130        │ N/A                │
╘════════════╧══════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛
```

Once a node shows up as _ACTIVE_ and _REACHABLE_ you can connect to it (use password `cisco`) with:

```
$ virl ssh nx-osv-1
```

Please note that during the connection process you will need to confirm you want to add its IP address to the list of _known hosts_.

One of the fantastic features that _virlutils_ includes is that it can generate inventories to be used by other systems, using the command: `virl generate [ pyats | nso | ansible ]`

For our demos we will use the `pyats` one, so try it once that all nodes in your simulation are _REACHABLE_ (the first time it might take up to 4 mins).

```
$ virl generate pyats -o default_testbed.yaml
Writing default_testbed.yaml
```

With just a single command you have now a YAML file that defines your VIRL environment as a testbed to be used by pyATS straight away!

<p align="center"> 
<img src="imgs/200wow.gif">
</p>

__We are now READY to start our demos!__

Please note that by the end of the labs, when you are done with your simulation, you can easily tear it down with:

```
$ virl down
Removing ./.virl/default
Shutting Down Simulation netdevops_default_oAmstu.....
SUCCESS
```

### Demo 1: Execute a command on a network device

The most basic demo will show you how to use pyATS to execute a single command on a certain network device. In this case you will see in your screen how this script executes a `show version` in a CSR1000v.

Please review the content of [this script](./pyats/1-pyats-intro.py), and you will see it executes the following steps:

1. Load the required pyATS library
2. Load the pyATS testbed definition from file
3. Select a specific device from the testbed
4. Connect to that device
5. Execute a command in that device

Run the demo with an interactive container (`-it`), and pass it the enable password as an environment variable (`-e PYATS_AUTH_PASS=cisco`) and a mapped volume from your workstation to the container (`-v $PWD/pyats/:/pyats/demos/`):

```
$ docker run -it \
  -e PYATS_AUTH_PASS=cisco \
  -v $PWD:/pyats/demos/ \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/1-pyats-intro.py
```

### Demo 2: List interface CRC errors from different devices

In this case you will use pyATS and Genie to compile interface counters from multiple devices across the network and then check if there are any CRC errors in them. The script will use the same function to compile CRC errors information from 2 devices with different CLI (CSR1000v and Nexus switch), with the available parsers providing independance from the underlying device type.

Please review the content of [this script](./pyats/2-genie-intro.py), and you will see the following steps to execute:

1. Load the required pyATS and Genie libraries
2. Define a reusable function that obtains __all__ interface counters from a single device

    * If not connected to the device, connect to it
    * Load the platform parser for that specific device
    * Load the interface parsers for interfaces in that device
    * Learn info about those device interfaces to parse and return it as structured data

3. Load the pyATS and Genie testbeds definition from file
4. Select a specific device from the testbed
5. Call the function defined previously to obtain all interface counters from that device
6. Select another device, with a different CLI
7. Call the function defined previously to obtain all interface counters from that device
8. Merge all interface details from these 2 different devices (with different CLIs), into a single source (python dictionary)
9. Loop through the compiled data in that single source and show CRC errors for every interface

Run the demo with an interactive container (`-it`) that requires the enable password & login user/password as environment variables (`-e PYATS_AUTH_PASS=cisco -e PYATS_USERNAME=cisco -e PYATS_PASSWORD=cisco`) and a mapped volume from your workstation to the container (`-v $PWD/pyats/:/pyats/demos/`):

```
$ docker run -it \
  -e PYATS_AUTH_PASS=cisco \
  -e PYATS_USERNAME=cisco \
  -e PYATS_PASSWORD=cisco \
  -v $PWD:/pyats/demos/ \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/2-genie-intro.py
```