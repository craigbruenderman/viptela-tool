import json


# Methods

def getInventory(obj):
    response = obj.get_request('system/device/vedges')
    json_data = json.loads(response)

    inventoryList = []
    entry = []
    for item in json_data['data']:
        entry = [item['system-ip'],  item['host-name']]
        inventoryList.append(entry)
    return inventoryList
    
    
def listEdges(obj):
    response = obj.get_request('system/device/vedges')
    json_data = json.loads(response)
    #print json_data['data']
    edgeList = []
    keys = ['uuid', 'hostname', 'local-system-ip', 'managementSystemIP']
    for edge in json_data['data']:
        if edge.has_key('uuid'):
            if edge.has_key('host-name'):
                if edge.has_key('local-system-ip'):
                    entry = [edge['uuid'], edge['host-name'], edge['local-system-ip'], edge['managementSystemIP']]
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


def getOMPStatus(obj):
    #GET dataservice/device/omp/status
    pass


def getOMPSessions(obj):
    #GET /device/omp/peers
    pass


def getRoutes(obj):
    #GET /device/ip/routetable
    pass


def getBFDSummary(obj, systemIP):
    u = "dataservice/device/bfd/summary?deviceId=%s" % (systemIP)
    response = obj.get_request(u)
    #json_data = json.loads(response)['data']
    #return json_data


def getBFDDowns(obj, systemIP):
    u = "dataservice/device/bfd/history?deviceId=%s" % (systemIP)
    response = obj.get_request(u)
    json_data = json.loads(response)['data']
    print json_data

    
def getStats(obj, systemIP):
    u = "dataservice/device/interface/stats?deviceId=%s" % (system_ip)
    response = obj.get_request(u)
    json_data = json.loads(response)['data']


def getTunnelStats(obj):
    """docstring for getTunnelStats"""
    pass


def getOSPFRoutes(obj, systemIP):
    u = "device/ospf/routes?deviceId=%s" % (systemIP)
    try: 
        response = obj.get_request(u)
        json_data = json.loads(response)['data']
        keys = ['Area', 'Cost', 'Prefix', 'Next Hop', 'Interface']
        routeDict = dict()
        routeList = []
        for route in json_data:
            #print route
            #print route['prefix']
            #print route['next-hop']
            # List of values
            routeEntry = [route['area-id'], route['cost'], route['prefix'], route['next-hop'], route['if-name']]
            routeDict = dict(zip(keys, routeEntry))
            routeList.append(routeDict)
        return routeList
    except: 
        print "No OSPF routes"
    

def getOSPFNeighbors(obj, systemIP):
    u = "device/ospf/neighbor?deviceId=%s" % (systemIP)        
    try: 
        response = obj.get_request(u)
        json_data = json.loads(response)['data']
        neighborDict = dict()
        neighborList = []
        keys = ['Neighbor State', 'Router ID']
        for neighbor in json_data:
            neighborEntry = neighbor['neighbor-state'], neighbor['router-id']        
            neighborDict = dict(zip(keys, neighborEntry))
            neighborList.append(neighborDict)
        return neighborList
    except:
        print "Failed to get OSPF Neighbors"


def getBGPRoutes(obj):
    """docstring for bgpRoutes"""
    pass
    

def getBGPNeighbors(obj):
    """docstring for getBGPNeighbors"""
    pass
