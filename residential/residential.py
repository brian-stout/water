#!/usr/local/bin/python3.5

import socket

from header import Header
from liquid import Liquid


incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

incoming.bind(('', 1112))

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
    liquid.treat_ammonia()
    liquid.treat_feces()

    #Change later to make a report
    """
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
    """
    if liquid.sludge_mat:
        print("Material collected to be sludged")
        """
        sludge_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sludge_outgoing.connect(("treatment", 4444))
        header.type = 2
        header.size = 8 + 8*len(liquid.data)
        sludge_outgoing.send(header.serialize())
        sluder_outgoing.send(liquid.serialize_water())
        sewage_outgoing.close()
        """

    print("Regular water detected.")
    sewage_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """
    sewage_outgoing.connect(("treatment", 1111))
    header.type = 0
    header.size = 8 + 8*len(liquid.data)
    sewage_outgoing.send(header.serialize())
    sewage_outgoing.send(liquid.serialize_water())
    sewage_outgoing.close()
    """

    client.close()
