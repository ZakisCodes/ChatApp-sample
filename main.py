from fastapi import FastAPI 
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from manager import WebSocketManager
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="ChatApp")

origins = [
    "https://cloackchat.onrender.com",  # Your Render domain
    "http://localhost:3000",           # Your local development frontend, for testing
    "http://127.0.0.1:3000",
    "http://localhost:8000"            # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = WebSocketManager()

template = Jinja2Templates(directory="templates")
@app.get("/")
def root_endpoint(request : Request):
    return template.TemplateResponse('test.html',
                                     {
                                         "request" : request
                                     })

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    while True:
        try:
            message = await websocket.receive_json()
            print(f"Message Recieved: {message}")
                        # braodcasting the messages
           # for client in manager.connected_clients:
            #    await manager.send_message(message,client)

            # Prepare the message for broadcasting
            broadcast_message = {
                "client": f"{websocket.client.host}:{websocket.client.port}", # type: ignore
                "message": message.get("content", "No content provided")
            }

            # Broadcast the message to all clients using the new method
            await manager.broadcast(broadcast_message, websocket)
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
            
