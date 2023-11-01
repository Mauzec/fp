import asyncio
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.rooms = {}  # Dictionary to store rooms and their clients
        self.clients = set()

    async def send_messages(self, sender, message, room_name):
        tasks = []
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for client in self.rooms[room_name]:
            if sender == client:
                client[0].write(f"You, {time_now}: {message}".encode())
            else:
                client[0].write(f"{sender[2]}, {time_now}: {message}".encode())
            tasks.append(asyncio.create_task(client[0].drain()))
        await asyncio.gather(*tasks)

    async def send_message(self, writer, response):
        writer.write(f"Server msg: {response}\n".encode())
        await writer.drain()

    async def broadcast_message(self, client, room, message):
        print(f"Client {client[2]}, from {room}, {message}")

    async def receive_message(self, client, room_name):
        while True:
            message = (await client[1].read(1024)).decode().strip()
            await self.broadcast_message(client, room_name, f"sent: {message}")

            if message == "exit":
                await self.exit(client, room_name)
                return

            await self.send_messages(client, message, room_name)

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, 'localhost', 55556)
        addr = server.sockets[0].getsockname()
        print(f"Server: {addr}")

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        await self.send_message(writer, "Enter your name")
        name = (await reader.read(1024)).decode().strip()
        client = (writer, reader, name)

        await self.broadcast_message(client, "No room", f"{name} joined the server")
        await self.send_message(writer, f"Your name: {name}\ncreate to create a room\nenter to enter a room")

        while True:
            action = (await client[1].read(1024)).decode().strip()
            await self.broadcast_message(client, "No room", f"Entered the command: {action}")

            if action == "create":
                await self.create_room(client)
                room_name = await self.enter_room(client)
            elif action == "enter":
                self.clients.add((client, "no room"))
                room_name = await self.enter_room(client)
            elif action == "exit":
                await self.exit(client, "no room")
            else:
                await self.send_message(client[0], "Wrong command")
                continue
            break

        await self.receive_message(client, room_name)

    async def enter_room(self, client) -> str:
        if (client, "no room") in self.clients:
            all_rooms = "\n".join(self.rooms.keys())
            await self.send_message(client[0], f"Enter the room you want to join:\n{all_rooms}")
            while True:
                room_name = (await client[1].read(1024)).decode().strip()
                if room_name in self.rooms:
                    break
                await self.send_message(client[0], "Room not found")
            self.rooms[room_name].append(client)
        else:
            for name_key, people_room in self.rooms.items():
                if client in people_room:
                    room_name = name_key

        await self.send_message(client[0], f"You joined the room {room_name}. Type 'exit' to leave.")
        await self.broadcast_message(client, "No room", f"Joined the room {room_name}")
        await self.send_messages(client, "Joined the room", room_name)

        return room_name

    async def exit(self, client, room_name):
        await self.send_message(client[0], "Connection lost")
        if room_name != "no room":
            self.rooms[room_name].remove(client)
            await self.broadcast_message(client, room_name, f"Entered command: exit")
        client[0].close()

    async def create_room(self, client):
        await self.send_message(client[0], "Enter the room name")
        while True:
            room_name = (await client[1].read(1024)).decode().strip()
            if room_name in self.rooms:
                await self.send_message(client[0], "This room already exists")
            else:
                self.rooms[room_name] = [client]
                self.clients.add((client, room_name))
                await self.broadcast_message(client, "No room", f"created the room {room_name}")
                break


if __name__ == "__main__":
    chat_server = ChatServer()
    asyncio.run(chat_server.start_server())
