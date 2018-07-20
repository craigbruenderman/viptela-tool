#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Class with REST Api GET and POST libraries

Example: python rest_api_lib.py vmanage_hostname username password

PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage

Note: All the three arguments are manadatory
"""

import requests
import sys
import json
import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class rest_api_lib:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.login(self.vmanage_ip, username, password)

    def login(self, vmanage_ip, username, password):
        #Login to vmanage
        base_url_str = 'https://%s/'%vmanage_ip

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url_str + login_action
        url = base_url_str + login_url
        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if '<html>' in login_response.content:
            print "Login Failed"
            sys.exit(0)

        self.session[vmanage_ip] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:443/dataservice/%s"%(self.vmanage_ip, mount_point)
        print url
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:443/dataservice/%s"%(self.vmanage_ip, mount_point)
        payload = json.dumps(payload)
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.content

# Methods

def getInventory(obj):
    response = obj.get_request('system/dataservice/device')
    json_data = json.loads(response)
    print(json_data)
    for item in json_data['data']:
        print(item)

    # Initialize the inventory data dictionary
    inv = {}
    # Store each item in the dictionary with the key of the "system-ip"
    for item in json_string['data']:
    #   print (item['local-system-ip']+"   "+item['host-name'])
        inv[item['system-ip']] = item['host-name']
    return(inv)
    
def listEdges(obj):
    response = obj.get_request('system/device/vedges')
    json_data = json.loads(response)
    edgeList = []
    keys = ['uuid', 'hostname', 'local-system-ip']
    for edge in json_data['data']:
        if edge.has_key('uuid'):
            if edge.has_key('host-name'):
                if edge.has_key('local-system-ip'):
                    entry = [edge['uuid'], edge['host-name'], edge['local-system-ip']]
                    edgeList.append(dict(zip(keys, entry)))
    return edgeList
    
def getTenants(obj):
    response = obj.get_request('tenantstatus')
    json_data = json.loads(response)
    tenantList = []
    keys = ['TenantName', 'TenantID']
    for item in json_data['data']:
        entry = [item['tenantName'], item['tenantId']]
        tenantList.append(dict(zip(keys, entry)))
    return tenantList
    
def getStats(obj,systemIP):
    response = obj.get_request('dataservice/device/interface/stats?deviceId="+system_ip')
    json_data = json.loads(response)['data']

def getTunnelStats(obj):
    """docstring for getTunnelStats"""
    pass

def getOSPFRoutes(obj):
    response = obj.get_request('device/ospf/routes?deviceId=169.254.10.9')
    json_data = json.loads(response)['data']
    #return json_data
    for route in json_data:
        print route['prefix']
    
def getOSPFNeighbors(obj):
    response = obj.get_request('device/ospf/neighbor?deviceId=169.254.10.9')
    json_data = json.loads(response)['data']
    neighborList = []
    keys = ['Neighbor State', 'Router ID']
    for route in json_data:
        entry = route['neighbor-state'], route['router-id']
        neighborList.append(zip(keys, entry))
    return neighborList

def getBGPRoutes(obj):
    """docstring for bgpRoutes"""
    pass
    
def getBGPNeighbors(obj):
    """docstring for getBGPNeighbors"""
    pass


def main(args):
    if not len(args) == 3:
        print __doc__
        return
    vmanage_ip, username, password = args[0], args[1], args[2]
    obj = rest_api_lib(vmanage_ip, username, password)
    
    #print getTenants(obj)
    #print "--------"
    #print listEdges(obj)
    print getOSPFNeighbors(obj)
    print "--------"
    print getOSPFRoutes(obj)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    
    
