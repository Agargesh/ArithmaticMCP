import requests
import sseclient
import time

# Set headers for the stream connection
headers = {
    "Accept": "text/event-stream",
    "Content-Type": "application/json"
}

# Connect to the SSE stream
print("Connecting to event stream...")
stream_response = requests.get("http://localhost:8000/sse/", headers=headers, stream=True)

if stream_response.status_code != 200:
    print(f"Failed to connect to /sse/. Status code: {stream_response.status_code}")
    exit(1)

client = sseclient.SSEClient(stream_response.raw)

# Wait for the 'endpoint' message with session_id
# not needed anymore
message_endpoint = None
for event in client.events():
    if event.event == "endpoint":
        message_endpoint = event.data
        print(f"Message endpoint received: {message_endpoint}")
        break

# Send the tool call with FULL JSON-RPC COMPLIANCE
# remove "if" create variable
if message_endpoint:
    payload = {
        "jsonrpc": "2.0",                 # Required
        "id": 1,                          # Required unique ID
        "method": "calculate",           # Or "add", "power", etc.
        "params": {
            "expression": "2 + 3 * 4"
        }
    }

    response = requests.post("http://localhost:8000" + message_endpoint, json=payload)
    print(f"Tool call sent. Status code: {response.status_code}")

# move client setup here

    # Read tool result from the event stream
    for event in client.events():
        print("Event Type:", event.event)
        print("Data:", event.data)

        if event.event == "tool_result":
            time.sleep(15)
            break

    client.close()  # Clean disconnect

else:
    print("Failed to receive message endpoint from the server.")
