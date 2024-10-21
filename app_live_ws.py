import json
import os

import uvicorn
import zmq
import zmq.asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

from app_live import app as reduction_viewer

load_dotenv()

APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = os.getenv("APP_PORT", 8075)

app = FastAPI()
# Mount the Dash app as a sub-application in the FastAPI server
app.mount("/reduction_viewer", WSGIMiddleware(reduction_viewer.server))

host = "127.0.0.1"
port = "5001"

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://{}:{}".format(host, port))
socket.setsockopt_string(zmq.SUBSCRIBE, "")


async def zmq_listener(websocket: WebSocket):
    while True:
        message = await socket.recv_json()
        print("Received message:", message)
        await websocket.send_text(json.dumps(message))


# Define the main API endpoint rerouting to the Dash app
@app.get("/")
def index():
    return RedirectResponse(url="/reduction_viewer")


@app.get("/reduction_update")
async def get():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket</title>
    </head>
    <body>
        <h1>Position Update WebSocket Messages</h1>
        <div id="messages"></div>
        <script>
            var ws = new WebSocket("ws://{APP_HOST}:{APP_PORT}/ws/reduction_update");
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages')
                var message = document.createElement('div')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            }};
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws/reduction_update")
async def reduction_update(websocket: WebSocket):
    await websocket.accept()
    await zmq_listener(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
