import random
import RESTInterface
import re

import discord
from discord.ext import commands

from cogs5e.funcs import scripting
from cogs5e.funcs.dice import roll
from cogs5e.funcs.lookupFuncs import select_monster_full
from cogs5e.funcs.sheetFuncs import sheet_attack
from cogs5e.models import embeds
from cogs5e.models.monster import Monster, SKILL_MAP
from utils.argparser import argparse
from utils.functions import fuzzy_search, a_or_an, verbose_stat, camel_to_title


class RESTapi:
    """Dice and math related commands."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='connect', aliases=['cnct'])
    async def connectCmd(self, ctx ):
        """returns a time limited connection key for the requesting user"""
        userid = ctx.author
        key = RESTInterface.GetConnectionKey(userid)
        await ctx.send('CONNECTION KEY: '+str(key))


def setup(bot):
    bot.add_cog(RESTapi(bot))