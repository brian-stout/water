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

    print("Receiving {} bytes from {} \t type: {}".format(header.size, addr, header.type))

    buf = client.recv(header.size - 8)
    while len(buf) < header.size - 8:
        buf += client.recv(header.size - 8 - len(buf))

    liquid = Liquid(buf)

    #Change later to make a report
    if liquid.detect_trash() == True:
        print("Trash detected.")
        liquid.deair()
        trash_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        trash_outgoing.connect(("downstream", 2222))
        header.type = 1
        header.size = 8 + 8*len(liquid.data)
        trash_sent_times += 1
        trash_sent_ammount += len(liquid.data)
        trash_outgoing.send(header.serialize())
        trash_outgoing.send(liquid.serialize_water())
        trash_outgoing.close()
        continue

    liquid.treat_ammonia()
    liquid.treat_feces()

    if liquid.sludge_mats:
        print("Material collected to be sludged")
        sludge_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sludge_outgoing.connect(("treatment", 4444))
        header.type = 0
        header.size = 8 + 8*len(liquid.sludge_mats)
        print("Sending  sludge data " + str(header.size) + " to downstream")
        sludge_sent_times += 1
        sludge_sent_ammount += len(liquid.sludge_mats)


        sludge_outgoing.send(header.serialize())
        sludge_outgoing.send(liquid.serialize_sludge())
        sludge_outgoing.close()

    if liquid.data:
        print("Regular water detected.")
        sewage_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sewage_outgoing.connect(("pretreatment", 1111))
        header.type = 0
        header.size = 8 + 8*len(liquid.data)

        water_sent_times += 1
        water_sent_ammount += len(liquid.data)

        sewage_outgoing.send(header.serialize())
        sewage_outgoing.send(liquid.serialize_water())
        sewage_outgoing.close()

    print("trash_sent_times: " + str(trash_sent_times))
    print("trash_sent_ammount: " + str(trash_sent_ammount))
    print("sludge_sent_times: " + str(trash_sent_times))
    print("sludge_sent_ammount: " + str(trash_sent_ammount))
    print("sewage_sent_ammount: " + str(water_sent_times))
    print("sewage_sent_ammount: " + str(water_sent_ammount))

    client.close()

