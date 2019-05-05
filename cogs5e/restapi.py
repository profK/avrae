import random
import discord
import websockets
import asyncio
import time
from discord.ext import commands

_TIMEOUTSEC=120  #timeout of key from issue in seconds
_connectionKeys={}
_connectionKeyTimeout={}
_websockets={}
_bot=None


def GetConnectionKey(userID):
    newKey = random.randint(100000, 999999)
    _connectionKeys[newKey] = userID
    _connectionKeyTimeout[newKey] = time.time() + _TIMEOUTSEC
    return newKey

    # check if key is assigned to a user and not expire


def IsKeyValid(key):
    if not key in _connectionKeys:
        return False
    if _connectionKeyTimeout[key] < time.time():
        return False
    return True

    # return the user to whom a valid key has been assigned


def GetUserIDByKey(key):
    return _connectionKeys[key]

class RESTapi:


    random.seed()

    # Get a time limtied connection key for the passed in user
    # UserID is the id of the associated user


    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='connect', aliases=['cnct'])
    async def connectCmd(self, ctx ):
        """returns a time limited connection key for the requesting user"""
        userid = ctx.author
        key = GetConnectionKey(userid)
        await ctx.send('CONNECTION KEY: '+str(key))

async def connect(websocket, path):
        key = int(await websocket.recv())
        if not IsKeyValid(key):
            await websocket.send('INVALID KEY')
            websocket.close()
            return
        userid = GetUserIDByKey(key)
        _websockets[userid] = websocket
        await websocket.send('CONNECTED')
        while websocket.open:
            text = await websocket.recv()
            _bot.process_commands(discord.message({'author':userid,'content':text}))
        return

def setup(bot):
    _bot=bot
    bot.add_cog(RESTapi(bot))
    start_server = websockets.serve(connect, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)