import asyncio
from datetime import datetime

class ChatServer:
    def __init__(self):
        self.rooms = {}
        self.clients = set() # client = (writer, reader, name)
    

    async def send_messages(self, sender, message:str, room_name):
        '''
        Sends a message from a sender to all client in a room given
        '''
        tasks = []
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for client in self.rooms[room_name]:
            if sender == client:
                tmp = message
                if tmp.startswith('<FILE>'):
                    tmp = 'FILE'
                client[0].write(f"You, {time_now}: {tmp}".encode())
            else:
                client[0].write(f"{sender[2]}, {time_now}: {message}".encode())
            tasks.append(asyncio.create_task(client[0].drain()))
        await asyncio.gather(*tasks)

    async def send_message(self, writer, response):
        '''
        Sends a message to a specific client
        '''
        writer.write(f"Server msg: {response}\n".encode())
        await writer.drain()

    async def log_message(self, client, room, message):
        '''
        Prints a message indicating which client in which room sent a message
        Server-side logging
        '''
        print(f"Client {client[2]}, from {room}, {message}")

    async def receive_message(self, client, room_name):
        '''
        Allows a client to continuosly receive and handle messages
        '''
        while True:
            message = (await client[1].read(4096)).decode().strip()
            await self.log_message(client, room_name, f"sent: {message}")

            if message == "exit":
                await self.exit(client, room_name)
                return

            await self.send_messages(client, message, room_name)

    async def start_server(self):
        '''
        Binds server to localhost:55556 and starts it
        '''
        server = await asyncio.start_server(self.handle_client, 'localhost', 55556)
        addr = server.sockets[0].getsockname()
        print(f"Server: {addr}")

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        '''
        Main handle method

        '''
        addr = writer.get_extra_info('peername')
        await self.send_message(writer, "Enter your name")
        name = (await reader.read(4096)).decode().strip()
        client = (writer, reader, name)

        await self.log_message(client, "No room", f"{name} joined the server")
        await self.send_message(writer, f"Your name: {name}\ncreate to create a room\nenter to enter a room")

        # wait until client create\join a room
        while True:
            action = (await client[1].read(4096)).decode().strip()
            await self.log_message(client, "No room", f"Entered the command: {action}")

            if action == "create":
                await self.create_room(client)
                room_name = await self.enter_room(client)
            elif action == "enter":
                self.clients.add((client, "no room"))
                room_name = await self.enter_room(client)
            elif action == "exit":
                await self.exit(client, "no room")
            else:
                continue
            break

        await self.receive_message(client, room_name)

    async def enter_room(self, client) -> str:
        '''
        Allows a client to enter a room
        '''
        if (client, "no room") in self.clients:
            all_rooms = "\n".join(self.rooms.keys())
            await self.send_message(client[0], f"Enter the room you want to join:\n{all_rooms}")
            while True:
                room_name = (await client[1].read(4096)).decode().strip()
                if room_name in self.rooms:
                    break
                await self.send_message(client[0], "Room not found")
            self.rooms[room_name].append(client)
        else:
            for name_key, people_room in self.rooms.items():
                if client in people_room:
                    room_name = name_key

        await self.send_message(client[0], f"You joined the room {room_name}. Type 'exit' to leave.")
        await self.log_message(client, "No room", f"Joined the room {room_name}")
        await self.send_messages(client, "Joined the room", room_name)

        return room_name

    async def exit(self, client, room_name):
        '''
        Handle a client exiting a room
        '''
        await self.send_message(client[0], "Connection lost")
        if room_name != "no room":
            self.rooms[room_name].remove(client)
            await self.log_message(client, room_name, f"Entered command: exit")
        client[0].close()

    async def create_room(self, client):
        '''
        Create a new room
        '''
        await self.send_message(client[0], "Enter the room name")
        while True:
            room_name = (await client[1].read(4096)).decode().strip()
            if room_name in self.rooms:
                await self.send_message(client[0], "This room already exists")
            else:
                self.rooms[room_name] = [client]
                self.clients.add((client, room_name))
                await self.log_message(client, "No room", f"created the room {room_name}")
                break


if __name__ == "__main__":
    chat_server = ChatServer()
    asyncio.run(chat_server.start_server())
