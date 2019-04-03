# pyATS and Genie

## Introduction

pyATS is an Automation Test System written in Python. It provides the core infrastructure to define topologies, connect to network devices and run the required tests.

Genie builds on top of pyATS and it is fully integrated to provide model automation tests. It focuses on test cases for features (ie. BGP, HSRP, OSPF), and abstracts how this information is obtained from underlying devices. 

Together, pyATS and Genie enable you to create network test cases that provide __stateful__ validation of devices operational status. You can use them to validate how a new feature or product will affect your network, compare the status of your network before/after a change, customize your network monitoring based on your own business drivers.

The solution provides visibility on network devices' health, by focusing not only on the _configurational_ state, but also on the _operational_ status.

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

However it would be easier to run it [in a Docker container](https://developer.cisco.com/docs/pyats/#!docker-container), as the available image includes all required software, libraries and dependencies. So we will use this option for our demos.

Before starting please clone this repo in your local workstation, so you can execute the different scripts we will use during the demos.

```
$ git clone https://github.com/juliogomez/netdevops.git
$ cd netdeveops
```

*** For these first demos we will be using [this testbed definition](./pyats/devnet_sandbox.yaml), including a couple of devices from the _always-on_ sandboxes: a CSR1000V (IOSXE) and a Nexus 9000 (NXOS). As long as you don't need to go through any reservation process, they are very convenient to use but they are sometimes quite slow and often unreliable.***

YOU NEED TO MAKE A RESERVATION FOR A sbx-multi-ios SANDBOX...

The sandbox you have reserved includes a _big_ VIRL server we will use to run some simulated devices for our demos. In order to easily manage it we will use a very handy utility called [virlutils](https://github.com/CiscoDevNet/virlutils).

You can install it in your workstation with:

```
$ pip install virlutils
```

Once done please create a VIRL init file...

```
$ vi ~/.virlrc
```

... with the following content:

```
VIRL_USERNAME=guest
VIRL_PASSWORD=guest
VIRL_HOST=10.10.20.160
```

And then start a new terminal window, so it reads the new VIRL init file.

Now you are able to search for some example pre-defined simulated topologies that could be useful for testing.

```
$ virl search
```

You may even filter them, and look for the ones using _IOS_.

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

Connect to your sandbox VPN and download the VIRL topology specified below, to start it in your server.

```
$ virl pull virlfiles/2-ios-router
Pulling from virlfiles/2-ios-router
Saved topology as topology.virl
$ virl up
Creating default environment from topology.virl
Localizing {{ dns_server }} with: 4.2.2.3
Localizing {{ gateway }} with: 172.16.30.254
Localizing rsa modulus 768 with: rsa modulus 1024
```

Now you have your VIRL simulation running in the sandbox server.

```
$ virl ls
Running Simulations
╒═════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation          │ Status   │ Launched                   │ Expires   │
╞═════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ virl_default_K83qto │ ACTIVE   │ 2019-04-03T07:19:37.995070 │           │
╘═════════════════════╧══════════╧════════════════════════════╧═══════════╛
```

You can also see its included nodes.

```
$ virl nodes
Here is a list of all the running nodes
╒═════════╤════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node    │ Type   │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞═════════╪════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ router2 │ IOSv   │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.118        │ N/A                │
├─────────┼────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ router1 │ IOSv   │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.117        │ N/A                │
╘═════════╧════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛
```

Once a node shows up as _ACTIVE_ you can connect to it (use password `cisco`) with:

```
$ virl ssh router1
```

Please note you will need to confirm you want to add its IP address to the list of _known hosts_.

One of the fantastic features that _virlutils_ includes is that it can generate inventories to be used by other systems, with `virl generate [ pyats | nso | ansible ]`

For our demos we will use the `pyats` one, try it.

```
$ virl generate pyats
Writing default_testbed.yaml
```

With just a single command now you have a YAML file that defines your VIRL environment as a testbed to be used by pyATS straight away!

<p align="center"> 
<img src="imgs/200wow.gif">
</p>

__We are now ready to start our demos!__

Please note that by the end of the labs, when you are done with your simulation, you can easily tear it down with:

```
$ virl down
Removing ./.virl/default
Shutting Down Simulation virl_default_K83qto.....
SUCCESS
```

### Demo 1: Execute a command on a network device

The most basic demo will show you how to use pyATS to execute a single command on a certain network device. Please review the content of [this script](./pyats/1-pyats-intro.py), and you will see the following steps to execute:

1. Load the required pyATS library
2. Load the pyATS testbed definition from file
3. Select a specific device from the testbed
4. Connect to that device
5. Execute a command in that device

Run the demo with:

```
$ docker run -it -v $PWD/pyats/:/pyats/demos/ ciscotestautomation/pyats:latest python3 /pyats/demos/1-pyats-intro.py
```

### Demo 2: Look for CRC errors across multiple devices

In this case you will use pyATS and Genie to compile interface counters from multiple devices across the network and then check if there are CRC errors in them. Please review the content of [this script](./pyats/2-genie-intro.py), and you will see the following steps to execute:

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




```
$ docker run -it -v $PWD/netdevops/pyats/:/pyats/demos/ ciscotestautomation/pyats:latest python3 /pyats/demos/2-genie-intro.py
```

-----

Additionally, [ipyATS](https://github.com/kecorbin/ipyats) is an iPython wrapper for pyATS and Genie you can use to develop your test cases. By default it provides you connectivity to a couple of devices from the _always-on_ sandboxes: a CSR1000V (IOSXE) and a Nexus 9000 (NXOS). So it is very convenient to easily get started with pyATS.


Finally install ipyATS and execute it:

```
root@3140943f041c:/??????# pip install ipyats
[... lots of installation logs ...]
root@3140943f041c:/??????# ipyats
[... more logs ...]
In [1]: 
```
