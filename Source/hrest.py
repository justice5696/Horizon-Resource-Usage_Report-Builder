
import json, requests, ssl

class Connection:
    def hv_connect(username, password, domain, hostname):
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        url = f"https://{hostname}"
        data = {"domain": domain, "password": password, "username": username}
        json_data = json.dumps(data)

        response = requests.post(f'{url}/rest/login', verify=False, headers=headers, data=json_data)
        data = response.json()

        access_token = {
            'accept': '*/*',
            'Authorization': 'Bearer ' + data['access_token']
        }
        return access_token

    def hv_disconnect(hostname, access_token):
        url = f"https://{hostname}"
        requests.post(f'{url}/rest/logout', verify=False, headers=access_token)

class Pools:
    def list_hvpools(hostname,access_token):
        url = f"https://{hostname}"
        response = requests.get(f'{url}/rest/inventory/v5/desktop-pools', verify=False,  headers=access_token)
        return response.json()

    def get_VirtualCenters(hostname, access_token):
        """ Gets the vCenter information for a given Horizon Connection Server (hostname)

        Parameters
        ----------
        hostname : str
            The IP or hostname of the Horizon Connection  Server that will be connected to
        access_token : str
            A web authentication token for the given hostname that will allow for API Calls

        Returns
        -------
        response.json(0)
            a list of all vCenters for this Horizon environment, as well as their configuration information. 
            a list of dictionaries - each dictionary corresponds to a vCenter.
        """
        url = f"https://{hostname}"
        response = requests.get(f'{url}/rest/config/v2/virtual-centers', verify=False,  headers=access_token)
        return response.json()