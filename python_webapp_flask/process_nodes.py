from requests.auth import HTTPBasicAuth
import requests
from netaddr import IPNetwork
import json


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



