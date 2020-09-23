from bluetooth import *
from PyOBEX.client import Client
import sys
import logging
logging.basicConfig(level = logging.INFO)

class BT:
    def __init__(self, duration = 8):
        self.duration = duration
        self.nearby_devices = discover_devices(duration = self.duration, lookup_names = True)
        self.client = None
    
    def refresh(self):
        logging.info('Please wait, upddating the list of nearby devices...')
        self.nearby_devices = discover_devices(duration = self.duration, lookup_names = True)

    def get_nearby_devices(self):
        return self.nearby_devices

    def connect(self):
        self.refresh()
        print('Sr.\tAddress \t\tName')
        for i in range(len(self.nearby_devices)):
            print(f'{i + 1}.\t{self.nearby_devices[i][0]}\t{self.nearby_devices[i][1]}')
        addr = self.nearby_devices[int(input('\nEnter the number of the device, to which you wish to connect : ')) - 1][0]
        service = find_service(name = b'OBEX Object Push\x00', address = addr)[0]
        logging.info(f'Connecting to {service["host"]} on port {service["port"]}...')
        self.client = Client(service["host"], service["port"])
        self.client.connect()
        logging.info('Connection success.')
        
    def disconnect(self):
        logging.info(f'Disconnecting from : {self.client.address}...')
        self.client.disconnect()
        self.client = None
        logging.info('Disconnected successfully.')
        
    def send_file(self, file_name, binary_data = None):
        self.connect()
        logging.info('Sending the file now...')
        if binary_data is None:
            with open(file_name, 'rb') as f:
                contents = f.read()
            self.client.put(file_name, contents)
        else:
            self.client.put(file_name, binary_data)
        logging.info('File has been sent successfully.')
        self.disconnect()
        
if __name__ == "__main__":
    bt_client = BT()
    bt_client.send_file('art.png')
