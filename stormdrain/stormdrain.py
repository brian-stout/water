#!/usr/local/bin/python3.5

import socket

from header import Header
from liquid import Liquid


incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

incoming.bind(('', 1111))

incoming.listen(10)

while True:
    (client, addr) = incoming.accept()

    header = Header(client.recv(8))

    print("Receiving {} bytes from {}".format(header.size, addr))
    print("/t type: {})".format(header.type))

    buf = client.recv(header.size - 8)
    while len(buf) < header.size - 8:
        buf += client.recv(header.size - 8 - len(buf))

    liquid = Liquid(buf)

    if liquid.detect_trash() == True:
        print("Trash detected.")
        liquid.deair()
        trash_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        trash_outgoing.connect(("downstream", 2222))
        header.type = 1
        header.size = 8 + 8*len(liquid.data)
        trash_outgoing.send(header.serialize())
        trash_outgoing.send(liquid.serialize_water())
        trash_outgoing.close()
    else:
        print("Regular water detected.")
        sewage_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sewage_outgoing.connect(("treatment", 1111))
        header.type = 0
        header.size = 8 + 8*len(liquid.data)
        sewage_outgoing.send(header.serialize())
        sewage_outgoing.send(liquid.serialize_water())
        sewage_outgoing.close()

    client.close()

