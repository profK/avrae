#!/usr/bin/env python

# WS server example

import asyncio
import websockets
import random
import time

_TIMEOUTSEC=120  #timeout of key from issue in seconds


_connectionKeys={}
_connectionKeyTimeout={}
_websockets={}

DiscordClient=None

random.seed()

#Get a time limtied connection key for the passed in user
#UserID is the id of the associated user
def GetConnectionKey(userID):
    newKey=random.randint(100000,999999)
    _connectionKeys[newKey]= userID
    _connectionKeyTimeout[newKey]= time.time()+_TIMEOUTSEC
    return newKey

#check if key is assigned to a user and not expire
def IsKeyValid(key):
    if not key in _connectionKeys :
        return False
    if _connectionKeyTimeout[key]<time.time():
        return False
    return True

#return the user to whom a valid key has been assigned
def GetUserIDByKey(key):
    return _connectionKeys[key]


async def connect(websocket, path):
    key = int(await websocket.recv())
    if not IsKeyValid(key):
        await websocket.send('INVALID KEY')
        websocket.close()
        return
    userid= GetUserIDByKey(key)
    _websockets[userid]=websocket
    await websocket.send('CONNECTED')
    while websocket.open:
        message=await websocket.recv()




    await websocket.send(greeting)
    print(f"> {greeting}")


#asyncio.get_event_loop().run_forever()
