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
from os import environ
from requests import get
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

# TZ_DISCORD_TOKEN, TZ_D2RW_TOKEN, and TZ_DISCORD_CHANNEL_ID are required
if not TZ_DISCORD_TOKEN or not TZ_D2RW_TOKEN or TZ_DISCORD_CHANNEL_ID == 0:
    print('Please set TZ_DISCORD_TOKEN, TZ_D2RW_TOKEN, and TZ_DISCORD_CHANNEL_ID in your environment.')
    exit(1)


class D2RuneWizardClient():
    """
    Interacts with the d2runewizard.com terror zone API.
    """
    @staticmethod
    def terror_zone():
        """
        Get the currently reported TZ status from the D2RW TZ API.

        API documentation: https://d2runewizard.com/integration#terror-zone-tracker
        """
        try:
            url = 'https://d2runewizard.com/api/terror-zone'
            params = {'token': TZ_D2RW_TOKEN}
            # headers = {'User-Agent': f'dclone-discord/{__version__}'}
            response = get(url, params=params, timeout=10)

            response.raise_for_status()
            return response.json()
        except Exception as err:
            print(f'[D2RW.terror_zone] API Error: {err}')
            return None

    @staticmethod
    def terror_zone_message():
        """
        Returns a formatted message of the current terror zone status.
        """
        # get the currently reported TZ status
        tz_status = D2RuneWizardClient.terror_zone()

        # build the message
        message = 'Current Terror Zone:\n'
        message += f'Zone: **{tz_status.get("terrorZone").get("zone")}** ({tz_status.get("terrorZone").get("act")})\n'
        message += '> Data courtesy of D2RW'

        return message


class DiscordClient(discord.Client):
    """
    Connects to Discord and watches for the `.tz` or `!tz` command to report the current Terror Zone status.
    """
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

    async def on_message(self, message):
        """
        This is called any time the bot receives a message. It implements the tz chatop.
        """
        if message.content.startswith('.tz') or message.content.startswith('!tz'):
            print(f'Responding to TZ chatop from {message.author}')
            current_status = D2RuneWizardClient.terror_zone_message()

            channel = self.get_channel(message.channel.id)
            await channel.send(current_status)


if __name__ == '__main__':
    client = DiscordClient(intents=discord.Intents.default())
    client.run(TZ_DISCORD_TOKEN)
