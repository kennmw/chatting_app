"""Server for multithreaded cht application """
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging
# Create a logger
logger = logging.getLogger("Server")
logger.setLevel(logging.DEBUG)


# create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(filename='file.log')


# CREATE FORMATTER AND ADD IT TO HANDLERS

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s, %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# add handlers to the logger

logger.addHandler(c_handler)
logger.addHandler(f_handler)

clients = {}
addresses = {}
host = ''
port = 1230
buffer_size = 1024
addr = (host, port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)
server.listen(4)

def accept_incoming_connection():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = server.accept()
        # print("%s:%s has connected." % client_address)
        logger.info("%s:%s has connected." % client_address)
        client.send(bytes("Server Greetings" + " \nNow type your name and press enter \n", 'utf-8'))
        addresses[client] = client_address
        logger.info(f"Client{client_address} added to client list")
        Thread(target=handle_client, args=(client,)).start()
        logger.info(f"{client_address}'s Thread has been started")


def handle_client(client):
    """Takes client socket as argument"""
    """Handles a single client connection"""
    name = client.recv(buffer_size).decode('utf-8')
    logger.info(f"First client name is {name.strip()}")
    # logger.info("%s:  has connected." % name)
    welcome = f'Welcome {name.strip()} Type quit to exit.\n'
    client.send(bytes(welcome, 'utf-8'))
    msg = "%s has joined the chat !\n" % name.strip()
    broadcast(bytes(msg, 'utf-8'))
    clients[client] = name
    while True:
        msg = client.recv(buffer_size)
        if msg != bytes("quit", 'utf-8'):
            logger.info(f"Message broadcast : {msg}")
            broadcast(msg, name.strip() + ": ")

        else:
            client.send(bytes("{quit}", 'utf-8'))
            client.close()
            del clients[client]
            logger.info("%s has left the chat ." % name.strip())
            broadcast(bytes("%s has left the chat ." % name.strip(), 'utf-8'))
            break


def broadcast(msg, prefix=""):
    # prefix is for name identification
    """Broadcasts a message to all the clients"""
    for sock in clients:
        sock.send(bytes(prefix, 'utf-8') + msg)


if __name__ == '__main__':
    server.listen(5)
    logger.info("Server started, Waiting for clients [ + ]..")
    # print("Waiting for connection...")
    accept_thread = Thread(target=accept_incoming_connection)
    accept_thread.start()
    accept_thread.join()
    server.close()
