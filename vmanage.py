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
import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from tabulate import tabulate
import viptela as v


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
    
    #tenants = v.getTenants(obj)
    #print "getTenants()\n"
    #print tabulate(tenants, headers="keys")
    
    vedges = v.getEdges(obj)
    print "getEdges()\n"
    print tabulate(vedges, headers="keys")
    
    controlConns = v.getControlConnections(obj, "169.254.10.8", "vsmart")
    print "getControlConnections()\n"
    print tabulate(controlConns, headers="keys")

#    print v.getStats(obj, "169.254.10.8")
    
    #print v.getRunConf(obj, "11OG427170281")
    #print v.getOSPFRoutes(obj, "169.254.10.8")
    
    # Get running config from sample vEdge
    #config = v.getRunConf(obj, "11OG403170902")
    
    # Get users
    #users = v.getUsers(obj)
    #print tabulate(users, headers="keys")
    
    # Get feature templates
    #featureTemplates = v.getFeatureTemplates(obj)
    #print featureTemplates[1]
    
    
    
#    for vedge in vedges:
#        print "\n"
#        print vedge['managementSystemIP']
#        neighbors = viptela.getOSPFNeighbors(obj, vedge['managementSystemIP'])
#        if neighbors:
#            print "\n"
#            print tabulate(neighbors, headers="keys")
#        ospfRoutes = viptela.getOSPFRoutes(obj, vedge['managementSystemIP'])
#        if ospfRoutes:
#            print "\n"
#            print tabulate(ospfRoutes, headers="keys")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    
    
