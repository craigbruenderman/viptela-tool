# viptela-tool

My feeble attempt at using the multi-tenant Viptela API.

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