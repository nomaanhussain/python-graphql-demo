import html
import requests
import datetime
from netaddr import IPNetwork
from colour import Color




    
def auto_graph_generate_nodes(nodes, json_file):
    incoming_data = outgoing_data = incoming_connections = outgoing_connections = {}

    for item in json_file['items']:
        if item['destinationIp'] not in incoming_data.keys():
            incoming_data[item['destinationIp']] = item['bytesSent']
            incoming_connections[item['destinationIp']] = 0 
        else:
            incoming_data[item['destinationIp']] += item['bytesSent']
            incoming_connections[item['destinationIp']] +=  1

        if item['sourceIp'] not in outgoing_data.keys():
            outgoing_data[item['sourceIp']] = item['bytesSent']
            outgoing_connections[item['sourceIp']] = 0 
        else:
            outgoing_data[item['sourceIp']] += item['bytesSent']
            outgoing_connections[item['sourceIp']] += 1
            
    return convert_nodes(nodes=nodes, items=json_file['items'], incoming_data=incoming_data, incoming_connections=incoming_connections, outgoing_data=outgoing_data, outgoing_connections=outgoing_connections)

def convert_nodes(nodes, items, incoming_data, incoming_connections, outgoing_data, outgoing_connections):
    for node in nodes:
        keys = ['connections', 'incoming', 'outgoing', 'svg']
        for key in keys:
            del node[key]

        node['status'] = "online"
        node['ip'] = node['id']
        node['id'] = 'HostUUID'
        #we can't get hostUUID as of now

        node['nodeName'] = protocol = sourcePort = node['macAddress'] = ''
        
        for item in items:
            if item['sourceIp'] == node['ip']:
                node['macAddress'] = item['srcMAC']
                protocol = item['protocol']
                sourcePort = item['sourcePort']
                if node['nodeName'] == '':
                    node['nodeName'] = item['hostName']
            if item['destinationIp'] == node['ip']:
                node['macAddress'] = item['dstMAC']

        addresses = get_ips(node['ip'])

        lst_ip = addresses[0].split('.') #TODO
        lst_ip[-1] = '0'

        node['ip_scope'] = '.'.join(lst_ip)
        node['ipGateway'] = addresses[0]

        node['networkGroup'] = ''


        if node['ip'] in incoming_data.keys():
            node['l_incomingData'] = incoming_data[node['ip']]
            node['l_incomingConn'] = incoming_connections[node['ip']]
        else:
            node['l_incomingData'] = 0
            node['l_incomingConn'] = 0

        if node['ip'] in outgoing_data.keys():
            node['l_outgoingData'] = outgoing_data[node['ip']]
            node['l_outgoingConn'] = outgoing_connections[node['ip']]
        else:
            node['l_outgoingData'] = 0
            node['l_outgoingConn'] = 0

        try:
            sourcePort = int(sourcePort)
        except:
            sourcePort = ''

        node = set_device_data(node, protocol, sourcePort)

    return nodes

def get_ips(ip):
    addresses = []
    network = IPNetwork('/'.join([ip, '24']))
    #TODO:find proper mask
    generator = network.iter_hosts()
    for elem in generator:
        addresses.append(str(elem))
    return addresses

def set_device_data(node, protocol, sourcePort):
    node['Port'] = {
            "id": "protocoPortObjUUID",
            "name": "protocolport_obj",
            "type": "ProtocolPortObject",
            "protocol": protocol,
            "port": int(sourcePort) if sourcePort else 0
          }

    if (node['l_outgoingConn'] == 0 and node['l_incomingConn'] > 0 and node['l_outgoingData'] == 0):
        objectType = 'Server'
    else:
        objectType = 'Client'

    node['objectType'] = objectType #TODO
    node['os'] = ''
    node['domain'] = ''
    node['deviceDetails'] = {
        "cpuType": "unknown",
        "cpuCores": "unknown",
        "memoryInMB": "unknown",
        "storageInGB": "unknown"
    }
    node['geo'] = {
        "name": "geolocation",
        "type": "Geolocation",
        "id": "geolocationUUID",
    }
    return node



def process_data(response_data, live_data, timeframe=10000):
    temp_links = {}

    for line in live_data["items"]:
        sourceIp, destinationIp = line["sourceIp"], line["destinationIp"]
        if f"{sourceIp}.{destinationIp}" not in temp_links:
            temp_links[f"{sourceIp}_{destinationIp}"] = line["bytesSent"]
        else:
            temp_links[f"{sourceIp}_{destinationIp}"] += line["bytesSent"]

    max_udp_length = 0
    for link in response_data["links"]:
        known_traffic = False
        for ip_key, udp_length in temp_links.items():
            source = ip_key.split("_")[0]
            target = ip_key.split("_")[1]
            if link["source"] == source and link["target"] == target:
                if udp_length > max_udp_length:
                    max_udp_length = udp_length
                link["value"] = udp_length
                known_traffic = True
                break
        if known_traffic is False:
            link["value"] = 0
    return response_data, max_udp_length

def process_auto_graph_data(response_data, live_data, timeframe=10000):
    response_data, max_udp_length = process_data(response_data, live_data, timeframe)

    for link in response_data["links"]:
        if link["value"] > 0:
            link['trafficType'] = 'TCP'
            #TODO:there's multiple types of traffic for IP1:IP2 connection ???
            link['absolutePath'] = [link['source'], link['target']]
        del link['value']

    return response_data

def transf_to_interval(value, max_value, a=1, b=100):
    if max_value == 0:
        return a
    return int(a + value / max_value * (b-a))

def colour_gradient(colour1, colour2, range):
    start = Color(colour1)
    colours = list(start.range_to(Color(colour2), range))

    return colours



def process_live_data(response_data, live_data, timeframe=10000):
    response_data, max_udp_length = process_data(response_data, live_data, timeframe)

    for link in response_data["links"]:
        if link["value"] > 0:
            link["CurrentTafficSize"] = link["value"]
            link["value"] = transf_to_interval(link["value"], max_udp_length)
            link['trafficType'] = 'TCP'
            #TODO:there's multiple types of traffic for IP1:IP2 connection ???
            link['absolutePath'] = [link['source'], link['target']]

    for el in response_data["links"]:
        if el["value"] < 50:
            colour_gradient_list = colour_gradient("#008000", "#ff0", 50)
            el["color"] = colour_gradient_list[el["value"]].hex
        else:
            colour_gradient_list = colour_gradient("#ff0", "#f00", 50)
            el["color"] = colour_gradient_list[el["value"] - 1 - 50].hex

    return response_data


def live_graph_generate_nodes(nodes, json_file):
    return auto_graph_generate_nodes(nodes, json_file)