import sseclient
# import json
import time
import requests

SSE_URL = "http://localhost:8000/sse/"
BASE_URL = "http://localhost:8000"

def start_client():
    print("connecting to SSE stream")
    response = requests.get(SSE_URL, headers={"Accept": "text/event-stream"}, stream=True)

    if response.status_code != 200:
        print(f"Failed to connect to SSE. Status code: {response.status_code}")
        return

    client = sseclient.SSEClient(response)

    endpoint_path = None
    for event in client.events():
        if event.event == "endpoint":
            endpoint_path = event.data  # This is something like "/messages/?session_id=..."
            print(f" Session endpoint received: {endpoint_path}")
            break

    if not endpoint_path:
        print("No endpoint received. Aborting.")
        return

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "calculate",  # Name of tool in @server.tool
        "params": {
            "expression": "2 + 3 * 4"
        }
    }

    print(f" Sending POST to {endpoint_path} with payload: {payload}")
    post_response = requests.post(BASE_URL + endpoint_path, json=payload)

    print(f"Tool call sent. Status code: {post_response.status_code}")
    if post_response.status_code != 202:
        print("Unexpected status from POST.")
        return

    print("Listening for results from server...")
    for event in client.events():
        print(f"Event Type: {event.event}")
        print(f"Data: {event.data}")
        if event.event == "tool_result":
            break

    time.sleep(60)
    client.close()
    print("Stream closed cleanly.")

if __name__ == "__main__":
    start_client()
