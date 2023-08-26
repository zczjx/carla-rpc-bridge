#!/usr/bin/env python3
import msgpackrpc

class SumServer(object):
    def get_rig(self):
        print('server: get_rig')
        return {"xres": 1920, "yres": 1080, "data": [0x55, 0xaa, 0x99, 0x88]}
    def push_data(self, data=[]):
        print(data)

if __name__ == '__main__':
    server = msgpackrpc.Server(SumServer())
    server.listen(msgpackrpc.Address("localhost", 18800))
    server.start()