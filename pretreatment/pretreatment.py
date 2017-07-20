#!/usr/local/bin/python3.5

import socket

from header import Header
from liquid import Liquid


incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

incoming.bind(('', 1111))

incoming.listen(20)

while True:
    (client, addr) = incoming.accept()

    header = Header(client.recv(8))
    print("Receiving {} bytes from {}".format(header.size, addr))
    packet_stage = header.custom
    

    buf = client.recv(header.size - 8)
    while len(buf) < header.size - 8:
        buf += client.recv(header.size - 8 - len(buf))

    liquid = Liquid(buf)

    #Change later to make a report

    if header.custom < 1:
        if liquid.detect_trash() == True and header.custom < 1:
            print("Trash detected.")
            liquid.deair()
            trash_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            trash_outgoing.connect(("downstream", 2222))
            header.type = 1
            header.custom = 1
            header.size = 8 + 8*len(liquid.data)
            trash_outgoing.send(header.serialize())
            trash_outgoing.send(liquid.serialize_water())
            trash_outgoing.close()
            continue
        else:
            header.custom = 1

    prev_hazmats = 0
    liquid.treat_hg()
    print("Found {} after mercury".format(len(liquid.hazmats)))
    prev_hazmats = len(liquid.hazmats)
    liquid.treat_pb()
    print("Found {} after lead".format(len(liquid.hazmats) - prev_hazmats))
    prev_hazmats = len(liquid.hazmats)
    liquid.treat_se()
    print("Found {} after selenium".format(len(liquid.hazmats) - prev_hazmats))

    print("Found {} hazardous contaminants from {}".format(len(liquid.hazmats),
        addr))

    if liquid.hazmats:
        hazmat_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hazmat_outgoing.connect(("downstream", 8888))
        header.type = 4
        header.size = 8 + 8*len(liquid.hazmats)
        hazmat_outgoing.send(header.serialize())
        hazmat_outgoing.send(liquid.serialize_hazmat())
        hazmat_outgoing.close()

    if liquid.data:
        sewage_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sewage_outgoing.connect(("treatment", 1111))
        header.type = 0
        header.size = 8 + 8*len(liquid.data)
        sewage_outgoing.send(header.serialize())
        sewage_outgoing.send(liquid.serialize_water())
        sewage_outgoing.close()

    client.close()

