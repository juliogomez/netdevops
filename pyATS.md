# pyATS and Genie

<!-- vscode-markdown-toc -->
* [Introduction](#Introduction)
* [Demos](#Demos)
	* [Demo 1: Execute a command on a network device](#Demo1:Executeacommandonanetworkdevice)
	* [Demo 2: List interface CRC errors from different devices](#Demo2:ListinterfaceCRCerrorsfromdifferentdevices)
	* [Demo 3: Interactive pyATS](#Demo3:InteractivepyATS)
	* [Demo 4: Working with Test Cases](#Demo4:WorkingwithTestCases)
	* [Demo 5: Profiling your network](#Demo5:Profilingyournetwork)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

## <a name='Introduction'></a>Introduction

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

## <a name='Demos'></a>Demos

Let's see it working.

The first thing you need to decide is _how_ you want to run pyATS: natively in your own system, or in a Docker container.

For the first option you should use a Python 3.X [virtual environment](https://virtualenv.pypa.io/en/latest/), so you don't clog your system, and then install the required tools (see [doc](https://developer.cisco.com/docs/pyats/#!python-virtual-environment)). 

However it is easier to run it [in a Docker container](https://developer.cisco.com/docs/pyats/#!docker-container), as the available image includes all required software, libraries and dependencies. So we will use this option for our demos.

The sandbox you have reserved includes a _big_ VIRL server we will use to run some simulated devices for our demos. In order to easily manage it we will use a very handy utility called [virlutils](https://github.com/CiscoDevNet/virlutils).

It also includes a _devbox_ with all required utilities pre-configured. So at this point you could decide to use the _devbox_ included in your sandbox to execute the demos, or rather configure your own system so you can continue using it later. If you decide to use the sandbox _devbox_ you can connect to it by running: `ssh developer@10.10.20.20`, and use password `C1sco12345`.

In any case, before starting please clone this repo into your system (sandbox _devbox_ or your local workstation), so you can execute the different scripts we will use during the demos.

```
$ git clone https://github.com/juliogomez/netdevops.git
$ cd netdevops/pyats
```

You can install _virlutils_ in your local workstation (no need to do it in the sandbox _devbox_) with:

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

That pyATS testbed definition file will need some variables to define the _enable password_ and _login user/password_.

```
$ export PYATS_AUTH_PASS=cisco
$ export PYATS_USERNAME=cisco
$ export PYATS_PASSWORD=cisco
```

__We are now READY to start our demos!__

Please note that by the end of the labs, when you are done with your simulation, you can easily tear it down with:

```
$ virl down
Removing ./.virl/default
Shutting Down Simulation netdevops_default_oAmstu.....
SUCCESS
```

### <a name='Demo1:Executeacommandonanetworkdevice'></a>Demo 1: Execute a command on a network device

The most basic demo will show you how to use pyATS to execute a single command on a certain network device. In this case you will see in your screen how this script executes a `show version` in a CSR1000v.

Please review the content of [this script](./pyats/1-pyats-intro.py), and you will see it executes the following steps:

1. Load the required pyATS library
2. Load the pyATS testbed definition from file
3. Select a specific device from the testbed
4. Connect to that device via SSH and configure the connection to be _automation-friendly_ (disable logging, change terminal width/length, no timeout)
5. Execute a command in that device

Run the demo with an interactive container (`-it`) that will be automatically deleted after execution (`--rm`), and pass it a mapped volume from your workstation to the container (`-v $PWD:/pyats/demos/`):

```
$ docker run -it --rm \
  -v $PWD:/pyats/demos/ \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/1-pyats-intro.py
```

### <a name='Demo2:ListinterfaceCRCerrorsfromdifferentdevices'></a>Demo 2: List interface CRC errors from different devices

In this case you will use pyATS and Genie to compile interface counters from multiple devices across the network and then check if there are any CRC errors in them. The script will use the same function to compile CRC errors information from 2 devices with different CLI (CSR1000v and Nexus switch), with the available Genie parsers providing independence from the underlying device type.

Please review the content of [this script](./pyats/2-genie-intro.py), and you will see the following steps to execute:

1. Load the required pyATS and Genie libraries
2. Define a reusable function that obtains __all__ interface counters from a single device

    * If not connected to the device, connect to it via SSH
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

Run the demo with an interactive container (`-it`) that will be automatically deleted after execution (`--rm`), and pass it a mapped volume from your workstation to the container (`-v $PWD:/pyats/demos/`):

```
$ docker run -it --rm \
  -v $PWD:/pyats/demos/ \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/2-genie-intro.py
```

### <a name='Demo3:InteractivepyATS'></a>Demo 3: Interactive pyATS

As you can see pyATS feels really _pythonic_, so wouldn't it be great to have the option to execute these steps interactively while developing your tests? Well, we got you covered!

[ipyATS](https://github.com/kecorbin/ipyats) is an iPython wrapper for pyATS and Genie, so that you can conveniently explore and develop your own tests in an interactive way.

You can easily install it with:

```
$ pip install ipyats
```

And run it with your VIRL testbed:

```
$ ipyats --testbed default_testbed.yaml
```

The great thing about being able to define the specific _testbed_ to use for this test is that you can reuse everything you create in different environments (eg. production, testing, datacenter 1, datacenter 2).

You can see the devices included in your own testbed:

```
In [1]: testbed.devices
Out[1]: TopologyDict({'nx-osv-1': <Device nx-osv-1 at 0x1171675c0>, 'csr1000v-1': <Device csr1000v-1 at 0x1174953c8>})
```

Create aliases for your devices:

```
In [2]: nx = testbed.devices['nx-osv-1']
In [3]: csr = testbed.devices['csr1000v-1']
```

You can now connect to your device (please make sure you have `telnet` installed in your system):

```
In [4]: csr.connect()
```

Ask if there are any links going _csr_ to _nx_:

```
In [5]: csr.find_links(nx)
Out[5]:
{<Link object 'csr1000v-1-to-nx-osv-1' at 0x117331b38>,
 <Link object 'csr1000v-1-to-nx-osv-1#1' at 0x11757d860>,
 <Link object 'flat' at 0x11757d780>}
```

Or execute a command in it:

```
In [6]: csr.execute('show version')
```

Probably by now you are thinking...

<p align="center"> 
<img src="imgs/201interestingstuff.jpg">
</p>

... and you are right!

Let's start by exploring what can be done with __genie.ops__ libraries.

How about easily obtaining from a device the complete table of routes __in a structured format__?

```
In [7]: routes = tasks.get_routing_table(nx)
```

This request will execute a number of commands in the device, compile all the received routing info and parse it into a structured format. Check the resulting dictionary:

```
In [8]: routes
```

It is __structured data__ that you can now easily query and process in your scripting!

For example, let's say you have a tool that needs to verify that a specific route (eg. 172.16.30.0/24) exists in the _management_ VRF of your Nexus switch.

```
In [9]: routes['vrf']['management']['address_family']['ipv4']['routes']['172.16.30.0/24']
Out[9]:
{'route': '172.16.30.0/24',
 'active': True,
 'source_protocol': 'direct',
 'metric': 0,
 'route_preference': 0,
 'next_hop': {'next_hop_list': {1: {'index': 1,
    'next_hop': '172.16.30.130',
    'updated': '03:59:48',
    'outgoing_interface': 'mgmt0'}}}}
```

Wow, that was easy! Think about the kind of processing and parsing you would have had to do in the past to go through the text output of all those commands. Now pyATS is compiling the information from all those commands and giving you a consolidated, structured view that you can easily work with.

If you are interested in understanding what that specific task does:

```
In [10]: show_source(tasks.get_routing_table)
def get_routing_table(dev):
    """
    returns a parsed and normalized routing table
    """
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    # The directory syntax is <feature>.<feature.<Feature>
    routing = abstract.ops.routing.routing.Routing(dev)
    routing.learn()
    return routing.info
```

This is a pretty neat way of _not-having_ to type all those commands, and just invoke the task. 

And of course, you can even create your own tasks!

Let's try now a different task, and learn about BGP in the _csr_:

```
In [11]: bgp = tasks.learn('bgp',csr)
```

Again, this task will run multiple BGP-related commands, iterating through all detected BGP neighbors, and provide you with a consolidated view that includes all relevant information in a structured format, so you can easily extract and process the specific data you require.

```
In [12]: bgp
```

Now let's explore what can be done with __genie.conf__ libraries.

For example, in order to work with BGP we need to import the required library:

```
In [13]: from genie.libs.conf.bgp import Bgp
```

And then could use it to learn the BGP configuration in our Nexus switch:

```
In [14]: bgps_nx = Bgp.learn_config(nx)
```

As long as there might be (potentially) several BGP instances we receive a _list_, and need to refer to its first entry (ie. 0):

```
In [15]: bgp_nx = bgps_nx[0]
```

You could also apply this configuration as an example, or a different one, to your device:

```
In [16]: bgp_nx.build_config()
```

Or remove all that BGP configuration:

```
In [17]: bgp_nx.build_unconfig()
```

You can check it's all gone with the same command we used in the _genie.ops_ section:

```
In [18]: bgp = tasks.learn('bgp',nx)
```

And easily apply all the BGP config back again:

```
In [19]: bgp_nx.build_config()
```

When you are done exploring ipyATS, you can exit with:

```
In [20]: exit()
```


### <a name='Demo4:WorkingwithTestCases'></a>Demo 4: Working with Test Cases

Now that you know how to run some basic tests with pyATS and Genie, it is time to explore how we could give it a proper structure to build a more complex test. That's what Test Cases are all about: a framework that allows you to build _repeatable_ and _complex_ testing processes.

Let's take a look at this example:

```
Task-1: basic_example_script
|-- commonSetup                                                           
|   |-- sample_subsection_1                                               
|   `-- sample_subsection_2                                               
|-- tc_one
|   |-- prepare_testcase                                                  
|   |-- simple_test_1                                                     
|   |-- simple_test_2                                                     
|   `-- clean_testcase                                                    
`-- commonCleanup                                                         
`-- clean_everything
```

The sections are quite simple:

* You can define a number of _tasks_ to run in your test case (in our example we have just 1 task)
* Then you will have some _common setup_ to do, structured in subsections 
* After that you would go into the real Test Case (_tc_), with 3 phases: preparation, execution and cleaning
* Finally, as a good citizen, you would need to _clean_ everything you set up during the _common setup_ phase

We can see it working in your setup. This time we will ask our pyATS container to provide an interactive shell (_ash_). We will use the _-alpine_ image because it has _vi_ already included in it, and you will need it to edit some files.

```
$ docker run -it --rm ciscotestautomation/pyats:latest-alpine ash
```

Once inside the container shell you have access to its directory structure and tools. Inside the `pyats` directory you will find multiple examples and templates to use with pyATS. To get started let's focus on a _basic_ one.

```
(pyats) /pyats # cd examples/basic
```

There you will find the `basic_example_script.py` python script file that defines a very simple Test Case. It includes all the sections mentioned before but actually not doing much (only logging)... so it is a good starting point as a template for your own test cases.

```
(pyats) /pyats/examples/basic# cat basic_example_script.py
```

To execute it you will need to define a _job_ that uses the python script. You can find it here:

```
(pyats) /pyats/examples/basic# cat job/basic_example_job.py
```

You would run the job like this:

```
(pyats) /pyats/examples/basic# pyats run job job/basic_example_job.py
```

You can see in the report shown at the end of the execution process that all tests in our task _PASSED_.

Let's insert a simple verification test in our test case. Please edit the python script with `vi basic_example_script.py`, scroll down to the _TESTCASES SECTION_ and look for the _First test section_. There insert the required code as per the following:

```
    # First test section
    @ aetest.test
    def simple_test_1(self):
        """ Sample test section. Only print """
        log.info("First test section ")
        self.a = 1
        self.b = 2
        if self.a != self.b:
            self.failed("{} is not {}".format(self.a, self.b))
```

As you can see we are defining 2 simple variables with fixed values of 1 and 2, and then inserting a conditional statement that fails if they are different. So obviously the test will now fail. Try it.

```
(pyats) /pyats/examples/basic# pyats run job job/basic_example_job.py
```

Check the execution logs and you will find how a failed test looks like when executing a test case:

```
...
2019-04-04T08:32:09: %AETEST-INFO: Starting section simple_test_1
2019-04-04T08:32:09: %SCRIPT-INFO: First test section
2019-04-04T08:32:09: %AETEST-ERROR: Failed reason: 1 is not 2
2019-04-04T08:32:09: %AETEST-INFO: The result of section simple_test_1 is => FAILED
...
2019-04-04T08:32:09: %EASYPY-INFO: +------------------------------------------------------------------------------+
2019-04-04T08:32:09: %EASYPY-INFO: |                             Task Result Summary                              |
2019-04-04T08:32:09: %EASYPY-INFO: +------------------------------------------------------------------------------+
2019-04-04T08:32:09: %EASYPY-INFO: Task-1: basic_example_script.commonSetup                                  PASSED
2019-04-04T08:32:09: %EASYPY-INFO: Task-1: basic_example_script.tc_one                                       FAILED
2019-04-04T08:32:09: %EASYPY-INFO: Task-1: basic_example_script.commonCleanup                                PASSED
2019-04-04T08:32:09: %EASYPY-INFO: +------------------------------------------------------------------------------+
2019-04-04T08:32:09: %EASYPY-INFO: |                             Task Result Details                              |
2019-04-04T08:32:09: %EASYPY-INFO: +------------------------------------------------------------------------------+
2019-04-04T08:32:09: %EASYPY-INFO: Task-1: basic_example_script
2019-04-04T08:32:09: %EASYPY-INFO: |-- commonSetup                                                           PASSED
2019-04-04T08:32:09: %EASYPY-INFO: |   |-- sample_subsection_1                                               PASSED
2019-04-04T08:32:09: %EASYPY-INFO: |   `-- sample_subsection_2                                               PASSED
2019-04-04T08:32:09: %EASYPY-INFO: |-- tc_one                                                                FAILED
2019-04-04T08:32:09: %EASYPY-INFO: |   |-- prepare_testcase                                                  PASSED
2019-04-04T08:32:09: %EASYPY-INFO: |   |-- simple_test_1                                                     FAILED
2019-04-04T08:32:09: %EASYPY-INFO: |   |-- simple_test_2                                                     PASSED
2019-04-04T08:32:09: %EASYPY-INFO: |   `-- clean_testcase                                                    PASSED
2019-04-04T08:32:09: %EASYPY-INFO: `-- commonCleanup                                                         PASSED
2019-04-04T08:32:09: %EASYPY-INFO:     `-- clean_everything                                                  PASSED
```

As you can see you don't need to be a Python expert to use the test cases framework. You have templates already available for you, where you can insert the specific tests you would like to run and execute them straight away.

You can now exit the container.

```
(pyats) /pyats/examples/basic# exit
```

### <a name='Demo5:Profilingyournetwork'></a>Demo 5: Profiling your network

So let's say you are responsible for a network and could use some help on how to be updated about possible issues happening in it. Wouldn't it be great to have a tool that helped you profiling your network end-to-end and storing that info as snapshots?

Let's focus, for example, on profiling everything related to BGP, OSPF, interfaces and the platforms in your network, and saving it to files. Ideally you would take a snapshot to learn how the network looks like when everything is working fine.

_Genie_ can help you do it with a simple command, specifying what features you want to learn (`ospf interface bgp platform`), from what specific testbed (`--testbed-file default_testbed.yaml`), and the directory where you want to store the resulting files (`--output good`):

```
$ docker run -it --rm -v $PWD:/pyats/demos/ ciscotestautomation/pyats:latest-alpine ash
(pyats) /pyats# cd demos
(pyats) /pyats/demos # genie learn ospf interface bgp platform --testbed-file default_testbed.yaml --output good
```

Inside the `good` directory, _console_ files show what commands were run to obtain all required info, while _ops_ files store the resulting information __in structured format__.

Now let's simulate something terrible happened in your network... by shutting down one of the loopback interfaces in your CSR1000v router. Well, it's not _that_ terrible, but you get the idea as an example of what _could have happened_.

First you need to identify the IP address of that CSR1000v, so you can connect to it:

```
(pyats) /pyats/demos # cat default_testbed.yaml | grep -A 1 GigabitEthernet1:
      GigabitEthernet1:
        ipv4: 172.16.30.129/24
```

Now you can SSH to it, with password `cisco`:

```
(pyats) /pyats/demos # ssh cisco@172.16.30.129
```

Once inside the system please shutdown interface loopback 1:

```
csr1000v-1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
csr1000v-1(config)#int lo 1
csr1000v-1(config-if)#shut
csr1000v-1(config-if)#exit
csr1000v-1(config)#exit
csr1000v-1#exit
Connection to 172.16.30.129 closed by remote host.
Connection to 172.16.30.129 closed.
(pyats) /pyats/demos #
```

In a real situation you would be receiving calls from users. "Something is wrong", "I lost connectivity", "My database stopped working". So instead of start your troubleshooting by _brute force_, how about asking Genie to determine what is the current status of the network, and even better _what changed_ since the last time you took the snapshot of the network in good state.

Let's do this by running the same command as previously, but asking the system to store the resulting files in a different directory (`--output bad`).

```
(pyats) /pyats/demos # genie learn ospf interface bgp platform --testbed-file default_testbed.yaml --output bad
```

And now find out what changed with a simple command.

```
(pyats) /pyats/demos # genie diff good bad
1it [00:00,  5.96it/s]
+==============================================================================+
| Genie Diff Summary between directories good/ and bad/                        |
+==============================================================================+
|  File: ospf_iosxe_csr1000v-1_ops.txt                                         |
|   - Identical                                                                |
|------------------------------------------------------------------------------|
|  File: platform_nxos_nx-osv-1_ops.txt                                        |
|   - Identical                                                                |
|------------------------------------------------------------------------------|
|  File: interface_iosxe_csr1000v-1_ops.txt                                    |
|   - Diff can be found at ./diff_interface_iosxe_csr1000v-1_ops.txt           |
|------------------------------------------------------------------------------|
|  File: bgp_nxos_nx-osv-1_ops.txt                                             |
|   - Diff can be found at ./diff_bgp_nxos_nx-osv-1_ops.txt                    |
|------------------------------------------------------------------------------|
|  File: ospf_nxos_nx-osv-1_ops.txt                                            |
|   - Identical                                                                |
|------------------------------------------------------------------------------|
|  File: bgp_iosxe_csr1000v-1_ops.txt                                          |
|   - Diff can be found at ./diff_bgp_iosxe_csr1000v-1_ops.txt                 |
|------------------------------------------------------------------------------|
|  File: platform_iosxe_csr1000v-1_ops.txt                                     |
|   - Identical                                                                |
|------------------------------------------------------------------------------|
|  File: interface_nxos_nx-osv-1_ops.txt                                       |
|   - Identical                                                                |
|------------------------------------------------------------------------------|
```

As you can see the system generates some files that signal exactly what has changed from the _good_ situation to the _bad_ one. In this specific case, the key file shows that Lo1 in the CSR1000v is now disabled:

```
(pyats) /pyats/demos # cat ./diff_interface_iosxe_csr1000v-1_ops.txt
--- learnt/interface_iosxe_csr1000v-1_ops.txt
+++ bad/interface_iosxe_csr1000v-1_ops.txt
info:
 Loopback1:
...
+  enabled: False
-  enabled: True
+  oper_status: down
-  oper_status: up
```

Talk about an easy way to determine why your network does not work as before, and what has changed exactly!

