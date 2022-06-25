from .live_traffic import *
from .process_nodes import *
from .user_interface import *



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


