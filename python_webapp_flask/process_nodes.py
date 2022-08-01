from requests.auth import HTTPBasicAuth
import requests
from netaddr import IPNetwork
import json

netObjUrl = ""


def spawn_node(ip):
    return {
        "id":ip,
        "connections":0,
        "incoming":0,
        "outgoing":0,
        "svg":""
    }

def get_nodes(json_file, want_port, internal_nodes=[]):
    json_data = {
            "nodes":[],
            "links":[]
    }

    for obj in json_file['items']:
        ip0 = obj['sourceIp']      # sender
        port0 = obj['sourcePort']

        ip1 = obj['destinationIp']     # receiver
        port1 = obj['destinationPort']

        if ip0 in internal_nodes and ip1 in internal_nodes or len(internal_nodes) == 0:
            if(want_port):
                ip1 = ip1 +":"+ str(port1)

            if(want_port):
                ip0 = ip0 +":"+ str(port0)

            if not {"id":ip1, "connections":0, "incoming":0, "outgoing":0, "svg":""} in json_data['nodes']:
                json_data['nodes'].append(spawn_node(ip1))
            if not {"id":ip0, "connections":0, "incoming":0, "outgoing":0, "svg":""} in json_data['nodes']:
                json_data['nodes'].append(spawn_node(ip0))

            if not {"source":ip0,"target":ip1} in json_data['links']:
                json_data['links'].append({"source":ip0,"target":ip1})

    return json_data


def generate_inside_ips_list():
    with requests.Session() as session:
        session.verify = False
        headers = {
            'User-Agent': 'REST API Agent'
        }

        #Get all network objects of type IPv4Adress and add to list
        excludeResponse = session.request("GET", netObjUrl, auth=HTTPBasicAuth('pcglabs', 'TheMarsian'),  headers=headers)
        excludeResponse = excludeResponse.json()

        addresses = []
        for item in excludeResponse['items']:
            if 'host' in item.keys():
                if item['host']['kind'] == 'IPv4Network':
                    ip_addr , mask = item['host']['value'].split('/')

                    network = IPNetwork('/'.join([ip_addr, mask]))
                    generator = network.iter_hosts()
                    for elem in generator:
                        addresses.append(str(elem))
    return addresses

def outside_changes_color(response_data):
    addresses = generate_inside_ips_list()

    for link in response_data["links"]:
        source_ip = link["source"]
        target_ip = link["target"]
        try:
            source_ip = link["source"].split(":")[0]
            target_ip = link["target"].split(":")[0]
        except:
            pass

        if source_ip not in addresses:
            link["color"] = "#0000FF"
        else:
        # if target_ip in addresses:
            link["color"] = "#0000FF"

    return response_data