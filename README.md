# viptela-tool


viptela-tool is a library designed to make the Viptela (Cisco SD-WAN) API more consumable. It is being developed based on the needs of the communications practice I work in, which focuses healivy on SD-WAN excellence.

The Viptela product itself is undergoing a high velocity of change, especially due to the Cisco acquisition, and the project will tend to lag behind the current state of the API. Some of the initial work was done against a multi-tenant instance of vManage, which is currently undergoing an overhaul and direction changes which we hear may be available in early 2019.

The initial focus of the tool is GET operations to provide insight into vManage and vEdge state. Going forward, PUT/POST functions will be added to assist with provisioning.

## Installation

I've been developing against Python 2.7.15

	pip install requests
	pip install tabulate

## Usage

	python vmanage.py sdwan.acme.com <user> <pass>

## Things to Know

* Call into the Provider by invoking with the IP of your multi-tenant vManage
* Call into a particular tenant by invoking with it's unique URL
	* I rely on /etc/hosts entries most of the time for testing
* You probably know this, but you must have Viptela cloud-ops whitelist your source IPs
