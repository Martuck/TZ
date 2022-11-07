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
from discord.ext import tasks
import discord

##################
# Bot Dictionary #
##################
tzdict = {'Blood Moor and Den of Evil': '1033399859039973457', 'Cold Plains and The Cave': '1033400167900123226', 'Burial Grounds, The Crypt, and the Mausoleum': '1033400209704755210', 'Stony Field': '1033400326205735014', 'Dark Wood': '1033400366630441060', 'The Forgotten Tower': '1033400469634170922', 'Jail': '1033400502798516355', 'Cathedral and Catacombs': '1033400591436754954', 'The Pit': '1033400658008735775', 'Tristram': '1033400671493423126', 'Moo Moo Farm': '1033400750656729088', 'Sewers': '1033400906227654829', 'Rocky Waste and Stony Tomb': '1033400908308041870', 'Dry Hills and Halls of the Dead': '1033400910669426828', 'Far Oasis': '1033400912795943003', 'Lost City, Valley of Snakes, and Claw Viper Temple': '1033400914867933244', 'Arcane Sanctuary': '1033400916650491915', "Tal Rasha's Tombs": "1033400918974152904", 'Spider Forest and Spider Cavern': '1033401329814601748', 'Flayer Jungle and Flayer Dungeon': '1033401331848859758', 'Kurast Bazaar, Ruined Temple, and Disused Fane': '1033401333912436767', 'Kurast Sewers': '1033401336399679498', 'Travincal': '1033401338425528383', 'Durance of Hate': '1033401340682055680', 'Outer Steppes and Plains of Despair': '1033401688201101402', 'River of Flame and City of the Damned': '1033401690436665425', 'Chaos Sanctuary': '1033401692491874334', 'Bloody Foothills': '1033401900269326396', 'Frigid Highlands': '1033401902186119259', 'Glacial Trail': '1033401904371335168', 'Crystalline Passage and Frozen River': '1033401906736922624', 'Arreat Plateau': '1033401910767669308', "Nihlathak's Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught": "1033401913309417583", "Ancient's Way and Icy Cellar": "1033401915377188935", 'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': '1033401917591781527'}

#####################
# End of Dictionary #
#####################

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
    Interacts with the d2runewizard.com terror zone API and tracks the current terror zone.
    """
    def __init__(self):
        # tracks the current terror zone
        self.current_terror_zone = None

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
        zone = tz_status.get("terrorZone").get("zone")
        pingid = tzdict.get(zone)

        # build the message
        message = 'Current Terror Zone:\n'
        message += f'Zone: **{tz_status.get("terrorZone").get("zone")}** ({tz_status.get("terrorZone").get("act")}) <@&{pingid}>\n'
        message += '> Data courtesy of D2RW'

        return message


class DiscordClient(discord.Client):
    """
    Connects to Discord and watches for the `.tz` or `!tz` command to report the current Terror Zone status.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.d2rw = D2RuneWizardClient()

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

        # start the background task to monitor the current terror zone
        try:
            self.check_terror_zone.start()
        except RuntimeError as err:
            print(f'Background Task Error: {err}')

    async def on_message(self, message):
        """
        This is called any time the bot receives a message. It implements the tz chatop.
        """
        if message.content.startswith('.tz') or message.content.startswith('!tz'):
            print(f'Responding to TZ chatop from {message.author}')
            current_status = D2RuneWizardClient.terror_zone_message()

            channel = self.get_channel(message.channel.id)
            await channel.send(current_status)

    @tasks.loop(seconds=60)
    async def check_terror_zone(self):
        """
        Background task that checks the current terror zone via the d2runewizard.com API every 60 seconds.
        If the current status is different from the last known status, a message is sent to Discord.
        """
        # print('>> Checking Terror Zone status...')
        terror_zone = self.d2rw.terror_zone().get('terrorZone').get('zone')

        # if the terror zone changed since the last check, send a message to Discord
        if terror_zone != self.d2rw.current_terror_zone:
            print(f'Terror Zone changed from {self.d2rw.current_terror_zone} to {terror_zone}')
            tz_message = D2RuneWizardClient.terror_zone_message()

            channel = self.get_channel(TZ_DISCORD_CHANNEL_ID)
            await channel.send(tz_message)

            # update the current terror zone
            self.d2rw.current_terror_zone = terror_zone

    @check_terror_zone.before_loop
    async def before_check_terror_zone(self):
        """
        Runs before the background task starts. This waits for the bot to connect to Discord and sets the initial terror zone status.
        """
        await self.wait_until_ready()  # wait until the bot logs in

        # get the current terror zone
        try:
            terror_zone = self.d2rw.terror_zone().get('terrorZone').get('zone')
        except Exception as err:
            print(f'Unable to set the current terror zone at startup: {err}')
            return

        # set the current terror zone
        # this prevents a duplicate message from being sent when the bot starts
        # comment this out if you want the bot to post the current terror zone when it starts
        self.d2rw.current_terror_zone = terror_zone
        print(f'Initial Terror Zone is {terror_zone}')


if __name__ == '__main__':
    client = DiscordClient(intents=discord.Intents.default())
    client.run(TZ_DISCORD_TOKEN)
