#!/usr/bin/env python3
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from datetime import datetime
from os import environ
from time import time
from requests import get
from discord.ext import tasks
import discord

#####################
# Bot Configuration #
#####################
# Setting environment variables is preferred, but you can also edit the variables below.

# Discord (Required)
TZ_DISCORD_TOKEN = environ.get('TZ_DISCORD_TOKEN')
TZ_DISCORD_CHANNEL_ID = int(environ.get('TZ_DISCORD_CHANNEL_ID', 0))

# D2RuneWizard API (Required)
TZ_D2RW_TOKEN = environ.get('TZ_D2RW_TOKEN')

########################
# End of configuration #
########################
__version__ = '0.1'

# TZ_DISCORD_TOKEN and TZ_DISCORD_CHANNEL_ID are required
if not TZ_DISCORD_TOKEN or TZ_DISCORD_CHANNEL_ID == 0:
    print('Please set TZ_DISCORD_TOKEN and TZ_DISCORD_CHANNEL_ID in your environment.')
    exit(1)

#GET https://d2runewizard.com/api/terror-zone

class Diablo2IOClient():
    """
    Interacts with the diablo2.io dclone API. Tracks the current progress and recent reports for each mode.
    """
    def status(self, zone=''):
        """
        Get the currently reported TZ status from the D2RW TZ API.

        API documentation: https://d2runewizard.com/integration
        """
        try:
            url = 'https://d2runewizard.com/api/terror-zone'
            params = {'zone': zone}
            #headers = {'User-Agent': f'dclone-discord/{__version__}'}
            response = get(url, params=params, timeout=10)

            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f'[D2RW.status] API Error: {err}')
            return None

    def progress_message(self):
        """
        Returns a formatted message of the current dclone status by mode (region, ladder, hardcore).
        """
        # get the currently reported TZ status
        # TODO: return from current_progress instead of querying the API every time?

        # build the message
        message = 'Current TZ Progress:\n'
        for data in status:
            zone = data.get('zone')

            message += f' - **{ZONE[zone]}**\n'
        message += '> Data courtesy of D2RW'

class DiscordClient(discord.Client):
    """
    Connects to Discord and starts a background task that checks the diablo2.io dclone API every 60 seconds.
    When a progress change occurs that is greater than or equal to DCLONE_THRESHOLD and for more than DCLONE_REPORTS
    consecutive updates, the bot will send a message to the configured DCLONE_DISCORD_CHANNEL_ID.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # DCLONE_D2RW_TOKEN is required for planned walk notifications
        if not TZ_D2RW_TOKEN:
            print('WARNING: TZ_D2RW_TOKEN is not set, you will not receive Terror Zone notifications.')

    async def on_ready(self):
        """
        Runs when the bot is connected to Discord and ready to receive messages. This starts our background task.
        """
        # pylint: disable=no-member
        print(f'Bot logged into Discord as "{self.user}"')
        servers = sorted([g.name for g in self.guilds])
        print(f'Connected to {len(servers)} servers: {", ".join(servers)}')

        # channel details
        channel = self.get_channel(TZ_DISCORD_CHANNEL_ID)
        if not channel:
            print('ERROR: Unable to access channel, please check TZ_DISCORD_CHANNEL_ID')
            await self.close()
            return
        print(f'Messages will be sent to #{channel.name} on the {channel.guild.name} server')

        # start the background task to monitor TZ status
        try:
            self.check_dclone_status.start()
        except RuntimeError as err:
            print(f'Background Task Error: {err}')

    async def on_message(self, message):
        """
        This is called any time the bot receives a message. It implements the dclone chatop.
        """
        if message.content.startswith('.tz') or message.content.startswith('!tz'):
            print(f'Responding to TZ chatop from {message.author}')
            current_status = self.tz.progress_message()

            channel = self.get_channel(message.channel.id)
            await channel.send(current_status)

if __name__ == '__main__':
    client = DiscordClient(intents=discord.Intents.default())
    client.run(TZ_DISCORD_TOKEN)
