import asyncio
import websockets

async def receivesAndSend(websocket):
    # Receives
    infoReceived = await websocket.recv()
    print(f'Receiving: {infoReceived}')

    # Send
    infoSending = f'Hi, I just received this: {infoReceived}!'
    print(f'Sending: {infoSending}')
    await websocket.send(infoSending)

async def main():
  async with websockets.serve(receivesAndSend, "localhost", 8765):
     await asyncio.Future()

if __name__ == "main":
   asyncio.run(main())