<p align="center"> 
<img src="imgs/0frontpage.jpg">
</p>

<!-- vscode-markdown-toc -->
* [Network Programmability](#NetworkProgrammability)
	* [The challenge of Dynamic applications vs Static network](#ThechallengeofDynamicapplicationsvsStaticnetwork)
	* [What is Programmability](#WhatisProgrammability)
	* [Why Coding](#WhyCoding)
	* [What has changed?](#Whathaschanged)
		* [Modern Programming Languages & Tools](#ModernProgrammingLanguagesTools)
		* [Online Communities](#OnlineCommunities)
		* [API Maturity](#APIMaturity)
	* [Coding essentials](#Codingessentials)
		* [YANG data models](#YANGdatamodels)
		* [JSON and XML](#JSONandXML)
		* [NETCONF and RESTCONF](#NETCONFandRESTCONF)
		* [REST APIs](#RESTAPIs)
		* [API Documentation](#APIDocumentation)
		* [Python](#Python)
	* [Summary](#Summary)
* [NetDevOps](#NetDevOps)
	* [The challenge of network configuration today](#Thechallengeofnetworkconfigurationtoday)
	* [Network configuration as code](#Networkconfigurationascode)
* [Hands-on with NetDevOps](#Hands-onwithNetDevOps)
	* [NetDevOps Demo 1 - Automating network configuration from testing to production](#NetDevOpsDemo1-Automatingnetworkconfigurationfromtestingtoproduction)
		* [GitLab setup](#GitLabsetup)
		* [CICD setup](#CICDsetup)
		* [VIRL verifications](#VIRLverifications)
		* [Local environment setup (optional)](#Localenvironmentsetupoptional)
		* [Demo overview](#Demooverview)
		* [Summary](#Summary-1)
	* [NetDevOps Demo 2 - VPN Head End Management Platform (HEMP)](#NetDevOpsDemo2-VPNHeadEndManagementPlatformHEMP)
		* [Topology](#Topology)
		* [Building blocks](#Buildingblocks)
		* [Environment setup](#Environmentsetup)
		* [Demo overview](#Demooverview-1)
		* [Summary](#Summary-1)
	* [NetDevOps Demo 3 - Working with pyATS and Genie](#NetDevOpsDemo3-WorkingwithpyATSandGenie)
		* [Execute a command on a network device](#Executeacommandonanetworkdevice)
		* [Consolidate info from devices with different CLI](#ConsolidateinfofromdeviceswithdifferentCLI)
		* [Develop your own tests with interactive pyATS](#DevelopyourowntestswithinteractivepyATS)
		* [Working with Test Cases](#WorkingwithTestCases)
		* [Profiling your network for troubleshooting](#Profilingyournetworkfortroubleshooting)
		* [Check all BGP neighbors are established](#CheckallBGPneighborsareestablished)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

---

## <a name='NetworkProgrammability'></a>Network Programmability

Do you often ask yourself why we keep configuring our network devices in the same way we have been doing it for the last 30 years? Isn't it strange that we still have to log into each individual box and use command-line instructions to perform any changes? Do you wonder if there might be a more optimal way of configuring your infrastructure, instead of CLI? Does this way of working make you feel like any _simple_ change in your network is _complex_ to implement?

__You are not alone.__

<p align="center"> 
<img src="https://media.giphy.com/media/paN2mV7vuCXx6/giphy.gif">
</p>

There are definitely alternative and innovative ways of programming your network infrastructure. Yes, when you configure your network devices to adopt a certain behaviour, or implement a new available feature, you are _programming_ them. So one of the first things we should be looking for is more optimal ways of programming our infrastructure.

### <a name='ThechallengeofDynamicapplicationsvsStaticnetwork'></a>The challenge of Dynamic applications vs Static network

Furthermore, as the network _exists_ to provide connectivity for __applications__, we should take a look at how these are evolving. Agile microservices-based cloud-native development, DevOps automation with CICD pipelines, and automated unit testing, enable really __dynamic__ application development for quick time-to-market requirements. Let's not forget that software is one of the most important assets to differentiate modern enterprises from their competition. Being able to quickly implement new features, deploy new locations, or fix issues, is absolutely __key__ to their success.

<p align="center"> 
<img src="imgs/1staticnw.jpg">
</p>

For the last years, servers have been virtualized with Virtual Machines that can be automatically deployed in minutes. These days the trend is going to container-based microservices, that are deployed _insanely fast_. These are short-lived entities that may be deployed dynamically across hybrid cloud environments, interacting among them to provide the desired service with virtually _unlimited_ scalability, and adapting to any possible issues in the underlying infrastructure via declarative statements.

In comparison, network infrastructure is much more _static_. In order to accommodate requirements from application developers it needs to be faster, more flexible and cost-optimized. Today network configuration is often a completely manual process that makes any desired change across the network complex and slow. The more elements these changes include (eg. firewalls, load-balancers...) the more difficult it gets to make them quick, reliable and adaptable. This situation often leads to bare minimum configurations in the network, that allows for a faster deployment (eg. no security ACLs, no QoS config, or trunking every VLAN in an interface) but usually leading to much bigger concerns.

<p align="center"> 
<img src="imgs/2skeleton.jpg">
</p>

Infrastructure is full of products designed to be used by... _humans_. It may not always seem that way, but human operators are the target users for CLI and web interfaces. This means that when you need to get something done via these interfaces, you (or some other human) has to do the work.

You won't have to think back too far to remember the last time you needed to complete some bulk-task on a computer. The task probably involved a lot of clicking, typing, copying-and-pasting, or other mind-numbing repetitions. These human interfaces (and the paradigm of having humans do the work) are to blame for the bulk-work that we sometimes have to do to complete a task.

Our brain has a great capacity, but clearly human input/output interfaces with a computer (typing and reading) are not very _fast_. Our thoughts neck down to this tiny straw, which output-wise is like poking things with your meat sticks, or using words (speaking or tapping things with fingers). For example, machine typing usually happens at a 20th of the speed you are thinking. And I am talking ten-finger typing, let's not even go into two-thumb typing... 
So while Elon Musk finishes his [BMI](https://waitbutwhy.com/2017/04/neuralink.html) (Brain Machine Interface), aka Wizard Hat, we will have to explore alternative options that optimize how we configure our networks.

<p align="center"> 
<img src="https://28oa9i1t08037ue3m1l0i861-wpengine.netdna-ssl.com/wp-content/uploads/2018/04/Communication-Speed-GRAPH-1.png">
</p>

### <a name='WhatisProgrammability'></a>What is Programmability

Computers are _great_ at bulk-work, but if you want your computer to talk to your infrastructure and do something, you will need a machine-to-machine interface or __API__ ([Application Programming Interface](https://en.wikipedia.org/wiki/Application_programming_interface)): an interface designed for software pieces to interact with each other.

> _By 2020, only 40% of network operations teams will use the command line interface (CLI) as their primary interface, which is a decrease from 75% in 2Q18._ (Gartner, 2018 Strategic Roadmap for Networking)

_Network Programmability_ uses a set of software tools to deploy, manage and troubleshoot network devices and controllers _via APIs_, gathering data and driving configurations to enhance and secure application delivery. This software can on-box or off-box, and work on-demand or event-driven.

We can ask an API to:
* Take some action
* Provide us with some piece of information
* Store some piece of information

We use these machine-to-machine APIs to make _simple_ requests to our infrastructure, which in aggregate, enable us to complete _powerful_ tasks.

For example, you might use APIs to make simple requests like...
* Get the status for interface X
* Get the last-change time for interface X
* Shutdown interface X
* Set the description of interface X to "Interface disabled per Policy"

... and that way complete a powerful task like: _"Disable all ports that have been inactive for 30 days."_

Sure, you could do this manually, but wouldn't it be better to codify the process (write it once) and then let your computer run this task whenever you need it done?

Besides this, information included in API responses should be formed by data structures that can be programmatically _readable_ by machines (and ideally also by humans). Classic CLI responses are human-readable text, but very difficult to be interpreted by a machine, that needs to be parsed with great difficulty before being able to leverage the included information.

If you need information from your infrastructure, ask for it. Using a machine-to-machine API means your request will complete, your data retrieved in a programmatic data structure, or you will receive notification to the contrary. All done in a way that enables you to automate the interaction. APIs make it easy to send requests to your infrastructure, but what makes it easy to codify the processes?

### <a name='WhyCoding'></a>Why Coding

_Coding_ is the process of writing down instructions, in a language a computer can understand, to complete a specific task.

<p align="center"> 
<img src="https://media.giphy.com/media/OVtqvymKkkcTu/giphy.gif">
</p>

Let's consider a simple codified process that we are asking a computer to follow:
* For each switch in my network...
    * For each interface in the switch...
        * If the interface is down, and hasn't changed states in more than thirty days, then:
            * Shutdown the interface
            * Update the interface description to mention why it's been shut down

```python
for switch in my_network:
    for interface in switch:
        if interface.is_down() and interface.last_change() > thirty_days:
            interface.shutdown()
            interface.set_description("Interface disabled per Policy")
```

This is essentially the process that you, as a human, would go through to complete the same task. By taking the time to codify it (write it down in a machine interpretable language), you can now ask the computer to do the task whenever you need it done. You, the human, are providing the intelligence (what needs to be done and how it should be done), while letting the computer do the boring and repetitious work (which is what it does best).

<p align="center"> 
<img src="imgs/6not.jpg">
</p>

While the code sample above is a snippet of a larger script, and is calling other functions (like `interface.last_change()` and `interface.shutdown()`), implementing the utility functions is straightforward and the code shown is actual valid Python code that would complete the task. The core logic is that simple.

### <a name='Whathaschanged'></a>What has changed?

APIs and programming languages aren't new, so, why the recent hype?

Well... they have _matured!_

#### <a name='ModernProgrammingLanguagesTools'></a>Modern Programming Languages & Tools

Modern programming languages like JavaScript, Python, Go, Swift, and others are less cumbersome and more flexible than their predecessors. It used to be that you had to write 10,000 lines of C++ code to do anything useful, but with these modern languages (and packages and libraries available from their developer communities) you can do powerful things in less than 300 lines of code. Which is probably shorter, or on par with, most Cisco IOS configurations that you have worked with.

These languages, when combined with other modern developer tools (eg. Git repositories, Package management systems, Virtual environments, Integrated Development Environments) equip you with powerful development tools that enable you to automate your tasks and processes and begin creating your own set of powerful tools and workflows.

While these tools are great, and are now bringing rich value to the systems engineering discipline, we are also benefiting from another maturing area of the software development industry.

#### <a name='OnlineCommunities'></a>Online Communities

In the past, when you set out to create some script or program, you often had to start _from scratch_, working with low-level standard libraries included with your programming language and toolset of choice. This created a high barrier to entry (and massive global repetition) as software developers had to write the same _heavy lifting_ modules to get common tasks done. Take for example making a HTTPS web request, where they had to write code to:

* Open a TCP connection on port 443
* Handle TLS negotiation and exchange certificates
* Validate the certificates
* Manage the TCP connection (and any connection pooling)
* Format HTTP requests
* Interpret HTTP responses

That is a lot of work when all the developer wanted to do was to get or send some data to / from some remote server. This is the reason why engineers left this work to software developers.

Now, thanks to the Open Source community, social code-sharing and collaboration sites like GitHub, and public package repositories, the developer communities around these new modern programming languages are building and sharing Open Source software libraries that help to encourage reuse and reduce duplicate work. Leveraging these community-created libraries can save you tremendous amounts of time and effort, and they enable you to focus your time and effort on what you want your code to do: your codified process.

<p align="center"> 
<img src="https://media.giphy.com/media/5IqxJsqlCtkqc/giphy.gif">
</p>

You can make a HTTPS request without much personal investment, because of the work done by these online communities.

```shell
$ pip install requests
Collecting requests
  Using cached
<-- output omitted for brevity -->
$ python
>>> import requests
>>> requests.get("https://api.github.com")
<Response [200]>

```

What you are seeing here is the following:
* We installed a community library from a public package repository ( `pip install requests` )
* We entered a Python interactive shell ( `python` )
* We imported the library into our Python code ( `import requests` )
* We made a HTTPS request to https://api.github.com and it was successful ( `<Response [200]>` )

Starting with installing the `requests` package on our machine, in four typed lines in a terminal we were able to download and install the package and use it to make a HTTPS request (without having to think about the steps involved with making the HTTPS request).

Now that languages and tools have evolved to be useful for infrastructure engineers, APIs have become easier to work with.

#### <a name='APIMaturity'></a>API Maturity

Gone are the days where it took an expert programmer to work with a product's API. Previous API standards like SOAP proved themselves to be not so _simple_, and easier to use API models like RESTful APIs have taken their place.

Now, thanks to RESTful APIs and standardized data formats like JSON, you can make requests of your infrastructure with the same ease these modern programming languages provide.

### <a name='Codingessentials'></a>Coding essentials

Let's do a quick review of the different foundational coding building blocks that network engineers will need to understand and use when entering the programmability world.

<p align="center"> 
<img src="imgs/39codingessentials.gif">
</p>

#### <a name='YANGdatamodels'></a>YANG data models

Data models are conceptual representations of data, that define what specific information needs to be included and the format to represent it. A data model can be accessed by multiple source applications, via different communication protocols.

[YANG](https://en.wikipedia.org/wiki/YANG) (_Yet Another Next Generation_) is a data modelling language defined originally in [RFC 6020](https://tools.ietf.org/html/rfc6020) and updated later in [RFC 7950](https://tools.ietf.org/html/rfc7950). It uses XML to describe the data model for _network devices_, and it is composed of modules and sub-modules that represent individual YANG files. YANG modules are _self-documenting_ hierarchical tree structures for organizing data.

```
+--rw interfaces
      |  +--rw interface* [name]
      |     +--rw name                        string
      |     +--rw description?                string
      |     +--rw type                        identityref
      |     +--rw enabled?                    boolean
      |     +--rw link-up-down-trap-enable?   enumeration
      +--ro interfaces-state
         +--ro interface* [name]
            +--ro name               string
            +--ro type               identityref
            +--ro admin-status       enumeration
            +--ro oper-status        enumeration
            +--ro last-change?       yang:date-and-time
            +--ro if-index           int32
            +--ro phys-address?      yang:phys-address
            +--ro higher-layer-if*   interface-state-ref
            +--ro lower-layer-if*    interface-state-ref
            +--ro speed?             yang:gauge64
            +--ro statistics
               +--ro discontinuity-time    yang:date-and-time
               +--ro in-octets?            yang:counter64
               +--ro in-unicast-pkts?      yang:counter64
               +--ro in-broadcast-pkts?    yang:counter64
               +--ro in-multicast-pkts?    yang:counter64
               +--ro in-discards?          yang:counter32
               +--ro in-errors?            yang:counter32
               +--ro in-unknown-protos?    yang:counter32
```

As you can see in the previous example, YANG modules are used to model _configuration_ and _state_ data. Configuration data can be modified (_rw_), while State data can only be read (_ro_).

YANG is based on standards from IETF, OpenConfig and others. It is supported by most networking vendors in their own devices, and allows them to augment or deviate models, in order to include vendor / platform specific information.

<p align="center"> 
<img src="imgs/40yangdatamodel.png">
</p>

YANG data models are publicly available [here](https://github.com/YangModels/yang). As you browse through the hundreds of them, you might soon realize that finding the model you are looking for may be quite _time-consuming_. To make your life easier please take a look at [Cisco YANG Explorer](https://github.com/CiscoDevNet/yang-explorer), an open-source YANG browser and RPC builder application to experiment with YANG data models.

<p align="center"> 
<img src="imgs/41yangexplorer.png">
</p>

Once you decide to use YANG data models in your code, you will need to use libraries for your preferred programming language. If your choice is Python, as it is for many network engineers, you should definitely checkout [pyang](https://github.com/mbj4668/pyang). This Python library can be used to validate YANG modules for correctness, to transform YANG modules into other formats, and even to generate code from the modules.

Finally you might also be interested in taking a look at the capabilities offered by the [YANG Catalog](https://yangcatalog.org/), a registry that allows users to find models relevant to their use cases from the large and growing number of YANG modules being published. You may read-access it via NETCONF or REST, to validate YANG modules, search the catalog, view module's details, browse modules and much more.

#### <a name='JSONandXML'></a>JSON and XML

Now that we know how to model data and store it locally, we need to start considering how to communicate it machine-to-machine. It is critical that our system knows how to send requests to network devices, and what format to expect when receiving responses. 

The classic approach with CLI provides us with structured data:

```
GigabitEthernet1 is up, line protocol is up
Description: TO_vSWITCH0
  Internet address is 172.16.11.11/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
      reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full Duplex, 1Gbps, media type is RJ45
```

This type of text output is great for human-machine interaction, because our brain easily understands the information reading through it. However this is not a good format for machine-to-machine communication, because the system receiving this text would need to be programmed to _parse_ through it, in order to extract the values for the different included fields. Yes, we could program the system to do it, using [regular expressions](https://en.wikipedia.org/wiki/Regular_expression). But there would be important drawbacks: not only implementing how to extract the relevant keys and values, but also how to do it for different platforms and vendors. Please consider that each OS will provide a slightly / largely different text output to show the same kind of info. So we would need to parse things differently for each case... definitely not the best approach.

Considering that we have defined a common data model, let's also agree on a common format to exchange that data. Instead of the previous text we would like to receive something like the following:

```
{
    "description": " TO_vSWITCH0",
    "ipv4Address": "172.16.11.11",
    "ipv4Mask": "255.255.255.0",
    "portName": "GigabitEthernet1",
}
```

This is an example of data in _structured format_, and it is critical for our systems to easily process information exchanged between machines. 

There are two common formats for data interchange being used these days: JSON and XML.

##### JSON

[JSON](http://json.org/) (JavaScript Object Notation) is more _modern_ and commonly used by new APIs. With its simple _key:value_ approach, it is very lightweight, easy for systems to generate and parse, but also easy for humans to read. 

```
{
    "className": "GRETunnelInterface", 
    "status": "up",
    "interfaceType": "Virtual"
    "pid": "C9300-48U",
    "serialNo": "FCW2123L0N3",
    "portName": "Tunnel201"
}
```

> No, you don't need to know any JavaScript to work with JSON. They just happen to share the syntax, but no need at all to be a JavaScript developer when using JSON as the data transfer format between systems.

Python users can easily work with JSON, using its own standard library:

```
import json
```

This library allows you to easily work with JSON as native Python objects. Very often you will import JSON data into Python dictionaries, with an array of _key:value_ pairs that enables you to search for the field you require by just running a standard search for a certain _key_.

Later we will discuss communication protocols, but for your reference please make a note that both __REST APIs__ and __RESTCONF__ support JSON and XML.

##### XML

[XML]() (eXtensible Markup Language) is a bit older, but still used by a lot of APIs. It is used for data transfer, but sometimes also to store info. It is language-independent and designed to be self-descriptive, although, compared to JSON, _tagging_ makes it a little bit more _difficult_ to read for humans.

```
{
    <interface>
        <name>GigabitEthernet1</name>
        <description>TO_vSWITCH0</description>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:
                  iana-if-type">ianaift:ethernetCsmacd</type>
            <enabled>true</enabled>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>172.16.11.11</ip>
                    <netmask>255.255.255.0</netmask>
                </address>
            </ipv4>
    </interface>
}
```

> XML is _not_ the same as HTML: XML carries data, while HTML represents it.

Python users also benefit from multiple available resources to work with XML, like [ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html) objects, [Document Object Model (DOM)](https://docs.python.org/3/library/xml.dom.html), [Minimal DOM Implementation (minidom)](https://docs.python.org/2/library/xml.dom.minidom.html), and [xmltodict](hhttps://github.com/martinblech/xmltodict).

You may learn more about XML in [this tutorial](https://www.w3schools.com/xml/).

By now you should have a clearer view on the relationship between YANG and JSON/XML. YANG is the data model that shows information about network devices configuration and status. JSON and XML are data exchange formats to represent the information stored in the data model, so it can easily be understood by both machines and humans.

<p align="center"> 
<img src="imgs/42yangjsonxml.png">
</p>

JSON displays information in a _clearer_ way and will be used more frequently by modern systems. However XML is still required for multiple systems that support it exclusively.

#### <a name='NETCONFandRESTCONF'></a>NETCONF and RESTCONF

Now that we understand data models and data transfer formats, we need to consider what protocol to use in order to exchange that information. NETCONF and RESTCONF are different protocols that you will need to use depending on the availability provided by your platform.

##### NETCONF

Network Configuration Protocol ([RFC 6241](https://tools.ietf.org/html/rfc6241)), is a network management protocol developed and standardized by the Internet Engineering Task Force (IETF). It supports a rich set of functionality to manage _configuration_ and _operational_ data, being able to manage network devices _running_, _candidate_ and _startup_ configurations. The NETCONF protocol defines a simple mechanism through which a network device can be managed, configuration data can be retrieved, and new configuration data can be uploaded and manipulated. The NETCONF protocol uses Remote Procedure Calls (RPCs) for its paradigm, such as `get-config`, `edit-config`, or `get`. A client encodes an RPC in XML and sends it to a server using a secure, connection-oriented session (such as Secure Shell Protocol [SSH]). The client (application) initiates a connection using SSH port 830 towards the server (network device). The server responds with a reply encoded in XML, and there is a capability exchange during session initiation, using XML encoding.

<p align="center"> 
<img src="imgs/43netconf.png">
</p>

Let' take a look at an example on how we could use Python to connect to a device via NETCONF.

```
from ncclient import manager
import xml
import xml.dom.minidom

with manager.connect(host=RW_HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False, device_params={'name': 'default'}, allow_agent=False, look_for_keys=False) as m:
    # XML filter to issue with the get operation
    # IOS-XE 16.6.2+        YANG model called "ietf-interfaces"
    interface_filter = '''
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                    <interface>
                        <name>GigabitEthernet1</name>
                    </interface>
            </interfaces-state>
        </filter>
    '''
    result = m.get(interface_filter)
    xml_doc = xml.dom.minidom.parseString(result.xml)
```

We start by importing the NETCONF and XML libraries we will be using (`ncclient` is a Python library that facilitates client-side scripting and application development around the NETCONF protocol). Then we connect to the device IP (`RW_HOST`), using the specified port for SSH (`PORT`) and the required credentials (`USER`/`PASS`). Once connected we define specifically what we want to receive (`interface_filter`) and make the request (`m.get`). `get` is the method used to request _operational_ data, but you could also ask for _configuration_ data using `get-config`, or modify that configuration using `edit-config`. Final step is just to parse the result into a Python dictionary, using the minidom library, to be able to work it.

And _voilá_, you get an XML response showing _operational_ data for the requested interface.

```
<rpc-reply message-id="urn:uuid:50bf9d6e-7e5c-4182-ae6b-972a055ceef7" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>GigabitEthernet1</name>
        <admin-status>up</admin-status>
        <oper-status>up</oper-status>
        <phys-address>00:0c:29:6c:81:06</phys-address>
        <speed>1024000000</speed>
        <statistics>
          <in-octets>5432293472</in-octets>
          <in-unicast-pkts>28518075</in-unicast-pkts>
          ……………
          <out-octets>2901845514</out-octets>
          <out-unicast-pkts>18850398</out-unicast-pkts>
        </statistics>
      </interface>
    </interfaces-state>
  </data></rpc-reply>
```

##### RESTCONF

RESTCONF ([RFC 8040](https://tools.ietf.org/html/rfc8040)) is based on the idea of adding a REST API to NETCONF. It can manage manage configuration and operational data defined in YANG models, and the URLs, HTTP verbs, and Request bodies are automatically generated from those associated YANG models. RESTCONF uses HTTP(S) as transport, and supports both XML and JSON as data transfer formats, while NETCONF only supports XML. Also, RESTCONF supports only a _sub-set_ of NETCONF, so not all operations are supported. 

<p align="center"> 
<img src="imgs/44restconf.png">
</p>

Remember that since REST principles are being used, RESTCONF is based on _stateless_ connections. As such, every application using RESTCONF writes directly to the _running configuration_, with no support for _candidate configuration_.

Being based on REST, RESTCONF supports the following methods:

* GET, to read/retrieve info
* POST, to create a new record
* PATCH, to update only some values of an existing record
* PUT, to update all values of an existing record
* DELETE, to erase an existing record

Let's take a look at how to use it. 

```
url = 'https://RO_HOST/restconf/data/interfaces-state/interface=GigabitEthernet1'

header = {'Content-type': 'application/yang-data+json',
          'accept': 'application/yang-data+json'}

response = requests.get(url, headers=header, verify=False, auth=ROUTER_AUTH)
interface_info = response.json()
oper_data = interface_info['ietf-interfaces:interface']
```

In this case we are sending a HTTP(S) request to our network device REST API. The URL structure will include the network device IP address (`RO_HOST`) and the resource we are asking about (`interface=GigabitEthernet1`). Then we will have to define the HTTP headers to send, specifying in this case what is the content type we are sending (YANG encoded in JSON) and the content we expect to receive in the response (YANG encoded in JSON). Finally we parse the JSON into a Python dictionary and extract the relevant info from the structured data.

```
{
    "ietf-interfaces:interface": {
        "name": "GigabitEthernet1",
        "admin-status": "up",
        "oper-status": "up",
        "last-change": "2018-01-17T21:49:17.000387+00:00",
        "phys-address": "00:0c:29:6c:81:06",
        "speed": 1024000000,
        "statistics": {
            "in-octets": 5425386232,
            "in-unicast-pkts": 28489134,
            ……………
            "out-octets": 2899535736,
            "out-unicast-pkts": 18844784
        }
    }
}
```

So the overall picture looks like this now:

<p align="center"> 
<img src="imgs/45netconfrestconf.png">
</p>

Network devices information is modelled in YANG to make it consistent, independent of the underlying infrastructure. Then than information can be represented with JSON or XML, and accessed by mean of NETCONF or RESTCONF from a remote client.

#### <a name='RESTAPIs'></a>REST APIs

By now you might be wondering _what is REST?_ It stands for Representational State Transfer, and [it was born](https://www.ics.uci.edu/~fielding/pubs/dissertation/fielding_dissertation.pdf) from the need to create a scalable Internet, where software systems could interact with each other, in an uniform and efficient approach.

It is a simple-to-use communications architecture style (not a standard) for networked applications, based on the client-server model. It expects all information required for the transaction to be provided at the time of the request. Client could be an application or a REST client, like [Postman](https://www.getpostman.com/) for development and testing. Server could be a system, network device, or network management application.

REST is stateless, so the server will close the connection after the specified exchange is completed, and no state will be maintained on the server side. This way it makes transactions very efficient.

The same as you use a HTTP _get_ method when browsing the internet and the server provides you with a website in HTML format that your browser decodes to make it human readable, REST APIs answer to _get_ requests from other systems with structured data (in JSON or XML) specifically addressed to them.

Think about SDN and NFV, where different types of controllers need to communicate and exchange information with multiple devices. Applications sitting on top of those controllers can actually query anything that the controller knows about the network below it. This can be operational data, configuration data stats about a single device with a 10GE interface, etc. Applications then take this information, process it and then program the controller by sending a _post_ instead of a _get_ request.

RESTful APIs are REST-based APIs, based on response-request communications using the HTTP protocol for the following operations (CRUD): 

* Post: Create a new resource
* Get: Retrieve/Read a resource
* Put: Update an existing resource
* Delete: Delete a resource

It includes five components that may be required in each Request: 

* URL: application server and the API resource
* Auth: there are few different authentication methods, not standardized, required to identify who is making the request (HTTP Basic, Custom, OAuth, none)
* Headers: define _content-type_ and _accept-type_, communicating to the server the format of data we will send and expect to receive (JSON or XML)
* Request Body (optional): may be missing if no data is required to be sent with the request
* Method: What is the task we ask the server to perform (ie. use POST to create a new record, or PUT to update an existing one)

Let's take a look at the format in this example:

```
    url = DNAC_IP + '/api/v1/host?hostIp=' + client_ip
    header = {'content-type': 'application/json', 'Cookie': dnac_jwt_token} 
    response = requests.get(url, headers=header, verify=False)
    client_json = response.json()
    client_info = client_json['response'][0]
```

First we need to define the URL with the IP address of the end system (ie. `DNAC_IP`) and the route to the required resource (ie. `/api/v1/host?hostIp=` combined with the IP of an end system). Then we specify the required headers, defining what is the format we are sending (JSON) and the required auth cookie. With that info we open the connection, make the request and store the response to parse it.

As long as these are HTTP requests we are sending, server will answer with a HTTP status code, headers and a response body.

Some possible HTTP status codes:

* 2xx Success: 200 OK, 201 Created
* 4xx Client Error: 400 Bad Request, 401 Unauthorized (something is wrong the authentication), 404 Not Found (most likely URL is wrong, or payload is wrongly formatted)
* 5xx Server Error: 500 Internal Server Error

Headers will will define the _content-type_ (JSON or XML), cache control, date and enconding.

The response body will be the payload, including the requested data in JSON or XML, depending on the headers provided during the request.

```
Response 200 / success
Cache-Control →no-cache
Content-Type →application/json;charset=UTF-8
…
{
    "hostIp" : "10.93.140.35" , 
    "hostMac" : "00:0c:29:6d:df:40" , 
    "hostType" : "wired" , 
    "connectedNetworkDeviceId" : "601c9ead-576c-402d-bcb1-224235b1e020" , 
    "connectedNetworkDeviceIpAddress" : "10.93.140.50" , 
    "connectedInterfaceId" : "eb613db0-0994-44ec-9146-1b65346f3d07" , 
    "connectedInterfaceName" : "GigabitEthernet1/0/13" , 
    "connectedNetworkDeviceName" : "NYC-9300" , 
    "vlanId" : "123" , 
    "lastUpdated" : "1528324633014" , 
    "accessVLANId" : "123" , 
    "id" : "841f9433-0d2c-4735-afe8-beb7547b7883"
}
```

#### <a name='APIDocumentation'></a>API Documentation

Documentation is always essential, but in this case even more, because REST APIs are an architectural style, not a standard. So docs will define specifically what you need to send to your network device, and what you should expect in return. 

Quality of the API documentation is the most important factor in API adoption, because it determines how difficult is to work with your APIs. You might have the most powerful APIs, but if they are not documented correctly nobody will be able to leverage them.

APIs are very often documented in the platform itself, offering you the option to test them directly there without needing to write any code, or even know a programming language. 

<p align="center"> 
<img src="imgs/46dnacapi.png">
</p>

It is also common for them to offer you the option to automatically generate sample code in different programming languages, so you can directly use it in your developments.

<p align="center"> 
<img src="imgs/47dnacapi2.png">
</p>

#### <a name='Python'></a>Python

When talking about programmability and APIs you need to pick your favorite programming language to let your system know what you want it to do, and how it needs to communicate with your network devices APIs. The goal will be to automate and script actions using the APIs provided by network devices, controllers, and applications. There are a myriad of different options when choosing your programming language (Python, Ruby, Go, JavaScript, C#, etc) and each developer will have his/her own preferences.

One very good option for network engineers to get started with programming is Python. It is one of the most popular programming languages across the globe for several reasons:

* Lots of available resources
* Extensive libraries
* Most SDKs developed in Python
* Powerful and fast
* Ubiquitous
* Easy to learn and friendly
* Open
* Wide support on different devices and platforms
* Rich and active support communities
* Most wanted language in 2017 & 2018

### <a name='Summary'></a>Summary

APIs and programming languages have evolved and matured to the point of being useful and applicable to the domains of infrastructure engineers.

The _net-effect_ being that you can get powerful things done with relatively small amounts of code. And by so doing, you can automate the repetitious and/or labor intensive parts of your job freeing you up to focus your time and effort on tasks deserving of your intellect.

Network programmability provides consistent and dynamic infrastructure configuration by automating deployments and simplifying network management, bringing the following main benefits:

* Automation
    * Time and cost optimization
    * Reduce errors
* Integration
* Innovation

## <a name='NetDevOps'></a>NetDevOps

DevOps principles are not exclusive to software development, and some of them can definitely be applied to infrastructure configuration. NetDevOps brings the culture, technical methods, strategies and best practices of DevOps to network management.

Sometimes it is referred to by different names, like _DevNetOps_, _NetOps_, or _SuperNetOps_. But in general it is related to the more generic term _Network Reliability Engineer_ (also coming from the DevOps counterpart [Site Reliability Engineering](https://en.wikipedia.org/wiki/Site_Reliability_Engineering)).

### <a name='Thechallengeofnetworkconfigurationtoday'></a>The challenge of network configuration today

Networks exist to provide connectivity for end-systems and applications, so obviously they have a critical role in any type of service. _Everything_ needs connectivity, so the network is certainly a fundamental asset in any modern enterprise these days. Its functionality has become so critical that most business nowadays would not be able to survive without connectivity.

However there is a very common _perception_ that the network is actually _fragile_.

<p align="center"> 
<img src="imgs/3yoda.jpg">
</p>

Key network engineers that have been working long enough on a certain network become _gurus_. They are the ones that know the _why_ and _how_ of multiple specific configurations: why _that_ had to be done last year on those core routers, how many neighbors should be seen by a certain edge router, or what that propagated BGP community means. Every box has a _unique configuration_ to accommodate whatever was required at a specific point in time: troubleshooting or debugging a certain issue, that small fix in the routing protocol weight to determine the right interface to use, or those interfaces that are down and nobody knows if they should actually be up or not. Sequential and manual provisioning leads into a situation where each network device becomes a _snowflake_, due to how its configuration has changed organically according to whatever was required along since it was installed.

Without these key engineers there is a _fear_ that network changes will go _wrong_. So operations teams tend to minimize the number and frequency of changes in their networks. Nobody wants to affect that _precious_ business traffic and be pointed at by the CTO as the person responsible for that big failure. So changes rarely happen. And when they happen they are _BIG_, because there is a backlog of things to do. The bigger the change, the more possibilities that something will fail. Besides this, teams are not well practiced because changes do not happen often. Fixing an issue while operating a network _live_, or performing a rollback quickly, requires practice. So now any problem that happens during the maintenance window will lead to the perception that the network configuration change was a _failure_.

Furthermore, applying network-wide policies becomes a task proportionally tedious to how big the network is. For example, consider a possible Infosec recommendation to change SNMP strings every 3 months. Doing it manually in a big network might require a number of engineers performing those changes simultaneously across the network, maybe during a maintenance window by night to make sure systems can be synchronized next morning. This manual process involves quite some manual interaction, which is definitely prone to errors.

<p align="center"> 
<img src="https://media.giphy.com/media/10PcMWwtZSYk2k/giphy.gif">
</p>

This type of considerations is very similar to the ones they had in classic software development. With their monolith architectures and bi-annual software updates, they suffered from similar challenges. And then they started doing things different, with things like Agile, DevOps, CICD pipelines and automated unit testing.

Applying this same type of principles to network configuration is what we called NetDevOps, and it will provide similar benefits to the ones software developers obtained while implementing this practices in their own environment. But it will require big cultural changes, like:
* _Embracing failure_ and learning from it for the future
* Understand that _change is good_
* _Collaborate actively_ between network developers and operations teams
* _Empower teams_ to take ownership and responsibility
* Provide _feedback systems_ that are actually useful to iterate and improve processes
* End-to-end _automation_ for the whole lifecycle of changes

<p align="center"> 
<img src="imgs/4culture.png">
</p>

What if network engineers started working with network configurations the same way software developers work with their code?

What if we could create automated pipelines for those network configurations, that worked like CICD does for software development?

What if the network could be continuously monitored for health and improvement?

Now __that__ would be a game changer. Not only in the way we manage our networks, but also in how we scale up, how we automate repetitive tasks, how different teams collaborate, and how we improve the reliability of our networks.

Let's explore it.

### <a name='Networkconfigurationascode'></a>Network configuration as code

With the advent of Cloud computing we have now the capabilities to provision and manage _ephemeral_ data centre resources (compute and connectivity) via machine-readable definition files. These files can be treated as common code, utilizing the same version control systems and best practices we use for software development, with goals like providing automation, improving efficiency and reducing errors. This is called _Infrastructure as Code_, or IaC.

We could follow the same approach with network device configurations, and this is what we call _Network as Code_. It is based on the idea of storing all network configurations in a [Version Control System](https://en.wikipedia.org/wiki/Version_control) (VCS) that manages and tracks changes in the network. This system storing all configurations for the whole network would be considered the [Single Source of Truth](https://en.wikipedia.org/wiki/Single_source_of_truth) for all-things network configuration.

In this new mode of operation, network configuration changes are proposed in code _branches_, like software code developers do. These branches are _safe_ places where network developers will be able to work _safely_ on their proposed configurations, without affecting the _master_ branch, where master configurations reside. Once these configurations are ready, developers will request their branch to be _merged_ with the master configurations, and will go through an approval process to verify there are no issues when incorporating these changes.

Continuing with the emulation of DevOps automation capabilities, this will lead into using CICD (Continuous Integration and Delivery) Build Servers to automatically deploy and test the proposed configurations in testing, staging and production environments. Configurations that successfully pass the complete tests set, will be deployed into the production environment. In case of failure during that final deployment, the system itself will automatically rollback the proposed changes, leaving the production network in the previous state just before the change.

<p align="center"> 
<img src="imgs/5cicd.png">
</p>

And considering that modern network devices support modern interfaces and APIs, let's leverage those to deploy our configurations across the network in an optimal way, instead of using the classic, slow and error-prone command-line interface.

Following this strategy, we are now ready to start building a completely automated environment to deploy and test configuration changes across the network.

## <a name='Hands-onwithNetDevOps'></a>Hands-on with NetDevOps

Now that you know about some of the most important building blocks for programmability, it is time to see them working together and how they are used to build business-relevant solutions that help managing our networks. And what better way to learn about them than getting our hands _dirty_ by going through some demos?

<p align="center"> 
<img src="imgs/99morpheus.jpg">
</p>

The following set of demos requires a [sandbox](https://developer.cisco.com/site/sandbox/): an environment where you have all the required platforms and elements that you will need for those demos. In our case we need a _big_ server to run VIRL simulations for all network devices we will discuss later, and another server to run our VCS, NSO, etc.

You may find the required sandbox for our demo using [this link](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology), and book it for up to one week exclusively for you.

<p align="center"> 
<img src="imgs/7reserve.png">
</p>

_Note: when doing the reservation please choose 'None' for simulation, as we will be launching the required topologies as part of the setup process._

Spinning up the whole system will take roughly 15 mins, so please look at this strangely satisfying pendulum while we get everything ready for you.

<p align="center"> 
<img src="imgs/8pendulum.gif">
</p>

Once the setup is ready you will receive an email with all required information to VPN into your sandbox. If you do not have a VPN client you may download AnyConnect [here](https://developer.cisco.com/site/sandbox/anyconnect/). Connect to your VPN and you are now ready to start working on your demos!

### <a name='NetDevOpsDemo1-Automatingnetworkconfigurationfromtestingtoproduction'></a>NetDevOps Demo 1 - Automating network configuration from testing to production

NetDevOps will deliver consistent version-controlled infrastructure configurations, deployed with parallel and automated provisioning. 

And what better way of understanding the real benefits of NetDevOps than building your own setup and seeing how it works? The goal will be to create a complete environment that demonstrates the following benefits _across the whole network_:

* Track the status of network configurations at any point in time
* Track who proposed and approved each specific configuration change
* Provide visibility on what are the differences of configurations at any point in time vs a previous situation
* Enable rollback to any previous moment
* Provide syntax-checking capabilities for network changes in your own local workstation
* Automate the deployment of any proposed change across different environments (eg. testing, staging, production)
* Model simulated virtual environments to test proposed changes before going to production
* Define and run the required tests set and passing criteria, both in testing and production, before accepting a change as successful
* Automatically rollback any proposed configuration that does not pass the tests set

These are the building blocks we will use to provide such a comprehensive demonstration:

* [GitLab](https://about.gitlab.com/): Version Control Server (VCS) with integration capabilities to provide automated pipelines 
* [Cisco Network Services Orchestrator](https://developer.cisco.com/site/nso/): formerly Tail-f, it provides end-to-end automation to design and deliver services much faster
* [pyATS](https://developer.cisco.com/pyats/): automation tool to perform stateful validation of network devices operational status with reusable test cases
* [VIRL](http://virl.cisco.com/): network modelling and simulation environment
* [Ansible](https://www.ansible.com/): simple automation

#### <a name='GitLabsetup'></a>GitLab setup

Open a terminal window (ie. [putty](https://www.putty.org/) on Windows or `terminal` on OSX) and `ssh` to your _devbox_ with the following credentials: `developer`/`C1sco12345`

```
$ ssh developer@10.10.20.20
```

Once in, clone the repository that includes all required files to build the setup into your _devbox_.

```
[developer@devbox ~]$git clone --recurse-submodules https://github.com/DevNetSandbox/sbx_multi_ios.git
```

With that, your sandbox _devbox_ includes now all required info to start building the environment.

```
[developer@devbox ~]$cd sbx_multi_ios/gitlab
[developer@devbox gitlab]$./setup.sh
```

`setup.sh` will start and configure your Version Control Server, a GitLab instance inside a Docker container running in your _devbox_. 

The process will take like 5 minutes, so check this out in the meanwhile.

<p align="center"> 
<img src="imgs/9pendulum2.gif">
</p>

Once your terminal shows the process is finished, you may check with `docker ps` that your GitLab containers are running, and how they offering their service in port 80.

```
[developer@devbox gitlab]$docker ps
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS                PORTS                                                                                       NAMES
5cd18a397811        gitlab/gitlab-ce       "/assets/wrapper"        2 days ago          Up 2 days (healthy)   0.0.0.0:80->80/tcp, 0.0.0.0:4567->4567/tcp, 0.0.0.0:32769->22/tcp, 0.0.0.0:32768->443/tcp   gitlab_gitlab_1
182c5937b931        gitlab/gitlab-runner   "/usr/bin/dumb-init …"   2 days ago          Up 2 days
```

Please point your browser to [http://10.10.20.20](http://10.10.20.20/), the IP address of your _devbox_ (default port 80), and check that you can access the HTTP interface for your new GitLab service.

#### <a name='CICDsetup'></a>CICD setup

Now that GitLab is ready, go back to your terminal and let's run the script to setup the complete CICD environment.

```
[developer@devbox gitlab]$cd ../cicd-3tier
[developer@devbox cicd-3tier]$./setup.sh
```

In this case `setup.sh` will perform the following actions:

1. Launch the required VIRL simulations for two different environments: test and production
2. Start NSO
3. Import test and production network configurations from VIRL to NSO
4. Synchronize devices configuration from NSO into VIRL simulations
5. Create a new repo in GitLab and initialize it locally in your _devbox_
6. Create locally in _devbox_ the _prod_ and _test_ git branches and push them to GitLab
7. List the status of VIRL nodes in _production_ and _test_

This complete process will take like 10 minutes, so time for your fix.

<p align="center"> 
<img src="imgs/10pendulum3.gif">
</p>

__Congrats, everything is now installed and ready!__

#### <a name='VIRLverifications'></a>VIRL verifications

Now you have two complete simulated environments running in your VIRL server: one for testing, and one replicating what would be a production physical network. Real world scenarios might be diverse: some customers may have a physical network in production, but only a simulated one for testing. Others might also have a real network for testing. Maybe even an additional one for staging before going to production. No matter how, the same principles apply to what we will be demonstrating. In our case the sandbox includes a couple of virtual environments, like the one depicted below, and implemented with VIRL for convenience.

<p align="center"> 
<img src="imgs/11topology.png">
</p>

As you can see each environment includes a standard 3-tier architecture, with 2x IOS-XE routers in the Core, 2x NX-OS switches in Distribution, and another 2x NX-OS switches in the Access layer.

You may find VIRL definitions for these two environments at the following locations in your _devbox_:
* `/home/developer/sbx_multi_ios/cicd-3tier/virl/test/topology.virl`
* `/home/developer/sbx_multi_ios/cicd-3tier/virl/prod/topology.virl`

Please make sure all your simulated routers are readily available (_REACHABLE_ status) in both prod and test. If they are not, your demonstration will fail in different stages.

```
[developer@devbox test]$pwd
/home/developer/sbx_multi_ios/cicd-3tier/virl/test
[developer@devbox test]$virl nodes
Here is a list of all the running nodes
╒══════════════╤═════════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node         │ Type        │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞══════════════╪═════════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ test-dist1   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.213        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-access1 │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.215        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-dist2   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.214        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-core2   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.212        │ N/A                │
├──────────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ test-core1   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.211        │ N/A                │
╘══════════════╧═════════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛
[developer@devbox test]$cd ../prod
[developer@devbox prod]$virl nodes
Here is a list of all the running nodes
╒═════════╤═════════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node    │ Type        │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞═════════╪═════════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ core2   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.222        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ core1   │ CSR1000v    │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.221        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ access1 │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.225        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ dist2   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.224        │ N/A                │
├─────────┼─────────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ dist1   │ NX-OSv 9000 │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.223        │ N/A                │
╘═════════╧═════════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛
```

*If* any of the nodes stay in _UNREACHABLE_ status please try the following:

1. Go into the environment directory (prod or test) and restart the node.

    ```
    [developer@devbox cicd-3tier]$cd virl/test
    [developer@devbox test]$virl stop test-dist2
    [developer@devbox test]$virl start test-dist2
    ```

2. Connect into that specific node (with `virl ssh` or `virl console`) and reboot it (password is `cisco`).

    ```
    [developer@devbox test]$virl ssh core1
    Attemping ssh connectionto core1 at 172.16.30.221
    Warning: Permanently added '172.16.30.221' (RSA) to the list of known hosts.
    cisco@172.16.30.221's password:


    core1#reload
    ```

3. If it still refuses to cooperate, stop the whole environment...

    ```
    [developer@devbox test]$cd /home/developer/sbx_multi_ios/cicd-3tier
    [developer@devbox cicd-3tier]$./cleanup.sh
    ```

    ... and then restart it.

    ```
    [developer@devbox cicd-3tier]$./setup.sh
    ```

Now that both of your VIRL environments are ready, let's setup your local environment.

#### <a name='Localenvironmentsetupoptional'></a>Local environment setup (optional)

To experience and demonstrate the full NetDevOps configuration pipeline, you may want to setup a local development environment where you can test proposed configuration changes before committing and pushing them to GitLab for the full test builds to occur. This is a completely optional step you might want to skip if you are not interested in testing locally.

To complete this step you will need to have a few local pre-requisites setup on your local workstation.

**1. Common software**: install Java JDK, python and sed (`brew install gnu-sed` in OSX)

**2. [Network Service Orchestrator](https://developer.cisco.com/site/nso/)**: in order to test the configuration pipeline locally, you'll need to have a local install of NSO on your workstation. Furthermore, you will need to have the same versions of NSO and NEDs (network element drivers) installed as the _DevBox_ within the Sandbox. Using different versions _may_ work, but for best experience matching the versions exactly is recommended.

* Network Service Orchestrator 4.5.3
* Cisco IOS NED 5.8
* Cisco IOS XE NED 6.2.10
* Cisco NX-OS NED 4.5.10

Once downloaded, you would install NSO in OSX like this:

```
$ sh nso-4.5.3.darwin.x86_64.signed.bin
$ sh nso-4.5.3.darwin.x86_64.installer.bin ~/ncs-4.5.3 --local-install
```

You may download the required NEDs from your sandbox _devbox_ via SCP to your own workstation.

```
$ scp developer@10.10.20.20:/usr/src/nso/ncs-4.5.3-cisco-ios-5.8.signed.bin .
$ scp developer@10.10.20.20:/usr/src/nso/ncs-4.5-cisco-nx-4.5.10.signed.bin .
$ scp developer@10.10.20.20:/usr/src/nso/ncs-4.5-cisco-iosxr-6.2.10.signed.bin .
```

Install those NEDs, by running the following two commands for each downloaded binary...

```
$ sh <bin_file>
$ tar -xzvf <gz_file>
````

... and then move each uncompressed folder into `~/dev/ncs-4.5.3/packages/neds`, replacing the existing ones.

Check all required NEDs are installed.

```
$ ls $NCS_DIR/packages/neds/
```

Once you have installed these versions, you'll need to `source` the `ncsrc` file for this version before beginning the local development process.

```
$ source ~/ncs-4.5.3/ncsrc
```

_Don't forget to include this command in your startup shell (eg .zshrc)_

Now you can test your local NSO installation.

First, setup the required structure and environment in your preferred directory.

```
$ ncs-setup --dest ~/ncs-run
```

Then start the NCS daemon.

```
$ cd ~/ncs-run
$ ncs
```

Check if NCS started correctly.

```
$ ncs --status
```

Start the CLI to connect to NCS...

```
$ ncs_cli -u admin
```

... or connect via SSH (default password is `admin`).

```
$ ssh -l admin -p 2024 localhost
```

Point your browser to [http://localhost:8080/](http://localhost:8080/) (credentials arer `admin`/`admin`).

If everything works correctly you may now stop the NCS daemon.

```
$ ncs --stop
```

_Congrats, your NSO local installation is complete!_

**3. Python + Ansible** 

The network-as-code mechanism in this demonstration leverages both Ansible and NSO, with Ansible orchestrating the execution and configuration used by NSO to deploy to the network. In order to test locally, you'll need to have a Python environment (_virtual environment_ is recommended) that meets these requirements.

* [Python](https://www.python.org/downloads/) 3.6.5 or higher
* Ansible 2.6.3 or higher

Once you install them, and with your virtual environment active, install the requirements.

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

__All pre-requisites are now complete!__

Let's now dig into setting up the local environment in your workstation.

1. Clone a copy of the repository from GitLab to your local workstation. Use this command to ensure the demo credentials are embedded in the git configuration.

    ```
    $ git clone http://developer:C1sco12345@10.10.20.20/developer/cicd-3tier
    $ cd cicd-3tier
    ```

2. To simplify the setup and management of the local environment, a `Makefile` is included in the repository. Simply run `make dev` to do the following (to see the exact commands being executed for each of these steps, just take a look at the content of your `Makefile`):

    a. Use NCS netsim to start a local simulation of the network including the core, distribution, and access devices

    b. Setup a local NCS project directory within the repo, start NCS and import in the netsim simulation
    
    c. Synchronize netsim and NCS
    
    d. Deploy the current network-as-code configuration to NCS and the network devices, using Ansible

    ```
    $ make dev
    ```

    Let's examine what is happening here, by going through the content of the `Makefile`.

    ```
    $ cat Makefile
    ```

    You will see the first line defines the different steps that are part of the `dev` directive.

    ```
    dev: netsim nso sync-from dev-deploy
    ```

    These steps are defined later in the same `Makefile`. You may also run them independently if you want to execute only that special step (eg. `make netsim`).

    __a. Start netsim__

    ```
    netsim:
        -ncs-netsim --dir netsim create-device cisco-ios core1
        -ncs-netsim --dir netsim add-device cisco-ios core2
        -ncs-netsim --dir netsim add-device cisco-nx dist1
        -ncs-netsim --dir netsim add-device cisco-nx dist2
        -ncs-netsim --dir netsim add-device cisco-nx access1
        -ncs-netsim start
    ```

    These `ncs-netsim` commands create netsim devices in the `netsim` directory, with the specified NEDs (ie. `cisco-ios` or `cisco-nx`) and a certain name (ie. `coreX`, `distX`, `accessX`). Then the last step starts them locally in your workstation. Netsim devices are a quick and easy way to test configuration changes locally, with no risk.

    You may check your netsim devices started correctly and their ports configuration, with:

    ```
    $ ncs-netsim is-alive
    $ ncs-netsim list
    ```

    You can also connect to your netsim devices CLI, and check with `show run` that nothing is configured yet. For example, to connect to `core1`:

    ```
    $ ncs-netsim cli-c core1
    ```

    __b. Start NSO__

    ```
    nso:
        -ncs-setup --dest . --package cisco-ios --package cisco-nx
        -ncs
    ```

    This `nso` directive prepares the current directory (`--dest .`) for a local NCS project, with the NEDs it will use (ie. `cisco-ios`and `cisco-nx`), and then it starts NCS.

    _It is important to note that NCS will automatically detect and add existing local netsim devices._

    You may login into NSO CLI and check the discovered devices (your netsim devices in this case) with:

    ```
    $ ncs_cli -C -u admin

    admin connected from 127.0.0.1 using console on JGOMEZ2-M-D2KW
    admin@ncs# show devices brief
    NAME     ADDRESS    DESCRIPTION  NED ID
    ------------------------------------------
    access1  127.0.0.1  -            cisco-nx
    core1    127.0.0.1  -            cisco-ios
    core2    127.0.0.1  -            cisco-ios
    dist1    127.0.0.1  -            cisco-nx
    dist2    127.0.0.1  -            cisco-nx
    admin@ncs#
    ```

    You may also see the devices configuration stored in NSO (not configured yet). For example, for `core1`:

    ```
    admin@ncs# show running-config devices device core1
    ```

    __c. Synchronize netsim and NCS__

    ```
    sync-from:
        -curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from
    ```

    This step will synchronize initial configurations _from_ netsim devices _into_ NCS. Check the configuration of your devices in NCS again, and you will see they include interfaces definitions now (eg. Loopback, Eth, FE).

    __d. Apply configurations__

    ```
    dev-deploy:
        -ansible-playbook --syntax-check -i inventory/dev.yaml site.yaml
        -ansible-playbook -i inventory/dev.yaml site.yaml
    ```

    This last directive uses Ansible to first check the syntax ([linting](https://en.wikipedia.org/wiki/Lint_(software))), and then executes the `site.yaml` playbook on the list of devices defined in the `dev.yaml` inventory file.

    The inventory file (`dev.yaml`) lists the devices that will be configured by the playbook, with their hostnames, credentials (if necessary) and management IP addresses:

    * NSO
    * One access switch
    * Two core routers
    * Two distribution switches

    <p align="center"> 
    <img src="imgs/12nsoarch.png">
    </p>

    If you review the playbook itself (`site.yaml`) you will find it executes the following steps:

    1. Synchronize _old_ configurations from NSO to devices
    2. Push _new_ configurations to NSO
    3. Synchronize _new_ configurations from NSO to devices

    But specifically for the second step you might be wondering _where are those new configurations?_

    Take a look at this extract from `site.yaml`, describing that second step:

    ```
    - name: Push new configurations to NSO
    hosts: all
    connection: local
    gather_facts: no

    tasks:
        - name: Device configuration
        nso_config:
            url: "{{ nso.url }}"
            username: "{{ nso.username }}"
            password: "{{ nso.password }}"
            data:
            tailf-ncs:devices:
                device:
                - name: "{{ nso_device_name }}"
                tailf-ncs:config:
                    "{{ config }}"
    ```

    That _tasks_ description uses the [`nso_config` module](https://docs.ansible.com/ansible/latest/modules/nso_config_module.html), and provides the required NCS URL, username and password, as parameters defined in the inventory file mentioned before.

    The `data` section is the one that describes what configuration to apply, and there you may find you need to provide the _device_name_ and _config_. Device names come again from the inventory file. BUT configurations are stored in the `host_vars` directory, where Ansible looks for variables as required. That directory stores individual YAML files, one per device, with the required configuration to apply to NCS devices.

    These configuration files in the `host_vars` directory will be important for us throughout the demo, as they store the configuration we want to apply, and therefore we will use them to apply changes to our network.

    After `dev_deploy` is completed you will see configurations correctly applied (and synchronized) to your netsim devices and NCS ones. You may check it worked fine with the same commands described in previous steps. For example, for `core1`:

    ```
    $ ncs-netsim cli-c core1

    admin connected from 127.0.0.1 using console on JGOMEZ2-M-D2KW
    core1# show running-config
    ```

    And...

    ```
    $ ncs_cli -C -u admin

    admin connected from 127.0.0.1 using console on JGOMEZ2-M-D2KW
    admin@ncs# show running-config devices device core1
    ```

    _(Note: after you complete the rest of this demo, when you don't need the local environment anymore, you can easily delete everything by running `make clean`. It will shutdown netsim devices, NSO, and delete any related remnants.)_

#### <a name='Demooverview'></a>Demo overview

Our demonstration will include the following architecture and elements, to show how a completely automated CICD pipeline could be applied to a network configuration environment across a complete network, including test and production environments.

<p align="center"> 
<img src="imgs/20pipeline.png">
</p>

The flow will be as follows: our network operator will interact with GitLab to perform any configuration changes. Ansible and NSO will deploy those changes into a virtual _test_ environment (with VIRL), and run automated tests (with pyATS) to verify the expected results after the change. If everything goes well, then our VCS will run the same process in the _production_ environment to implement those changes in the real network.

Integrating that environment with the local setup we built in the previous section, results in a comprehensive architecture where the local environment uses the same tools (NSO & Ansible) as the remote one. Locally it will only do the syntax checking, and once configurations are pushed to the remote GitLab, the same set of tools will also deploy and test the proposed changes, first into a _test_ environment and then into _production_.

<p align="center"> 
<img src="imgs/33cicd_arch.png">
</p>

Your GitLab Version Control Server (VCS) is ready. Please find the new infrastructure-as-code repository by pointing your browser to [http://10.10.20.20/developer/cicd-3tier](http://10.10.20.20/developer/cicd-3tier), and login with `developer`/`C1sco12345`. Leave that window open, as we will use it to run the demo.

<p align="center"> 
<img src="imgs/21gitlab_project.png">
</p>

The repository (or _repo_) stores all required files and configurations to work with during the demo. Some key elements are the following ones:

* `.gitlab-ci.yml` is the pipeline definition, including all different steps to follow in the automation process
* `virl` is a folder used by VIRL to define the emulated architectures (_test_ and _prod_)
* `tests` is a folder used by pyATS for automated testing
* `group_vars`, `host_vars` and `inventory` are folders used by Ansible to automate configurations deployment

__If__ you did not follow the optional local setup process, please clone a copy of the repository from GitLab to your local workstation (if you already did it in the previous section, please skip this step). Use this command to ensure the demo credentials are embedded in the git configuration.

```
$ git clone http://developer:C1sco12345@10.10.20.20/developer/cicd-3tier
$ cd cicd-3tier
```

You will need to edit some of the files in this local repo, so please choose your favorite editor / IDE ([integrated development environment](https://en.wikipedia.org/wiki/Integrated_development_environment)). One possible option is [Visual Studio Code](https://code.visualstudio.com/), but you could also just defer to using something simpler like `vi` or any other text editor.

First of all, please take a look at the `.gitlab-ci.yml` pipeline file definition.

```
$ cat .gitlab-ci.yml
```

You will see our pipeline includes the following steps:

1. Use Ansible to validate configurations that need to be applied to NSO and network devices are syntactically correct ([linting](https://en.wikipedia.org/wiki/Lint_(software))), for the three environments: _dev_ (local), _test_ and _production_.
2. Deploy those configurations to the _test_ environment.
3. Run automated testing in the _test_ environment to make sure the resulting network state is the expected one.
4. Deploy those configurations to the _production_ environment. In this case you will see it specifies `when: manual`, meaning we would like to explicitly initiate the deployment process to _production_. `allow-failure: false` means that in case of failure when deploying in _production_ the system should automatically roll-back to the previous state.
5. Run automated testing in the _production_ environment to make sure the resulting network state is the expected one. 

_Important note: for our demonstration we will use two simulated environments: test and production. It is more convenient for us to use a simulated environment for production, but in a real-world scenario the production environment would be built by real equipment from the production network._

<p align="center"> 
<img src="https://media.giphy.com/media/G0GfSkTMYKNWw/giphy.gif">
</p>

Let's take a look at our network configurations.

```
$ cd host_vars
$ ls
access1.yaml core1.yaml   core2.yaml   dist1.yaml   dist2.yaml
```

As you can see there is one YAML file per device in our network. Those files will be the ones you need to modify to perform changes in your network.

In a real-world scenario each network developer would have cloned this repository in their local machine, and work in their own local copy, via a specific branch. For our demo we will be one of those network developers, and propose changes from our local git repo.

For example, let's say we would like to change the OSPF router-id of our core1 router, from `.1` to `.101`. We would have to edit `core1.yaml`, look for the relevant configuration line...

```
ospf:
    - id: 1
      network:
      - area: 0
        ip: 172.16.0.0
        mask: 0.0.0.3
      - area: 0
        ip: 172.16.0.4
        mask: 0.0.0.3
      - area: 0
        ip: 172.16.0.16
        mask: 0.0.0.3
      - area: 0
        ip: 192.168.1.1
        mask: 0.0.0.0
      router-id: 192.168.1.1
```

... and change that last line to the desired value.

```
      router-id: 192.168.1.101
```

Save the file.

Right now you have _only_ modified a local text file in your workstation. And _git_ knows about it.

```
$ git status
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   core1.yaml

no changes added to commit (use "git add" and/or "git commit -a")
```

As long as we are happy with this change, we need to add the modified file to our next _git_ commit.

```
$ git add core1.yaml
$ git commit -am "Update OSPF router-id from .1 to .101"
[master 0b24c9b] Update OSPF router-id from .1 to .101
 1 file changed, 1 insertion(+), 1 deletion(-)
```

Now is the time to send our configuration change to the remote repo in the VCS GitLab server.

```
$ git push
warning: redirecting to http://10.10.20.20/developer/cicd-3tier.git/
Counting objects: 4, done.
Delta compression using up to 12 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 389 bytes | 389.00 KiB/s, done.
Total 4 (delta 3), reused 0 (delta 0)
To http://10.10.20.20/developer/cicd-3tier
   00f2b65..1b70da9  test -> test
```

Go back to the browser window that pointed to your GitLab repo at [http://10.10.20.20/developer/cicd-3tier](http://10.10.20.20/developer/cicd-3tier), and you will see the update there.

<p align="center"> 
<img src="imgs/22gitlab_pipeline_start.png">
</p>

Pushing your proposed change in the new `core1.yaml` file will automatically start the pipeline defined in the `.gitlab-ci.yml` file. It is applied on the _test_ network, and you may check its execution in real-time by clicking on the _CI / CD_ section in the left bar. In this example we would be running pipeline #3.

<p align="center"> 
<img src="imgs/23gitlab_pipeline_run.png">
</p>

As you can see the pipeline includes 3 different _stages_: _validate_, _deploy_to_test_ and _verify_deploy_to_test_.

These are coming from the pipeline definition in your `.gitlab-ci.yml` file.

Clicking on each one of these stages will show you the specific steps followed in there:

1. _validate_

<p align="center"> 
<img src="imgs/24gitlab_pipeline_validate.png">
</p>

This stage starts a container running Ansible and do the syntax checking of proposed configurations, including changes, in all 3 environments: _dev_ (local), _test_ and _prod_.

2. _deploy_to_test_

<p align="center"> 
<img src="imgs/25gitlab_pipeline_deploy.png">
</p>

Second stage starts a container running Ansible to sync existing configs from NSO to devices, then apply configuration changes to NSO, and finally sync again configs from NSO to devices.

3. _verify_deploy_to_test_

<p align="center"> 
<img src="imgs/26gitlab_pipeline_test.png">
</p>

The final stage starts a container running a pyATS image and run automated tests based on the content of `tests/validation_tasks.robot` and `tests/test_testbed.yml`. The defined set of tests includes not only reachability, but also number of expected OSPF neighbors and interfaces in each network device after the applied changes. 

The whole process will take like 5 minutes, until you can see the 3 stages completed successfully in the _test_ environment.

<p align="center"> 
<img src="imgs/27gitlab_pipeline_complete.png">
</p>

At that point your proposed network configuration change has been completely validated in a VIRL-simulated _test_ environment, and you are now good to propose it to be applied in the real _production_ network.

You can do that by _requesting_ to merge the content of the git _test_ branch into the git _production_ branch.

<p align="center"> 
<img src="imgs/28merge1.gif">
</p>

<p align="center"> 
<img src="imgs/29merge2.gif">
</p>

If you go back to the pipeline section you will see there is a new pipeline there, #4. It includes the same steps as the previous one, but the main difference is that this pipeline is being applied to the _production_ network.

<p align="center"> 
<img src="imgs/30gitlab_pipeline_prod_blocked.png">
</p>

As you can see the _production_ pipeline has the same 3 stages as the one we applied previously in the _test_ environment. However when running it, the pipeline appears as _blocked_ before running the _deploy_to_prod_ stage. The reason is we configured `when: manual` in the `.gitlab-ci.yml` pipeline definition file, so that we _had_ to manually confirm we want to actually initiate the deployment in the production network. This is a configuration decision, and maybe useful if you would like to perform the actual change during a maintenance window.

In order to move forward with the pipeline we need to confirm it manually by pressing the _play_ button.

<p align="center"> 
<img src="imgs/31gitlab_pipeline_prod_confirm.png">
</p>

It will automatically start deploying our configuration changes into the _production_ network. If everything goes well, it will successfully complete this stage and move to the next one, to test the results after changes are implemented. 

After 5 minutes, by the end of this process you should see the complete pipeline has been successfully executed, and your proposed changes have been tested and finally applied to the _production_ network.

<p align="center"> 
<img src="imgs/32gitlab_pipeline_prod_complete.png">
</p>

__CONGRATULATIONS! You have completed your first NetDevOps demo on how to fully automate and test network configuration changes all the way to production!__ 

<p align="center"> 
<img src="imgs/100congrats.gif">
</p>

#### <a name='Summary-1'></a>Summary

In this NetDevOps demo you have seen a modern approach into version-controlled automated network configuration and testing. The scenario describes how multiple network operators would be able to propose configuration changes, in the same way developers do it for code: using _git_ branches. A standard version control server provides multiple benefits, like automated pipelines, version control and tracking, rollback cababilities, etc. During the demo you have also experienced the benefits of being able to locally verify syntax for proposed changes before submitting them. Also how a simulated environment helps verifying proposed changes are correct, before applying them into the production network. Finally, the set of automated tests helps making sure proposed changes have not had unexpected results on critical business-relevant functionality. This way you have experienced end-to-end automation and testing in a scalable and error-free approach.

<p align="center"> 
<img src="imgs/34netdevops_overview.png">
</p>

### <a name='NetDevOpsDemo2-VPNHeadEndManagementPlatformHEMP'></a>NetDevOps Demo 2 - VPN Head End Management Platform (HEMP)

Managing connections from [extranet](https://en.wikipedia.org/wiki/Extranet) environments usually involves a great amount of workload, especially around VPN configurations at central hub points. One way of implementing this type of environments is pre-configuring VPN endpoints at remote locations, and then completing the required configuration from the central head-end point as connectivity is required. This configuration will explicitly define the authorized end-points and type of traffic that can traverse the connection.

Once connectivity to a certain remote location is not required anymore, you will have to remove the associated relevant configuration from the central head-end, disabling that specific VPN and hence discontinuing connectivity.

As you might guess, scaling this type of environment would really benefit from _automation_. The more remote locations from different 3rd-party entities (ie. partners, vendors), the longer the process to configure VPNs, ACLs with type of traffic and authorized end-points, etc. Implementing these long VPN configurations via CLI is of course a _prone-to-error_ process due to the required human interaction, so automation will also take care of this challenge and provide the required consistency along the network.

<p align="center"> 
<img src="imgs/54carrey.gif">
</p>

This demonstration will focus on how to automate the lifecycle of extranet VPN connections, from setting them up to checking everything is correct, providing related metrics, and tearing them down once they are not required anymore. It also includes a simple graphical user interface (GUI) that uses APIs to demonstrate how easy it could be to manage those VPN connections for users without the required permissions to connect via CLI to network devices, or even the knowledge to configure them.

#### <a name='Topology'></a>Topology

Our demo setup will include 1 central hub location with a _headend_ router that will concentrate VPN connections from 4 remote _partner_ locations.

We will also have some switches acting as _hosts_ exchanging traffic, and another router simulating _internet_, providing connectivity between the headend and partner locations.

All devices will be simulated using VIRL as per the diagram below.

<p align="center"> 
<img src="imgs/51hemptopo.png">
</p>

#### <a name='Buildingblocks'></a>Building blocks

These are the components we will use to build the demo:

* [Cisco Network Services Orchestrator](https://developer.cisco.com/site/nso/): formerly Tail-f, it provides end-to-end automation to design and deliver services much faster
* [VIRL](http://virl.cisco.com/): network modelling and simulation environment
* [Ansible](https://www.ansible.com/): simple automation

The provided GUI portal to manage HEMP uses the following technologies:

* Python, Flask, and JavaScript for the primary web interface
* Telegraf, InfluxDB, and Grafana for visualizing operational metrics collected via SNMP

For ease of deployment and portability, all of the above components are run as a [docker compose stack](https://github.com/DevNetSandbox/sbx_multi_ios/blob/add-hemp-demo/hemp/docker-compose.yml) which can be executed directly on your sandbox _devbox_.

#### <a name='Environmentsetup'></a>Environment setup

Once you are connected via VPN to your reserved sandbox, please open a terminal window (ie. [putty](https://www.putty.org/) on Windows or `terminal` on OSX) and `ssh` to your _devbox_ with the following credentials: `developer`/`C1sco12345`

```
$ ssh developer@10.10.20.20
```

Once in, clone the repository that includes all required files to build the setup into your _devbox_.

```
[developer@devbox ~]$git clone --recurse-submodules https://github.com/DevNetSandbox/sbx_multi_ios.git
```

With that, your sandbox _devbox_ includes now all required info to start building the environment.

Go into the `hemp` directory and run the `setup.sh` script to set the complete environment up.

```
[developer@devbox ~]$cd sbx_multi_ios/hemp
[developer@devbox hemp]$./setup.sh
```

`setup.sh` will perform the following steps in the sandbox _devbox_:

1. Install required software tools and dependencies in a python virtual environment
2. Launch VIRL simulations for the whole network, including 4 remote _partner_ locations and 1 central hub _headend_
3. Setup and start NSO
4. Add all VIRL network devices into NSO
5. Synchronize all existing configurations from network devices to NSO
6. Display the status for VIRL network devices 
7. Start a HEMP management GUI, implemented with containers
8. Use Ansible to pre-configure the headend and activate 2 out of the 4 remote locations VPNs

<p align="center"> 
<img src="imgs/53hempworkflow.png">
</p>

The process will take approximately 15 minutes, so check this out in the meanwhile.

<p align="center"> 
<img src="imgs/50pendulum.gif">
</p>

#### <a name='Demooverview-1'></a>Demo overview

Your demo architecture is now set up, and includes the following main components: 

* 1 central _headend_ router where _partner_ extranet VPN connections from remote devices are terminated
* 4 remote _partner_ routers (_partner1_, _partner2_, _partner3_, _partner4_) that represent the _unmanaged_ side of extranet/partner VPN connections

Simulated devices connected to both, the remote _partner_ routers and the _headend_ one, are configured with IP SLA probes, to send interesting traffic through the VPNs and keep them active.

Every remote _partner_ router (1 to 4) is completely configured to establish their respective VPNs. Having connectivity for each one of them will depend exclusively on having the proper configuration applied on the _headend_ router side.

On the _headend_ router we have already provided the required configuration to setup VPN connections towards _partner1_ and _partner2_ remote devices. The `partners` directory includes YAML files with all required parameters to configure the _headend_ router and complete the VPN connections _just_ for _partner1_ and _partner2_ remote locations (not 3 and 4).

This configuration has been provided using Ansible and associated NSO modules during step 8 of the _setup_ phase. That step is the one that runs an Ansible playbook, described in the `site.yaml` file. If you go through its content, you will see that first it synchronizes the configuration from NSO to the remote devices for consistency (in case there might have been any changes configured directly on the devices they will be overwritten by this step). Then the playbook will load _partner1_ and _partner2_ YAML files into variables, and push those those to NSO as new headend router configuration to activate those specific VPNs. Finally the playbook with instruct NSO to sync that new configuration from NSO to the _headend_ router.

However, _partner3_ and _partner4_ VPNs are pre-configured __only__ on the partner/remote side, and will need you to provide additional configuration on the _headend_ to complete those VPNs setup.

Instead of configuring it manually, or via YAML files and Ansible, for this demo you will be able to define the required configuration in the _headend_ via a GUI management portal. It will allow you to provide the required parameters, and the GUI will translate them into the required information to send towards NSO north-bound APIs.

<p align="center"> 
<img src="imgs/52hempelements.png">
</p>

This API-based automation solution will enable you to easily apply or remove the required configuration in the _headend_ router, without having to connect to the device via CLI and type _myriads_ of commands.

At this point you might be wondering why NSO is part of the architecture, or if you could use Ansible to directly configure your network devices. One of the multiple benefits that NSO provides is that, although in this demo we are only using IOS XE devices, it would be easy to support a _mixed_ environment with other types of devices / CLIs (ie. IOS XR, ASA firewall, other vendors...) _without doing any modifications in the management GUI_. Please remember the GUI uses NSO north-bound APIs, so it does not depend on the type of underlying infrastructure devices. NSO plays a key role by performing that translation from API requests to the information and format those devices require and support.

You may access the HEMP GUI portal by pointing your browser to http://10.10.20.20:5001

<p align="center"> 
<img src="imgs/55hemp1.png">
</p>

Please click on _Configure VPN connections_ and there you will see the ones already configured on the _headend_ router: _partner1_ and _partner2_. 

<p align="center"> 
<img src="imgs/56hemp2.png">
</p>

You may now click on one of them, for example _partner1_, and the GUI will display its configuration and metrics. The system will also allow you to perform some actions on that specific VPN:

* _Check Sync_: this will compare the configuration in NSO vs the one in the _headend_ router
* _Reactivate Re-Deploy_: ask NSO to sync configuration again from NSO to the _headend_ router
* _Undeploy_: remove configuration from the _headend_ router, while conveniently keeping it in NSO in case you need to redeploy it later

Now let's go back to _Configure VPN connections_ and click on _Add VPN_ to start the "VPN Setup Wizard". This will allow you to provide the required information to establish the VPN connection from the _headend_ router to _partner3_. 

You may find below the required configuration that will be applied in the _headend_ router, so that _partner3_ VPN connection is established:

```
partner3:
  - partner_name: partner3
    device:
      - headend
    sequence: 103
    peer_ip: 172.16.252.3
    isakmp_algo: 3des
    isakmp_group: 2
    pre_shared_key: cisco
    transform_encryption: esp-3des
    transform_auth: esp-md5-hmac
    acl_number: "101"
    acl_rule: "permit ip 192.168.0.0 0.0.0.255 192.168.3.0 0.0.0.255"
```

This is the sequence of steps you will need to follow in the GUI:

<p align="center"> 
<img src="imgs/57hemp3.png">
</p>

<p align="center"> 
<img src="imgs/58hemp4.png">
</p>

<p align="center"> 
<img src="imgs/59hemp5.png">
</p>

<p align="center"> 
<img src="imgs/60hemp6.png">
</p>

<p align="center"> 
<img src="imgs/61hemp7.png">
</p>

<p align="center"> 
<img src="imgs/62hemp8.png">
</p>

Once you are done with _partner3_ please repeat the process for the _partner4_ VPN connection, using the parameters below:

```
partner4:
  - partner_name: partner4
    device:
      - headend
    sequence: 104
    peer_ip: 172.16.252.4
    isakmp_algo: 3des
    isakmp_group: 2
    pre_shared_key: cisco
    transform_encryption: esp-3des
    transform_auth: esp-md5-hmac
    acl_number: "104"
    acl_rule: "permit ip 192.168.0.0 0.0.0.255 192.168.4.0 0.0.0.255"
```

By the end of the process you should have something like this in the _Configure VPN connections_ section:

<p align="center"> 
<img src="imgs/63hemp9.png">
</p>

You may now click on _Monitor VPN Connections_ and the GUI will load a Grafana dashboard. Please login there with `admin/admin`, and change the password. If it does not work correctly (error message _Dashboard not found_) you may still access the Grafana dashboard by pointing your browser directly to http://10.10.20.20:3000

Selecting the _Tunnel Detail_ dashboard will show you information about each specific tunnel, just by choosing the peer IP address:

<p align="center"> 
<img src="imgs/64grafana1.png">
</p>

The _Extranet Monitoring_ dashboard will show you all information about how the _headend_ router is doing:

<p align="center"> 
<img src="imgs/65grafana2.png">
</p>

__CONGRATULATIONS! You have now completed your second NetDevOps demo on how to leverage APIs to automate Extranet VPNs management!__ 

<p align="center"> 
<img src="imgs/101congrats.gif">
</p>

#### <a name='Summary-1'></a>Summary

This automation demo shows how you can leverage APIs to easily provision and monitor Extranet VPNs from a simple custom GUI. With this kind of approach network operators would not need to:

* Understand network architecture details
* Remotely connect to devices
* Be experts on each underlying device CLI
* Configure those devices via a _myriad_ CLI commands

> Note: it is important to remark that this automation demo is based on NSO and its capability to extend existing functionalities via service models. The primary service model for NSO can be found in the `./nso/packages/vpn` directory. Service models/packages are the primary way that NSO functionality is extended. A service model is comprised of a YANG file, a set of templates, and optionally some python or java logic.

### <a name='NetDevOpsDemo3-WorkingwithpyATSandGenie'></a>NetDevOps Demo 3 - Working with pyATS and Genie

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

Your network devices are also objects in pyATS, so you can perform operations on them using _methods_, like the following:

* connect()
* ping(destination)
* execute('show version')
* configure('no ip domain lookup')

The output from these commands will be parsed into structured data, so your systems can easily extract business-relevant data from them.

0k, let's see it working.

The first thing you need to decide is _how_ you want to run pyATS: natively in your own system, or in a Docker container.

For the first option you should use a Python 3.X [virtual environment](https://virtualenv.pypa.io/en/latest/), so you don't clog your system, and then install the required tools (see this [doc](https://developer.cisco.com/docs/pyats/#!python-virtual-environment)). 

However it is easier to run it [in a Docker container](https://developer.cisco.com/docs/pyats/#!docker-container), as the available image includes all required software, libraries, dependencies and a ton of examples you can use to get started. So we will use containers for our demos.

<p align="center"> 
<img src="imgs/205ilovecontainers.jpg">
</p>

The sandbox you have reserved includes a _big_ [VIRL](http://virl.cisco.com/) server we will use to run some simulated devices for our demos. 

<p align="center"> 
<img src="imgs/204virllogo.png">
</p>

It also includes a _devbox_ with all required utilities pre-configured. At this point you could decide to use the _devbox_ included in your sandbox to execute the demos, or rather configure your own system so you can continue using it later. If you decide to use the sandbox _devbox_ you can connect to it by running: `ssh developer@10.10.20.20`, and use password `C1sco12345`.

In order to easily manage the VIRL server we will use a very handy utility called [virlutils](https://github.com/CiscoDevNet/virlutils). You will only need to install _virlutils_ if you decide to use your own local workstation for the demos (no need to do it if you will be using the sandbox _devbox_).

```
$ pip install virlutils
```

Once done, please create a VIRL init file (again, no need to do this step if you will be using the sandbox _devbox_)...

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

Now you should be able to search for [some example pre-defined simulated topologies](https://github.com/virlfiles)
 that could be useful for testing (you can find some more [here](https://github.com/VIRL-Open/sample-topologies)).

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

__With just a single command you have now a YAML file that defines your VIRL environment as a testbed to be used by pyATS straight away!__

<p align="center"> 
<img src="imgs/200wow.gif">
</p>

That pyATS testbed definition file will need some variables to define the _enable password_ and _login user/password_. The most convenient way to use them later is to have them stored in a file, so please go ahead and download it.

```
$ curl -L https://raw.githubusercontent.com/juliogomez/netdevops/master/pyats/env.list -o env.list
```

__We are now READY to start our demos!__

_Don't do it now_, but please note that by the end of our set of demos, when you are finally done with your simulation, you can easily tear it down with:

```
$ virl down
Removing ./.virl/default
Shutting Down Simulation netdevops_default_oAmstu.....
SUCCESS
```

#### <a name='Executeacommandonanetworkdevice'></a>Execute a command on a network device

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

Run the demo with an interactive container (`-it`) that will be automatically deleted after execution (`--rm`), and pass it a mapped volume from your workstation to the container (`-v $PWD:/pyats/demos/`). When the container starts it will automatically execute the specified python script.

```
$ docker run -it --rm \
  -v $PWD:/pyats/demos/ \
  --env-file env.list \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/1-pyats-intro.py
```

#### <a name='ConsolidateinfofromdeviceswithdifferentCLI'></a>Consolidate info from devices with different CLI

In this case you will use not only pyATS, but also Genie, to compile interface counters from multiple devices across the network and then check if there are any CRC errors in them. 

<p align="center"> 
<img src="imgs/207errors.gif">
</p>

The script will use the same function to compile CRC errors information from 2 devices with different CLI (ie. CSR1000v and Nexus switch), with the available Genie parsers providing independence from the underlying device type. Genie uses [models](https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/models) to determine the specific commands and format that need to be used for each feature in each platform/OS, and how to map the outcome to the specific fields in the resulting structured data.

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

Run the demo with an interactive container (`-it`) that will be automatically deleted after execution (`--rm`), and pass it a mapped volume from your workstation to the container (`-v $PWD:/pyats/demos/`). When the container starts it will automatically execute the specified python script.

```
$ docker run -it --rm \
  -v $PWD:/pyats/demos/ \
  --env-file env.list \
  ciscotestautomation/pyats:latest \
  python3 /pyats/demos/2-genie-intro.py
```

#### <a name='DevelopyourowntestswithinteractivepyATS'></a>Develop your own tests with interactive pyATS

Now that you have seen a couple of simple examples of what can be done with pyATS and Genie, you might want to start developing your own tests. But instead of iterating through the process of "writing a complete script, trying to run it, failing and rewriting", we would rather have a more _interactive_ way of developing tests. Something that allows us to check the results of each step during the test, and debug it by exploring the results at any point of the flow.

As you may have noticed pyATS feels really _pythonic_, so wouldn't it be great to have something similar
to the interactive Python shell? Something that would give us the option to execute individual steps interactively while developing our tests? Well, we got you covered!

[ipyATS](https://github.com/kecorbin/ipyats) is an iPython wrapper for pyATS and Genie, so that you can conveniently explore and develop your own tests in an interactive way.

For our demos we will start a pyATS container and ask it to start an interactive shell (_bash_) so we can install ipyATS in it.

```
$ docker run -it --rm \
  -v $PWD:/pyats/demos/ \
  --env-file env.list \
  ciscotestautomation/pyats:latest bash
```

You can easily install ipyATS in it with:

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

__Wow, that was easy! Think about the kind of processing and parsing you would have had to do in the past to go through the text output of all those commands. Now pyATS is compiling the information from all those commands and giving you a consolidated, structured view that you can easily work with.__

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

Now let's try a different task, and learn about _all-things_ BGP in the _csr_ device:

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

As long as for other routing protocols (not BGP) there might be several instances we receive a _list_, and we need to refer to its first entry, numbered 0:

```
In [15]: bgp_nx = bgps_nx[0]
```

We can also apply configurations, like this or a different one, to our device:

```
In [16]: bgp_nx.build_config()
```

Or remove all BGP configuration:

```
In [17]: bgp_nx.build_unconfig()
```

You can check it's all gone with the same command we used in the _genie.ops_ section:

```
In [18]: bgp = tasks.learn('bgp',nx)
In [19]: bgp
Out[19]: {}
```

And easily apply all BGP configuration back again:

```
In [20]: bgp_nx.build_config()
```

When you are done exploring ipyATS, you can exit with:

```
In [21]: exit()
root@2ad68679070c:/pyats# exit
```

__ipyATS makes it really easy for you to develop and debug your tests step-by-step, in the classic _pythonic_ way!__

#### <a name='WorkingwithTestCases'></a>Working with Test Cases

Now that you know how to run some basic tests with pyATS and Genie, it is time to explore how we could give it a proper structure to build a more complex test. That's what _Test Cases_ are all about: a framework that allows you to build _repeatable_ and _more sophisticated_ testing processes.

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

The sections are easy to understand:

* You can define a number of _tasks_ to run in your test case (in the example above we have just 1 task)
* Then you will have some _common setup_ to do, structured in subsections 
* After that, you would go into the real Test Case (_tc_), with 3 phases: preparation, execution and cleaning
* Finally, as a good citizen, you would need to _clean after yourself_, everything you set up during the _common setup_ phase

Let's see it working in your own setup. In this case we will use the _-alpine_ image because it has _vi_ already included in it, and you will need it to edit some files during this demo. We will ask our pyATS container to provide a shell (_ash_ for _-alpine_ image) so we can work with it interactively.

```
$ docker run -it --rm ciscotestautomation/pyats:latest-alpine ash
```

Once inside the container shell you have access to its directory structure and tools. Inside the `pyats` directory you will find multiple examples and templates to use with pyATS. To get started let's focus on a _basic_ one.

```
(pyats) /pyats # cd examples/basic
```

There you will find the `basic_example_script.py` python script file that defines a very simple _Test Case_. It includes quite some python code for all the sections mentioned before, but actually not doing much (in fact only logging)... so it is a good starting point as a template to develop your own test cases.

```
(pyats) /pyats/examples/basic# cat basic_example_script.py
```

This script will be executed from a _job_, defined in this file:

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

Save the file and try it.

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

__As you can see you don't need to be a Python expert to use the test cases framework. You have templates readily available for you, where you can insert the specific tests you would like to run and execute them straight away.__

Once you are done you can exit the container.

```
(pyats) /pyats/examples/basic# exit
```

#### <a name='Profilingyournetworkfortroubleshooting'></a>Profiling your network for troubleshooting

Now let's say you are responsible for a network and could use some help on how to be updated about possible issues happening in it. Wouldn't it be great to have a tool that helps you profile the network end-to-end and store that info as snapshots?

<p align="center"> 
<img src="imgs/209tellmehow.gif">
</p>

Let's focus, for example, on profiling everything related to BGP, OSPF, interfaces and the platforms in your network, and saving it to snapshot files. Ideally you would take a first snapshot of your network when everything is working _superb_.

_Genie_ can help you do it __with a simple command__, specifying what features you want to learn (`ospf interface bgp platform`), from what specific testbed (`--testbed-file default_testbed.yaml`), and the directory where you want to store the resulting files (`--output good`):

```
$ docker run -it --rm \ 
  -v $PWD:/pyats/demos/ \ 
  --env-file env.list \
  ciscotestautomation/pyats:latest-alpine ash
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

In the real world, soon you would be receiving calls from users: "Something is wrong... _terribly_ wrong", "I lost ALL connectivity", "My database stopped working!". So instead of starting to troubleshoot by _brute force_, how about asking Genie to determine what is the current new status of the network after the outage. And even better, _what changed exactly_ since the last time you took the snapshot of the network in good state?

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

If you want learn more about how Genie network profiling can help you manage and debug issues in your network, please check [this fantastic lab](https://github.com/hpreston/netdevops_demos/blob/master/genie-cli-1/README.md) and also [this one](https://github.com/CiscoTestAutomation/CL-DevNet-2595). Both offer you the option to run them on _mocked devices_, so you don't actually need a reserved sandbox environment... how cool is that?

#### <a name='CheckallBGPneighborsareestablished'></a>Check all BGP neighbors are established

We will now explore another example that will help you check all BGP neighbors in your network are in the desired _established_ state. 

The test case structure includes the following sections:

* Common setup: connect to all devices included in your testbed.
* Test cases: learn about all BGP sessions in each device, check their status and build a table to represent that info. If there are neighbors _not in a established state_ the test will fail and signal this condition in an error message.

In order to run it first you will need to install `git` on your pyATS container, clone a repo with additional examples, install a tool to create nice text tables (_tabulate_), go into the directory and execute the _job_: 

```
$ docker run -it --rm -v $PWD:/pyats/demos/ ciscotestautomation/pyats:latest-alpine ash
(pyats) /pyats # apk add --no-cache git
(pyats) /pyats # git clone https://github.com/kecorbin/pyats-network-checks.git
(pyats) /pyats # pip3 install tabulate
(pyats) /pyats # cd pyats-network-checks/bgp_adjacencies
(pyats) /pyats/pyats-network-checks/bgp_adjacencies # pyats run job BGP_check_job.py --testbed_file /pyats/demos/default_testbed.yaml
```

As a result you will find the following table in your logs, displaying all BGP neighbors in all your devices, and their current status:

```
2019-04-05T18:10:41: %SCRIPT-INFO: | Device     | Peer     | State       | Pass/Fail   |
2019-04-05T18:10:41: %SCRIPT-INFO: |------------+----------+-------------+-------------|
2019-04-05T18:10:41: %SCRIPT-INFO: | csr1000v-1 | 10.2.2.2 | established | Passed      |
2019-04-05T18:10:41: %SCRIPT-INFO: | nx-osv-1   | 10.1.1.1 | established | Passed      |
```

__It was never this easy to make sure BGP neighbors across your network are properly _established_!__


# Author

* [Julio Gomez](https://www.linkedin.com/in/juliogomezsanchez/) - Initial work - [Blog](cs.co/julioblog)

# License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/juliogomez/netdevops/LICENSE.md) file for details

# Acknowledgements

Many thanks to the following programmability and NetDevOps gurus for their contributions and source materials that helped building this document:

* Kevin Corbin
* Hank Preston
* Chris Lunsford
* Jason Gooley
* Gabi Zapodeanu
* Jean-Benoit Aubin