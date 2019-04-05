# pyATS and Genie

<!-- vscode-markdown-toc -->
* [Introduction](#Introduction)
* [Demos](#Demos)
	* [Demo 1 - Execute a command on a network device](#Demo1-Executeacommandonanetworkdevice)
	* [Demo 2 - List interface CRC errors from different devices](#Demo2-ListinterfaceCRCerrorsfromdifferentdevices)
	* [Demo 3 - Interactive pyATS](#Demo3-InteractivepyATS)
	* [Demo 4 - Working with Test Cases](#Demo4-WorkingwithTestCases)
	* [Demo 5 - Profiling your network for troubleshooting](#Demo5-Profilingyournetworkfortroubleshooting)
	* [Demo 6 - Check all BGP neighbors are Established](#Demo6-CheckallBGPneighborsareEstablished)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

## <a name='Introduction'></a>Introduction

pyATS is an Automation Test System written in Python. It provides the core infrastructure to define topologies, connect to network devices and run the required tests.

<p align="center"> 
<img src="imgs/202pyatslogo.jpg">
</p>

Genie builds on top of pyATS and it is fully integrated to provide model automation tests. It focuses on test cases for features (ie. BGP, HSRP, OSPF), and abstracts how this information is obtained from underlying devices. 

<p align="center"> 
<img src="imgs/203genie.png">
</p>

Together, pyATS and Genie enable you to create network test cases that provide __stateful__ validation of devices operational status. You can use them to validate how a new feature or product will affect your network, compare the status of your network before/after a change, customize your network monitoring based on your own business drivers.

The solution provides visibility on network devices health, by focusing not only on the _configurational_ state, but also on the _operational_ status.

It is agnostic and extensible, so any type of system could potentially be included by developing the right set of libraries. 

It can be integrated into CICD pipelines (implemented via integration servers like GitLab or Jenkins), other frameworks (like Robot, for almost-natural language stateful tests definition), or even interact with ChatBots (ChatOps).

It also integrates _beautifully_ with VIRL topologies, and we will show you how to do it so you can focus only on what you want to test in your network.

[pyATS Documentation](https://developer.cisco.com/docs/pyats)

The network topology you will use for testing is called the _testbed_, and it includes your devices and links. It is defined in a YAML file, and as long as pyATS is implemented in Python, _everything is an object_... including the testbed.

Your network devices are also objects in pyATS, so you can perform operations on them using _methods_:

* connect()
* ping(destination)
* execute('show version')
* configure('no ip domain lookup')

The output from these commands will be parsed into structured data, so your systems can easily extract business-relevant data from them.

## <a name='Demos'></a>Demos

0k, let's see it working.

The first thing you need to decide is _how_ you want to run pyATS: natively in your own system, or in a Docker container.

For the first option you should use a Python 3.X [virtual environment](https://virtualenv.pypa.io/en/latest/), so you don't clog your system, and then install the required tools (see [doc](https://developer.cisco.com/docs/pyats/#!python-virtual-environment)). 

However it is easier to run it [in a Docker container](https://developer.cisco.com/docs/pyats/#!docker-container), as the available image includes all required software, libraries and dependencies. So we will use this option for our demos.

<p align="center"> 
<img src="imgs/205ilovecontainers.jpg">
</p>

The sandbox you have reserved includes a _big_ [VIRL](http://virl.cisco.com/) server we will use to run some simulated devices for our demos. 

<p align="center"> 
<img src="imgs/204virllogo.png">
</p>

It also includes a _devbox_ with all required utilities pre-configured. So at this point you could decide to use the _devbox_ included in your sandbox to execute the demos, or rather configure your own system so you can continue using it later. If you decide to use the sandbox _devbox_ you can connect to it by running: `ssh developer@10.10.20.20`, and use password `C1sco12345`.

In order to easily manage the VIRL server we will use a very handy utility called [virlutils](https://github.com/CiscoDevNet/virlutils). You will only need to install _virlutils_ if you decide to use your own local workstation for the demos (no need to do it if you will be using the sandbox _devbox_).

```
$ pip install virlutils
```

Once done, please create a VIRL init file...

```
$ vi ~/.virlrc
```

... and define the required VIRL credentials:

```
VIRL_USERNAME=guest
VIRL_PASSWORD=guest
VIRL_HOST=10.10.20.160
```

Then start a new terminal window in your workstation, so that it reads the new VIRL init file configuration.

Now you should be able to search for some example pre-defined simulated topologies that could be useful for testing (you can find some more [here](https://github.com/VIRL-Open/sample-topologies)).

```
$ virl search
```

You may even filter those examples: ie. look for the ones including _IOS_ in their name.

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
$ mkdir tests
$ cd tests
$ virl pull virlfiles/genie_learning_lab
Pulling from virlfiles/genie_learning_lab
Saved topology as topology.virl
$ virl up
Creating default environment from topology.virl
Localizing {{ gateway }} with: 172.16.30.254
```

__Now you have your VIRL simulation running in the sandbox server!__

```
$ virl ls
Running Simulations
╒══════════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation               │ Status   │ Launched                   │ Expires   │
╞══════════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ netdevops_default_oAmstu │ ACTIVE   │ 2019-04-03T10:54:44.416113 │           │
╘══════════════════════════╧══════════╧════════════════════════════╧═══════════╛
```

<p align="center"> 
<img src="imgs/206power.jpg">
</p>

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

For our demos we will use the `pyats` one, so try it once that all nodes in your simulation are _REACHABLE_.

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

_Don't do it now_, but please note that by the end of our set of demos, when you are finally done with your simulation, you can easily tear it down with:

```
$ virl down
Removing ./.virl/default
Shutting Down Simulation netdevops_default_oAmstu.....
SUCCESS
```

### <a name='Demo1-Executeacommandonanetworkdevice'></a>Demo 1 - Execute a command on a network device

The most basic demo will show you how to use pyATS to execute a single command on a certain network device. In this case you will see in your screen how this script executes a `show version` on a CSR1000v.

Download the required script to your system:

```
$ curl -L https://raw.githubusercontent.com/juliogomez/netdevops/master/pyats/1-pyats-intro.py -o 1-pyats-intro.py
```

Please review [its content](./pyats/1-pyats-intro.py) and you will see it executes the following steps:

1. Load the required pyATS library
2. Load the pyATS testbed definition from file
3. Select a specific device from the testbed
4. Connect to that device via SSH and configure the connection to be _automation-friendly_ (disable logging, change terminal width/length, no timeout)
5. Execute a command in that device

Run the demo with an interactive container (`-it`) that will be automatically deleted after execution (`--rm`), and pass it a mapped volume from your workstation to the container (`-v $PWD:/pyats/demos/`):

```
$ docker run -it --rm \
  -v $PWD:/pyats/demos/ \
  -e PYATS_AUTH_PASS=cisco \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/1-pyats-intro.py
```

### <a name='Demo2-ListinterfaceCRCerrorsfromdifferentdevices'></a>Demo 2 - List interface CRC errors from different devices

In this case you will use pyATS and Genie to compile interface counters from multiple devices across the network and then check if there are any CRC errors in them. 

<p align="center"> 
<img src="imgs/207errors.gif">
</p>

The script will use the same function to compile CRC errors information from 2 devices with different CLI (CSR1000v and Nexus switch), with the available Genie parsers providing independence from the underlying device type.

Download the required script to your system:

```
$ curl -L https://raw.githubusercontent.com/juliogomez/netdevops/master/pyats/2-genie-intro.py -o 2-genie-intro.py
```

Please review [its content](./pyats/2-genie-intro.py) and you will see the following steps to execute:

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

### <a name='Demo3-InteractivepyATS'></a>Demo 3 - Interactive pyATS

As you can see pyATS feels really _pythonic_, so wouldn't it be great to have the option to execute these steps interactively while developing your tests? Well, we got you covered!

[ipyATS](https://github.com/kecorbin/ipyats) is an iPython wrapper for pyATS and Genie, so that you can conveniently explore and develop your own tests in an interactive way.

For our demos we will start a pyATS container and ask it to start an interactive shell (_bash_) so we can install ipyATS in it.

```
$ docker run -it --rm -v $PWD:/pyats/demos/ ciscotestautomation/pyats:latest bash
```

You can easily install it with:

```
root@2ad68679070c:/pyats# pip install ipyats
```

And run it with your VIRL testbed:

```
root@2ad68679070c:/pyats# ipyats --testbed demos/default_testbed.yaml
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

If you are interested in understanding what that specific _task_ does, you can find out with:

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

Now let's try a different task, and learn about _all-things- BGP in the _csr_ device:

```
In [11]: bgp = tasks.learn('bgp',csr)
```

Again, this task will run multiple BGP-related commands, iterating through all detected BGP neighbors, and provide you with a consolidated view that includes all relevant information in a structured format, so you can easily extract and process the specific data you require.

```
In [12]: bgp
```

Now let's explore what can be done with __genie.conf__ libraries.

For example, in order to work with BGP configurations we need to import the required library:

```
In [13]: from genie.libs.conf.bgp import Bgp
```

And then we could use it to learn the BGP configuration in our Nexus switch:

```
In [14]: bgps_nx = Bgp.learn_config(nx)
```

As long as there might be (potentially) several BGP instances we receive a _list_, and need to refer to its first entry (ie. 0):

```
In [15]: bgp_nx = bgps_nx[0]
```

We can also apply configurations, like this or a different one, to our device:

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
In [19]: bgp
Out[19]: {}
```

And easily apply all the BGP config back again:

```
In [20]: bgp_nx.build_config()
```

When you are done exploring ipyATS, you can exit with:

```
In [21]: exit()
root@2ad68679070c:/pyats# exit
```


### <a name='Demo4-WorkingwithTestCases'></a>Demo 4 - Working with Test Cases

Now that you know how to run some basic tests with pyATS and Genie, it is time to explore how we could give it a proper structure to build a more complex test. That's what Test Cases are all about: a framework that allows you to build _repeatable_ and _more sophisticated_ testing processes.

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

* You can define a number of _tasks_ to run in your test case (in the example above we have just 1 task)
* Then you will have some _common setup_ to do, structured in subsections 
* After that, you would go into the real Test Case (_tc_), with 3 phases: preparation, execution and cleaning
* Finally, as a good citizen, you would need to _clean_ everything you set up during the _common setup_ phase

Let's see it working in your own setup. In this case we will use the _-alpine_ image because it has _vi_ already included in it, and you will need it to edit some files during this demo. We will ask our pyATS container to provide a shell (_ash_ for _-alpine_ image) so we work with it interactively.

```
$ docker run -it --rm ciscotestautomation/pyats:latest-alpine ash
```

Once inside the container shell you have access to its directory structure and tools. Inside the `pyats` directory you will find multiple examples and templates to use with pyATS. To get started let's focus on a _basic_ one.

```
(pyats) /pyats # cd examples/basic
```

There you will find the `basic_example_script.py` python script file that defines a very simple Test Case. It includes quite some python code for all the sections mentioned before, but actually not doing much (in fact only logging)... so it is a good starting point as a template for your own test cases.

```
(pyats) /pyats/examples/basic# cat basic_example_script.py
```

It is executed with a _job_ that invokes the python script. You can find it here:

```
(pyats) /pyats/examples/basic# cat job/basic_example_job.py
```

You would run the job with `pyats run job ...`:

```
(pyats) /pyats/examples/basic# pyats run job job/basic_example_job.py
```

You can see in the report shown at the end of the execution process that all tests in our task _PASSED_.

Let's insert a simple verification test in our test case. Please edit the python script with `vi basic_example_script.py`, scroll down to the _TESTCASES SECTION_ and look for the _First test section_. There you need to insert the required code as per the following:

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

As you can see we are defining 2 simple variables with fixed values of 1 and 2, and then inserting a conditional statement that fails if they are different. So, obviously the test will now fail because 1 and 2 are different. 

<p align="center"> 
<img src="imgs/208thinking.gif">
</p>

Try it.

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

Once you are done you can exit the container.

```
(pyats) /pyats/examples/basic# exit
```

### <a name='Demo5-Profilingyournetworkfortroubleshooting'></a>Demo 5 - Profiling your network for troubleshooting

So let's say you are responsible for a network and could use some help on how to be updated about possible issues happening in it. Wouldn't it be great to have a tool that helped you profiling your network end-to-end and storing all that info as snapshots?

<p align="center"> 
<img src="imgs/209tellmehow.gif">
</p>

Let's focus, for example, on profiling everything related to BGP, OSPF, interfaces and the platforms in your network, and saving it to files. Ideally you would take a snapshot of your network when everything is working _superb_.

_Genie_ can help you do it with a simple command, specifying what features you want to learn (`ospf interface bgp platform`), from what specific testbed (`--testbed-file default_testbed.yaml`), and the directory where you want to store the resulting files (`--output good`):

```
$ docker run -it --rm -v $PWD:/pyats/demos/ ciscotestautomation/pyats:latest-alpine ash
(pyats) /pyats# cd demos
(pyats) /pyats/demos # genie learn ospf interface bgp platform --testbed-file default_testbed.yaml --output good
```

Inside the created `good` directory, _console_ files will show you what commands were run to obtain all required info, while _ops_ files will store the resulting information __in structured format__.

Now let's simulate something _terrible_ happened in your network... by shutting down one of the loopback interfaces in your CSR1000v router. Well, it's not _that terrible_, but you get the idea as an example of what _could have happened_.

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

Once inside the system please shutdown interface loopback 1, to simulate _that terrible catastrophe in your network_:

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
```

<p align="center"> 
<img src="imgs/210whathaveidone.gif">
</p>

In the real world, soon you would be receiving calls from users: "Something is wrong... _terribly_ wrong", "I lost ALL connectivity", "My database stopped working!". So instead of starting your troubleshooting by _brute force_, how about asking Genie to determine what is the current new status of the network after the outage, and even better _what changed exactly_ since the last time you took the snapshot of the network in good state.

Let's do this by running the same command as previously, but asking the system to store the resulting files in a different directory (`--output bad`).

```
(pyats) /pyats/demos # genie learn ospf interface bgp platform --testbed-file default_testbed.yaml --output bad
```

And now find out what changed with yet another simple command.

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

As you can see the system generates some files that signal _exactly_ what has changed from the _good_ situation to the _bad_ one. In this specific case, one of the files immediately shows that Lo1 in the CSR1000v has been disabled!

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

__Talk about an easy way to determine why your network is not working properly as before, and to find out what happened exactly!__

<p align="center"> 
<img src="imgs/211cool.gif">
</p>

### <a name='Demo6-CheckallBGPneighborsareEstablished'></a>Demo 6 - Check all BGP neighbors are Established

We will now explore another example that will help you check all BGP neighbors in your network are in the desired _established_ state. 

The test case is structured in the following sections:

* Common setup: connect to all devices included in your testbed.
* Test cases: learn about all BGP sessions in each device, check their status and build a table to represent that info. If there are neighbors _not in a established state_ the test will fail and signal this condition in an error message.

In order to run it you will first need to install `git` on your pyATS container, clone an examples repo, install a tool to create nice text tables (_tabulate_), go into the directory and execute the _job_: 

```
$ docker run -it --rm -v $PWD:/pyats/demos/ ciscotestautomation/pyats:latest-alpine ash
(pyats) /pyats # apk add --no-cache git
(pyats) /pyats # git clone https://github.com/kecorbin/pyats-network-checks.git
(pyats) /pyats # pip3 install tabulate
(pyats) /pyats # cd pyats-network-checks/bgp_adjacencies
(pyats) /pyats/pyats-network-checks/bgp_adjacencies # pyats run job BGP_check_job.py --testbed-file /pyats/demos/default_testbed.yaml
```

As a result you will find the following table in your logs, displaying all BGP neighbors in all your devices, and their current status 

```
2019-04-05T18:10:41: %SCRIPT-INFO: | Device     | Peer     | State       | Pass/Fail   |
2019-04-05T18:10:41: %SCRIPT-INFO: |------------+----------+-------------+-------------|
2019-04-05T18:10:41: %SCRIPT-INFO: | csr1000v-1 | 10.2.2.2 | established | Passed      |
2019-04-05T18:10:41: %SCRIPT-INFO: | nx-osv-1   | 10.1.1.1 | established | Passed      |
```

