#!/usr/bin/env python3
import msgpackrpc

if __name__ == '__main__':
    client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
    result = client.call('get_rig')
    print(type(result))
    print(result)
    client.call('push_data', [4, 9 ,2, 8, 7])