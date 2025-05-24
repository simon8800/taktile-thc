import requests
import sys

LIST_DECISION_FLOWS_API_URL = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/list-decision-graphs/sandbox/decide"
GET_DECISION_GRAPH_API_URL = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/get-decision-graph/sandbox/decide"
PATCH_DECISION_GRAPH_API_URL = "https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/patch-decision-graph/sandbox/decide"
JSON_MEDIA_TYPE = "application/json"


def flow_id_exists(flow_id, api_key):
    """
    Validates if a flow with the given ID exists in the organization's flows
    Return True if the flow exists, else False
    """
    try:
        data = {
            "data": {"organization_name": "NB36"},
            "metadata": {"version": "v1.0", "entity_id": "string"},
            "control": {"execution_mode": "sync"},
        }
        headers = {
            "accept": JSON_MEDIA_TYPE,
            "Content-Type": JSON_MEDIA_TYPE,
            "X-Api-Key": api_key,
        }
        response = requests.post(
            LIST_DECISION_FLOWS_API_URL, json=data, headers=headers
        )
        parsed_response = response.json()
        flows = parsed_response.get("data", {}).get("flows", [])
        for flow in flows:
            if flow.get("flow_id") == flow_id:
                return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error handling request: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in flow_id_exists: {e}")


def node_id_exists(flow_id, node_id, api_key):
    """
    Validates if a node with the given ID exists in the flow and is a 'code_node'
    Returns "valid", "not found", or "wrong type", or None on error.
    """
    try:
        data = {
            "data": {"flow_id": flow_id},
            "metadata": {"version": "v1.0", "entity_id": "string"},
            "control": {"execution_mode": "sync"},
        }
        headers = {
            "accept": JSON_MEDIA_TYPE,
            "Content-Type": JSON_MEDIA_TYPE,
            "X-Api-Key": api_key,
        }
        response = requests.post(GET_DECISION_GRAPH_API_URL, json=data, headers=headers)
        parsed_response = response.json()
        graph = parsed_response.get("data", {}).get("graph", [])
        node_found = correct_node_type = False
        for node in graph:
            if node.get("node_id") == node_id:
                node_found = True
                if node.get("node_type") == "code_node":
                    correct_node_type = True
                    break
        if node_found and correct_node_type:
            return "valid"
        elif not node_found:
            return "not found"
        else:
            return "wrong type"
    except requests.exceptions.RequestException as e:
        print(f"Error handling request: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in node_id_exsits: {e}")
        return None


def deploy_code_to_taktile_node(flow_id, node_id, src_code_file_path, api_key):
    try:
        with open(src_code_file_path, "r") as f:
            src_code = f.read()
        data = {
            "data": {"flow_id": flow_id, "node_id": node_id, "src_code": src_code},
            "metadata": {"version": "v1.0", "entity_id": "string"},
            "control": {"execution_mode": "sync"},
        }
        headers = {
            "accept": JSON_MEDIA_TYPE,
            "Content-Type": JSON_MEDIA_TYPE,
            "X-Api-Key": api_key,
        }
        print(
            f"Deploying {src_code_file_path} to Flow ID: {flow_id}, Node ID: {node_id}"
        )
        response = requests.post(
            PATCH_DECISION_GRAPH_API_URL, json=data, headers=headers
        )
        parsed_response = response.json()
        data = parsed_response.get("data", {})
        if data.get("status") == "success":
            print(f"Deployment to Node {node_id} successful!")
            return True
    except FileNotFoundError:
        print(f"Error: Source code file not found at '{src_code_file_path}'")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error handling request: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in deploy_code_to_taktile_node: {e}")
        return False


if __name__ == "__main__":
    FLOW_ID = sys.argv[1]
    NODE_ID = sys.argv[2]
    SRC_CODE_FILE_PATH = sys.argv[3]
    API_KEY = sys.argv[4]

    if not flow_id_exists(FLOW_ID, API_KEY):
        print(f"Error: Flow ID '{FLOW_ID}' does not exist")
        sys.exit(1)

    node_status = node_id_exists(FLOW_ID, NODE_ID, API_KEY)
    if node_status == "valid":
        deploy_code_to_taktile_node(FLOW_ID, NODE_ID, SRC_CODE_FILE_PATH, API_KEY)
    elif node_status == "not found":
        print(f"Error: Node ID '{NODE_ID}' does not exist")
        sys.exit(1)
    elif node_status == "wrong type":
        print(f"Error: Node with ID '{NODE_ID}' is not of type 'code_node'")
        sys.exit(1)
    elif node_status is None:
        print("Error validating node ID")
        sys.exit(1)
