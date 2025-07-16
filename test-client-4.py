import sseclient
import requests
# import json
import time

SSE_URL = "http://localhost:8000/sse/"
BASE_URL = "http://localhost:8000"

def make_post_request(endpoint_path, payload):
    """Makes a POST request to the MCP tool endpoint with a JSON-RPC payload."""
    url = f"{BASE_URL}{endpoint_path}"
    print(f"Making POST request to {url} with payload: {payload}...")
    try:
        response = requests.post(url, json=payload)
        print(f"POST response status: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"POST request error: {e}")
        return None

def start_sse_client():
    """Starts an SSE client, receives endpoint, sends tool call, and listens for result."""
    print(f"Connecting to SSE stream at {SSE_URL}...")
    try:
        # Open stream connection
        response = requests.get(SSE_URL, stream=True, headers={"Accept": "text/event-stream"})
        client = sseclient.SSEClient(response.raw)

        endpoint_path = None

        # Listen for endpoint message
        for event in client.events():
            if event.event == "endpoint":
                endpoint_path = event.data
                time.sleep(0.5)
                print(f"Endpoint received: {endpoint_path}")
                break

        if not endpoint_path:
            print("No endpoint received. Aborting.")
            return

        # Build tool payload
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "calculate",  # Change if needed
            "params": {
                "expression": "2 + 3 * 4"
            }
        }

        # Send the tool call
        status = make_post_request(endpoint_path, payload)
        if status != 202:
            print("Unexpected status from tool call POST. Aborting.")
            return

        print("Listening for tool_result event...")

        # Listen for tool_result
        for event in client.events():
            print(f"Event Type: {event.event}")
            print(f"Data: {event.data}")
            if event.event == "tool_result":
                break

        time.sleep(1)
        client.close()
        print("Stream closed cleanly.")

    except requests.exceptions.ConnectionError as e:
        print(f"SE connection error: {e}")
    except Exception as e:
        print(f"Unexpected error in SSE client: {e}")

if __name__ == "__main__":
    # This client runs everything in order
    start_sse_client()
