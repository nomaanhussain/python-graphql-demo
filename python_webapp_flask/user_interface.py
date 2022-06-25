
def create_template_new_node(counter, cluster, svg, elem, port):
    return  {
        "id": counter,
        "groupID": cluster,
        "status": "online",
        "ep_icon": svg,
        "name": elem["id"],
        "ip": elem["id"].split(":")[0],
        "ports": port
    }

def create_template_cluster(i, cluster):
    return {
           "id":  i,
           "image": chr(i + 64),
           "name": cluster["Name"]
    }

def get_ui_element(data, json_connections = 0):
    navbar = ""
    response_data = {}

    if(json_connections == 0):
        prev_data = data[0]
        response_data = {
            "UI-Interface": []
        }
    else:
        response_data = {
            "UI-Interface": [],
            "groups": [],
            "ObjectType": []
        }
        prev_data = data
        navbar = json_connections["clusters"]

    nodes = []
    counter = 0
    for elem in prev_data["nodes"]:
        try:
            counter += 1
            cluster = ""
            svg = ""
            port = ""    
            try:
                cluster = elem["cluster"] - 1
                svg = elem["svg"]
                port = elem["id"].split(":")[1]
            except:
                pass

            new_node = create_template_new_node(counter, cluster, svg, elem, port)

            if(new_node["ports"] == ""):
                del new_node["ports"]
            if(new_node["ep_icon"] == ""):
                del new_node["ep_icon"]
            if(new_node["groupID"] == ""):
                del new_node["groupID"]

            if(not new_node["name"].startswith("Cluster")):
                nodes.append(new_node)
        except:
            pass
    response_data["UI-Interface"] = nodes

    if(navbar != ""):
        groups = []
        i = 1
        for cluster in navbar:
            group_obj = create_template_cluster(i, cluster)
            groups.append(group_obj)
            i += 1
        response_data["groups"] = groups

    ObjectType = []

    children = []
    for elem in prev_data["nodes"]:
        try:
            if(elem["svg"].rsplit("/",1)[1].split(".")[0] == "student-computer"):
                new_dict = {
                    "id": elem["index"] + 1,
                    "name": elem["id"]
                }
                children.append(new_dict)
        except:
            pass
    Servers = {
        "category": "Servers",
        "child": children
    }

    if(len(Servers["child"])):
        ObjectType.append(Servers)

    children = []
    for elem in prev_data["nodes"]:
        try:
            if(elem["svg"].rsplit("/",1)[1].split(".")[0] == "printer"):
                new_dict = {
                    "id": elem["index"] + 1,
                    "name": elem["id"]
                }
                children.append(new_dict)
        except:
            pass
    Clients = {
        "category": "Clients",
        "child": children
    }
    if(len(Clients["child"])):
        ObjectType.append(Clients)

    if(len(Clients["child"]) or len(Servers["child"])):
        response_data["ObjectType"] = ObjectType
    return response_data

def generate_ui_techknow(response_data):
    objectTypeJson = [{"category": "Servers", "child": []}, {"category": "Clients", "child": []}]

    idx_server, idx_client = 0, 0
    for item in response_data[0]["nodes"]:
        if item["incoming"] > 2:
            objectTypeJson[0]["child"].append({ "id": idx_server, "name": "Server " + str(idx_server)})
            idx_server += 1
        else:
            objectTypeJson[1]["child"].append({ "id": idx_client, "name": "Client " + str(idx_client)})
            idx_client += 1
    return objectTypeJson