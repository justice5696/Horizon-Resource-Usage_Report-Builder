# Horizon Resource Usage_Report Builder
 A tool to build an xlsx file containing the aggregated data of all Horizon Desktops' resource usage in vCenter

Must call the Python script HRUC.py with the following syntax:
    python _"path"_\HRUC.py _"Path to INI Config File"_.ini

The script queries all of the given Horizon Pods and any vCenter server connected to those Horizon Pods. From Horizon, it pulls each Pool and associated pool data. From vCenter, it pulls the resource usage and capacity of each cluster (CPU and Memory). All of this data together produces a Dictionary for every vCenter Cluster, and within the dictionary entry for each Cluster is a list of every single Pool that leverages the cluster. From this data an, Excel file is generated. Each sheet of the Excel file corresponds to a vCenter Cluster, and the max possible resource usage is computed (Max number of desktops in a pool * size of desktops in the automated pool).

The DailyRunPython.ps1 file can be used to run the python script automatically every X seconds and automatically copy the produced Excel sheets to some remote/local share. 

The PythonEnvironment_BuildInstructions.txt file lists the original build environment used to develop the script. It goes over the version of python and of the various modules used, and how to install it all on a Windows machine. 

The INI file has the following fields:
    - HorizonHosts: a list of Horizon Connection servers. Each Connection server should be from a different POD.
    - Username: a domain username with Read-Only Administrator privileges in all Horizon Pods and any vCenter that the Horizon Pods are connected to.
    - Password: the password of the above username
    - Domain: the domain of the above credentials

    *** The account listed in the INI file must have Read-Only Admin permissions in all Horizon and vCenter Environments that will be queried. ***
