#!/usr/local/bin/python

import struct

def is_undu(number):
    last_digit = 0
    flip_bool = False
    string = str(number)

    if len(string) == 1:
        return True
    if len(string) >= 2:
        if string[0] == string[1]:
            return False
        elif string[0] > string[1]:
            flip_bool = False
        elif string[0] < string[1]:
            flip_bool = True

    #Change to check for failures instead of successes to avoid flip booleans
    for i in range(len(string)-1):
        if flip_bool == False:
            if int(string[i]) <= int(string[i+1]):
                return False
            else:
                flip_bool = True
        else:
            if int(string[i]) >= int(string[i+1]):
                return False
            else:
                flip_bool = False

    return True

#https://stackoverflow.com/a/18833845
def is_prime(n):
    '''check if integer n is a prime'''

    # make sure n is a positive integer
    n = abs(int(n))

    # 0 and 1 are not primes
    if n < 2:
        return False

    # 2 is the only even prime number
    if n == 2: 
        return True    

    # all other even numbers are not primes
    if not n & 1: 
        return False

    # range starts with 3 and only needs to go up 
    # the square root of n for all odd numbers
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True

class Node:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

class Liquid:
    def __init__(self, blob):
        self.slots = len(blob)//8
        raw_data = struct.unpack("!" + "LHH"*self.slots, blob)
 
        self.hazmats = set()
        self.sludge_mat = dict()

        self.data = {i//3+1: list(raw_data[i:i+3]) for i in
                range(0, len(raw_data), 3) if raw_data[i]}

    def treat_se(self):
        '''Circularly-linked list'''
        heads = set(self.data.keys())
        for k,v in self.data.items():
            heads.discard(v[2])
            heads.discard(v[1])

        if len(heads) < 1:
            to_remove = max(d[0] for d in self.data.values())
            self.hazmats.add(to_remove)

            for i in self.data:
                if self.data[i][0] == to_remove:
                    break
            del self.data[i]
            for n in self.data:
                if self.data[n][1] == i:
                    self.data[n][1] = 0
                if self.data[n][2] == i:
                    self.data[n][2] = 0


    def treat_pb(self):
        pass

    def treat_hg(self):
        '''Multiple roots in graph'''
        heads = set(self.data.keys())
        for k,v in self.data.items():
            heads.discard(v[1])
            heads.discard(v[2])

        if len(heads) > 1:
            to_remove = min((self.data[i][0] for i in heads))
            self.hazmats.add(to_remove)

            for i in self.data:
                if self.data[i][0] == to_remove:
                    break

            del self.data[i]
            self.treat_hg()

    def serialize_water(self):
        for n in range(self.slots):
            n += 1
            if n not in self.data:
                self.data[n] = (0,0,0)

        array = (x for n in range(self.slots) for x in self.data[n+1])
        return struct.pack("!" + "LHH"*len(self.data), *array)

    def serialize_hazmat(self):
        array = (x for val in self.hazmats for x in (val,0))
        return struct.pack("!" + "LL"*len(self.hazmats), *array)

    def detect_trash(self):
        ret_bool = False

        for key in self.data:
            if self.data[key][1] not in self.data:
                ret_bool = True
                self.data[key][1] = 0xFFFF
            if self.data[key][2] not in self.data:
                ret_bool = True
                self.data[key][2] = 0xFFFF

        return ret_bool

    def deair(self):
        temp_list = []
        for key in self.data:
            if self.data[key][0] == 0:
                temp_list.append(key)

        for key in temp_list:
            self.data.pop(key, None)

    def treat_ammonia(self):
        temp_list = []
        for key in self.data:
            if is_undu(self.data[key][0]) == True:
                temp_list.append(key)
                self.sludge_mat[key] = self.data[key]

        for key in temp_list:
            print("Removing Ammonia")
            self.data.pop(key, None)

    def treat_feces(self):
        temp_list = []
        for key in self.data:
            if is_prime(self.data[key][0]) == True:
                temp_list.append(key)
                self.sludge_mat[key] = self.data[key]

        for key in temp_list:
            print("Removing Ammonia")
            self.data.pop(key, None)
