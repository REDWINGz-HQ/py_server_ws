import asyncio
import websockets
import json

clients = {}

async def register_client(websocket, client_name):

    if client_name not in clients:
        clients[client_name] = websocket
        print("----------------------------------------------------")
        print(f"Client {client_name} connected.")
        print("----------------------------------------------------")

async def unregister_client(client_name):
    if client_name in clients:
        del clients[client_name]
        print("----------------------------------------------------")
        print(f"Client {client_name} disconnected.")
        print("----------------------------------------------------")

async def handle_message(message,sender_name):

    message_json = json.loads(message)
    
    # Ensure that 'uuid' and 'message' keys exist
    if "uuid" not in message_json or "message" not in message_json:
        raise KeyError("Missing 'id' or 'message' in the received JSON.")
    
    target_client = message_json["id"]
    data = message_json["message"]
    
    if target_client in clients:
        websocket = clients[target_client]
        await websocket.send(json.dumps(data))  # Send the message as JSON
        print(f"Message from {sender_name} sent to {target_client}: {data}")
    else:
        print(f"Target client {target_client} not found.")

async def handler(websocket, path):

    try:
        client_name = await websocket.recv()
        await register_client(websocket, client_name)
        async for message in websocket:
            await handle_message(message, client_name)

    except websockets.ConnectionClosedOK:
        print(f"Connection with client closed normally.")

    except websockets.exceptions.ConnectionClosed:
        # print(f"Connection with client {client_name} closed unexpectedly.")
        await unregister_client(client_name)

    except Exception as e:
        print(f"Error in connection handler: {e}")
    
    finally:
        await unregister_client(client_name)

# Start the WebSocket server

start_server = websockets.serve(handler, "0.0.0.0", 8000)

print("Started server.....")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
