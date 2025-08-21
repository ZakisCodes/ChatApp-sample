from fastapi.websockets import WebSocket

class WebSocketManager:
    def __init__(self):
        self.connected_clients = []

    async def connect(self, websocket: WebSocket):
        if websocket.client is not None:
            client_ip = f"{websocket.client.host}:{websocket.client.port}"
            print(f"Client: {websocket.client.host} and port: {websocket.client.port}") # type: ignore
        else:
            client_ip = "unknown"
            print("Client information is unavailable")

        await websocket.accept()
        self.connected_clients.append(websocket)
        print(f"Connected clients are {self.connected_clients}")
        # send welcome msg to client
        msg = {"client" : client_ip,
               "message": "Welcome to this braodcast"}
        await websocket.send_json(msg)
    
    async def broadcast(self, message: dict, sender: WebSocket):
        """
        Broadcasts a message to all connected clients.
        """
        for client in self.connected_clients:
            if client != sender:
                await client.send_json(message)
    
    async def send_message(self, message: dict, websocket: WebSocket):
        message = {
            "client" : f"{websocket.client.host}:{websocket.client.port}", # type: ignore
            "message" : message["content"]
        }
        await websocket.send_json(message)
    
    
    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)
        print(f"Client {websocket.client.host} : {websocket.client.port} disconnected") # type: ignore
        print(f"Connected clients {self.connected_clients}")
