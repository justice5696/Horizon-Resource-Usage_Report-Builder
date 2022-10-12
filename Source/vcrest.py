"""
Module: vcrest.py
A module of helper functions for getting vCenter Cluster and VM data. 
"""

import requests, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s=requests.Session()
s.verify=False

def getvCenterSession(hostname, username, password):
    """Gets a list of vCenter Rest API session objects

    Parameters
    ----------
    hostname : str
        The IP or hostname of the vCenter Server that will be connected to
    username : str
        The username of the account that will be used to authenticate to vCenter. Format <username>[@<domain>]
    password: str
        The password of the username parameter

    Returns
    -------
    s
        a vCenter Session object to be used for subsequent API calls
    """
    s.post(f"https://{hostname}/rest/com/vmware/cis/session",auth=(username,password))
    return s

def GetClusters(s, hostname):
    """Gets a list of vCenter Clusters from the vCenter hostname parameter using the vCenter Rest API

    Parameters
    ----------
    s : vCenter API Session Object
        a vCenter Session object that can be used for API calls
    hostname : str
        The IP or hostname of the vCenter Server whose Clusters will be returned.

    Returns
    -------
    Clusters
        the HTTP response to the Get Clusters API Call. Contains all clusters for the specified vCenter. 
        Does not contain the Resource Summary for the cluster - only name and clusterID
    """
    Clusters = s.get(f"https://{hostname}/rest/vcenter/cluster")
    return Clusters

def GetVMs(s, hostname):
    """Gets a list of VMs from the vCenter hostname parameter using the vCenter Rest API

    Parameters
    ----------
    s : vCenter API Session Object
        a vCenter Session object that can be used for API calls
    hostname : str
        The IP or hostname of the vCenter Server whose VMs will be returned.

    Returns
    -------
    VMs
        the HTTP response to the Get VMs API Call. Contains all VMs for the specified vCenter. 
    """
    VMs = s.get(f"https://{hostname}/rest/vcenter/vm")
    return VMs

#takes in a list of vcenters and a username and password
def getAllClusterInfo(hostnames, username, password):
    """Gets a list of vcenter clusters and their resource usage using the vCenter SDK for Python pyVmomi. This is required because 
    the Rest API does not have a method for returning resource values.\
    
    If a new vCenter REST API can return Resource Usage, change this function to use that.

    Parameters
    ----------
    hostname : str
        The IP or hostname of the vCenter Server that will be connected to
    username : str
        The username of the account that will be used to authenticate to vCenter. Format <username>[@<domain>]
    password: str
        The password of the username parameter

    Returns
    -------
    VCClist
        a list of lists. Each sub-list corresponds to a cluster and 
        contains: [vCenterHostname, clusterID, CPU Capacity, CPU Used, Memory Capacity, Memory Used]
    """

    VCCList = []
    def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj

    s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode=ssl.CERT_NONE
    for i in range(len(hostnames)):
        
        #for each vcenter hostname in hostnames create a session/connection
        c= SmartConnect(host=hostnames[i], user=username, pwd=password, disableSslCertValidation=True)
        content=c.content

        #create a list of clusters 
        cluster = [cluster for cluster in get_all_objs(content,[vim.ClusterComputeResource])]
        for cl in cluster:
            ru = cl.GetResourceUsage()
            clusterId = str(cl)
            cpuR = ru.cpuUsedMHz
            cpuC = ru.cpuCapacityMHz
            memR = ru.memUsedMB
            memC = ru.memCapacityMB
            tippy = [hostnames[i], clusterId, cpuC, cpuR, memC, memR]
            VCCList.append(tippy)

    return VCCList


def getAllClusterInfoSingle(hostname, username, password):
    """Gets a list of vcenter clusters and their resource usage using the vCenter SDK for Python pyVmomi. This is required because 
    the Rest API does not have a method for returning resource values.

    Only does this for a single vCenter 
    
    If a new vCenter REST API can return Resource Usage, change this function to use that.

    Parameters
    ----------
    hostname : str
        The IP or hostname of the vCenter Server that will be connected to
    username : str
        The username of the account that will be used to authenticate to vCenter. Format <username>[@<domain>]
    password: str
        The password of the username parameter

    Returns
    -------
    VCClist
        a list of lists. Each sub-list corresponds to a cluster and 
        contains: [vCenterHostname, clusterID, CPU Capacity, CPU Used, Memory Capacity, Memory Used]
    """

    VCCList = []
    def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj

    s=ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode=ssl.CERT_NONE
    
        
    #for each vcenter hostname in hostnames create a session/connection
    c= SmartConnect(host=hostname, user=username, pwd=password, disableSslCertValidation=True)
    content=c.content

    #create a list of clusters 
    cluster = [cluster for cluster in get_all_objs(content,[vim.ClusterComputeResource])]
    for cl in cluster:
        ru = cl.GetResourceUsage()
        clusterId = str(cl)
        cpuR = ru.cpuUsedMHz
        cpuC = ru.cpuCapacityMHz
        memR = ru.memUsedMB
        memC = ru.memCapacityMB
        tippy = [hostname, clusterId, cpuC, cpuR, memC, memR]
        VCCList.append(tippy)

    return VCCList


    
    





