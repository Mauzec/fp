import asyncio
import tkinter as tk

from tkinter import filedialog

class client:
    def __init__(self) -> None:
        self.gui = ''
        self.user =''

        self.host = 'localhost'
        self.port = 55556

        self.reader = ''
        self.writer = ''
        
    async def error(self, message):
        '''
        Used to print error messages
        '''
        print(f"error: {message}")
        
    async def receive_message(self): 
        '''
        Continuously read message from the server & displays them
        '''
        while True:
            message = await self.reader.read(4096)
            message = message.decode().strip()

            tmp = message.find('<FILE>') 
            if tmp >= 0:
                message = message[tmp:].split('<FILE>')
                with open(f'/Users/maus/hello/{message[1]}', 'wb') as f:
                    f.write(message[1])
                continue


            print(f"{message}")
            await self.gui.receive_message(message)  
            if "Connection lost" in message:
                return
            
    async def send_message(self, message):
        '''
        Send a message to the server
        '''
        if message == "": 
            self.error("No entries")
            return
        self.writer.write(message.encode())
        await self.writer.drain()
        if message == "exit":
            return
           
    async def start_client(self) -> None:
        '''
        Sets up the client
        '''
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("")
        
        await self.receive_message()
        self.writer.close()

    async def send_image(self, imagepath: str) -> None:
        '''
        Send a image to the server
        '''
        with open(imagepath, 'rb') as image_file:
            image_data = image_file.read()
            image_size = len(image_data)

            # send the image size first
            self.writer.write(f'<FILE>{image_size}<FILE>{image_data}'.encode())
            await self.writer.drain()
        
class Gui:
    def __init__(self, client):
        self.imagepath = None

        self.client = client
        
        self.root = tk.Tk()
        self.root.title("Client")
        self.root['background'] = "gray"

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side="right", fill="y")
        
        self.text_widget = tk.Text(self.root, wrap=tk.WORD, yscrollcommand=self.scrollbar.set)
        self.text_widget.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.text_widget.yview)

        self.text_entry = tk.Entry(self.root)
        self.text_entry.pack(side="left", fill="x",expand=True)

        self.send_button = tk.Button(self.root, text="Send", command=self.button_click)
        self.send_button.pack(side='left', fill='x', expand=True)

        self.image_button = tk.Button(self.root, text='Browse', command=self.select_image)
        self.image_button.pack(side='left', fill='x', expand=True)
           
    def select_image(self):
        self.imagepath = filedialog.askopenfilename()
        self.text_entry.delete(0, 'end')
        self.text_entry.insert(0, self.imagepath)

    async def update(self, interval = 0.05):
        while True:
            self.root.update()
            await asyncio.sleep(interval)

    def button_click(self):
        asyncio.create_task(self.send_message())
        
    async def send_message(self):
        if self.imagepath != None:
            tmp = self.imagepath
            self.imagepath = None
            await self.client.send_image(tmp)
            
        else:
            message = self.text_entry.get()
            await self.client.send_message(message)
        
    async def receive_message(self, message: str):
        self.text_widget.insert("end", message + '\n')
        self.text_entry.delete(0, "end")
 
async def main():
    my_client = client()
    my_des = Gui(my_client)
    my_client.gui = my_des
    tasks = [
        asyncio.create_task(my_client.start_client()),
        asyncio.create_task(my_des.update())
    ]
    
    await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(main())