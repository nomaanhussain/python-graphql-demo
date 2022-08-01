from .live_traffic import *
from .process_nodes import *
from .user_interface import *
from .process_nodes import *


def resolve_autograph(obj, info):
    try:

        json_file = json.load(open('generated.json'))
        response_data = [get_nodes(json_file, False, [])]
        response_data.append(get_ui_element(response_data))
        response_data[1]["ObjectType"] = generate_ui_techknow(response_data)

        process_auto_graph_data(response_data[0], json_file)

        response_data[0]["nodes"] = auto_graph_generate_nodes(response_data[0]["nodes"], json_file)

        payload = {
            "success": True,
            "links": response_data[0]["links"],
            "nodes": response_data[0]["nodes"]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


def resolve_livegraph(obj, info):
    try:

        json_file = json.load(open('generated.json'))
        response_data = [get_nodes(json_file, False, [])]
        response_data.append(get_ui_element(response_data))
        response_data[1]["ObjectType"] = generate_ui_techknow(response_data)

        outside_changes_color(response_data[0])
        process_live_data(response_data[0], json_file)

        response_data[0]["nodes"] = live_graph_generate_nodes(response_data[0]["nodes"], json_file)

        for el in response_data[0]["links"]:
            if el["value"] < 50:
                colour_gradient_list = colour_gradient("#00FF00", "#FFFF00", 50)
                el["color"] = colour_gradient_list[el["value"]].hex
            else:
                colour_gradient_list = colour_gradient("#FFFF00", "#FF0000", 50)
                el["color"] = colour_gradient_list[el["value"] - 1 - 50].hex
        
        

        payload = {
            "success": True,
            "links": response_data[0]["links"],
            "nodes": response_data[0]["nodes"]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload