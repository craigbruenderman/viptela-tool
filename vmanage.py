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
from tabulate import tabulate
import viptela


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
        #print url
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.content
        return data

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:443/dataservice/%s"%(self.vmanage_ip, mount_point)
        payload = json.dumps(payload)
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.content


def main(args):
    if not len(args) == 3:
        print __doc__
        return
    vmanage_ip, username, password = args[0], args[1], args[2]
    obj = rest_api_lib(vmanage_ip, username, password)
    
    #print getTenants(obj)
    #print "--------"
    for edge in viptela.listEdges(obj):
        #print edge['managementSystemIP']
        #print edge

        neighbors = viptela.getOSPFNeighbors(obj, edge['managementSystemIP'])
        if neighbors:
            for neighbor in neighbors:
                print neighbor
                #printTable(neighbor, neighbors[0].keys())

#        ospfRoutes = getOSPFRoutes(obj, edge['managementSystemIP'])
#        if ospfRoutes:
#            print ospfRoutes[0].keys()
#            for route in ospfRoutes:
#                print route
#                

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    
    
