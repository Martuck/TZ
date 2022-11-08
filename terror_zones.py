#!/usr/bin/env python3
"""
A Discord Bot for tracking Terror Zones in Diablo 2: Resurrected
Copyright (C) 2022 @Synse, @Martuck

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
tzdict = {
    'Ancient\'s Way and Icy Cellar': '1033401915377188935',
    'Arcane Sanctuary': '1033400916650491915',
    'Arreat Plateau': '1033401910767669308',
    'Blood Moor and Den of Evil': '1033399859039973457',
    'Bloody Foothills': '1033401900269326396',
    'Burial Grounds, The Crypt, and The Mausoleum': '1033400209704755210',
    'Cathedral and Catacombs': '1033400591436754954',
    'Chaos Sanctuary': '1033401692491874334',
    'Cold Plains and The Cave': '1033400167900123226',
    'Crystalline Passage and Frozen River': '1033401906736922624',
    'Dark Wood': '1033400366630441060',
    'Dry Hills and Halls of the Dead': '1033400910669426828',
    'Durance of Hate': '1033401340682055680',
    'Far Oasis': '1033400912795943003',
    'Flayer Jungle and Flayer Dungeon': '1033401331848859758',
    'Frigid Highlands': '1033401902186119259',
    'Glacial Trail': '1033401904371335168',
    'Jail': '1033400502798516355',
    'Kurast Bazaar, Ruined Temple, and Disused Fane': '1033401333912436767',
    'Kurast Sewers': '1033401336399679498',
    'Lost City, Valley of Snakes, and Claw Viper Temple': '1033400914867933244',
    'Moo Moo Farm': '1033400750656729088',
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': '1033401913309417583',
    'Outer Steppes and Plains of Despair': '1033401688201101402',
    'River of Flame and City of the Damned': '1033401690436665425',
    'Rocky Waste and Stony Tomb': '1033400908308041870',
    'Sewers': '1033400906227654829',
    'Spider Forest and Spider Cavern': '1033401329814601748',
    'Stony Field': '1033400326205735014',
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': '1033400918974152904',
    'The Forgotten Tower': '1033400469634170922',
    'The Pit': '1033400658008735775',
    'Travincal': '1033401338425528383',
    'Tristram': '1033400671493423126',
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': '1033401917591781527'
}

bpdict = {
    'Ancient\'s Way and Icy Cellar': '6-8',
    'Arcane Sanctuary': '7-9',
    'Arreat Plateau': '9-11',
    'Blood Moor and Den of Evil': '7-9',
    'Bloody Foothills': '4-6',
    'Burial Grounds, The Crypt, and The Mausoleum': '8-10',
    'Cathedral and Catacombs': '27-35',
    'Chaos Sanctuary': '6-7',
    'Cold Plains and The Cave': '13-16',
    'Crystalline Passage and Frozen River': '13-17',
    'Dark Wood': '7-9',
    'Dry Hills and Halls of the Dead': '20-27',
    'Durance of Hate': '15-21',
    'Far Oasis': '7-9',
    'Flayer Jungle and Flayer Dungeon': '22-29',
    'Frigid Highlands': '9-11',
    'Glacial Trail': '7-9',
    'Jail': '18-24',
    'Kurast Bazaar, Ruined Temple, and Disused Fane': '15-17',
    'Kurast Sewers': '12-14',
    'Lost City, Valley of Snakes, and Claw Viper Temple': '21-28',
    'Moo Moo Farm': '6-8',
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': '12-14',
    'Outer Steppes and Plains of Despair': '16-20',
    'River of Flame and City of the Damned': '14-17',
    'Rocky Waste and Stony Tomb': '17-23',
    'Sewers': '18-24',
    'Spider Forest and Spider Cavern': '14-20',
    'Stony Field': '7-9',
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': '49-63',
    'The Forgotten Tower': '15-20',
    'The Pit': '8-11',
    'Travincal': '6-8',
    'Tristram': '5-6',
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': '22-29'
}

sudict = {
    'Ancient\'s Way and Icy Cellar': 'Snapchip Shatter',
    'Arcane Sanctuary': 'The Summoner',
    'Arreat Plateau': 'Thresh Socket',
    'Blood Moor and Den of Evil': 'Corpsefire',
    'Bloody Foothills': 'Dac Farren and Shenk The Overseer',
    'Burial Grounds, The Crypt, and The Mausoleum': 'Blood Raven and Bonebreaker',
    'Cathedral and Catacombs': 'Bone Ash and Andariel',
    'Chaos Sanctuary': 'Grand Vizier of Chaos, Infector of Souls, Lord De Seis, and Diablo',
    'Cold Plains and The Cave': 'Bishibosh and Coldcrow',
    'Crystalline Passage and Frozen River': 'Frozenstein',
    'Dark Wood': 'Treehead Woodfist',
    'Dry Hills and Halls of the Dead': 'Bloodwitch the Wild',
    'Durance of Hate': 'Wyand Voidbringer, Maffer Dragonhand, Bremm Sparkfist, and Mephisto',
    'Far Oasis': 'Beetleburst',
    'Flayer Jungle and Flayer Dungeon': 'Stormtree and Witch Doctor Endugu',
    'Frigid Highlands': 'Eldritch the Rectifier, Sharptooth Slayer, and Eyeback the Unleashed',
    'Glacial Trail': 'Bonesaw Breaker',
    'Jail': 'Pitspawn Fouldog',
    'Kurast Bazaar, Ruined Temple, and Disused Fane': 'Battlemaid Sarina',
    'Kurast Sewers': 'Icehawk Riftwing',
    'Lost City, Valley of Snakes, and Claw Viper Temple': 'Dark Elder and Fangskin',
    'Moo Moo Farm': 'The Cow King',
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': 'Pindleskin and Nihlathak',
    'Outer Steppes and Plains of Despair': 'Izual',
    'River of Flame and City of the Damned': 'Hephasto The Armorer',
    'Rocky Waste and Stony Tomb': 'Creeping Feature',
    'Sewers': 'Radament',
    'Spider Forest and Spider Cavern': 'Sszark The Burning',
    'Stony Field': 'Rakanishu',
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': 'Ancient Kaa The Soulless and Duriel',
    'The Forgotten Tower': 'The Countess',
    'The Pit': 'None',
    'Travincal': 'Ismail Vilehand, Toorc Icefist, and Geleb Flamefinger',
    'Tristram': 'Griswold',
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': 'Colenzo The Annihilator, Achmel The Cursed, Bartuc The Bloody, Ventar The Unholy, Lister The Tormentor, and Baal'
}

imdict = {
    'Ancient\'s Way and Icy Cellar': 'Cold, Lightning, Poison, and Physical',
    'Arcane Sanctuary': 'Cold, Fire, Lightning, Poison, and Physical',
    'Arreat Plateau': 'Cold, Fire, Lightning, and Poison',
    'Blood Moor and Den of Evil': 'Cold and Fire',
    'Bloody Foothills': 'Cold, Fire, Lightning, and Poison',
    'Burial Grounds, The Crypt, and The Mausoleum': 'Lightning',
    'Cathedral and Catacombs': 'Cold, Fire, Lightning, and Physical',
    'Chaos Sanctuary': 'Cold, Fire, and Lightning',
    'Cold Plains and The Cave': 'Cold, Fire, and Lightning',
    'Crystalline Passage and Frozen River': 'Cold, Fire, Lightning, Poison, Physical, and Magic',
    'Dark Wood': 'Cold, Fire, and Poison',
    'Dry Hills and Halls of the Dead': 'Cold, Fire, Lightning, and Poison',
    'Durance of Hate': 'Cold, Fire, Lightning, and Poison',
    'Far Oasis': 'Lightning, Poison, and Physical',
    'Flayer Jungle and Flayer Dungeon': 'Cold, Fire, Lightning, Poison, Physical, and Magic',
    'Frigid Highlands': 'Cold, Fire, Lightning, Poison, Physical, and Magic',
    'Glacial Trail': 'Cold, Fire, Lightning, Poison, and Physical',
    'Jail': 'Cold, Fire, Poison, and Physical',
    'Kurast Bazaar, Ruined Temple, and Disused Fane': 'Cold, Fire, Lightning, Poison, Physical, and Magic',
    'Kurast Sewers': 'Cold, Lightning, Poison, and Magic',
    'Lost City, Valley of Snakes, and Claw Viper Temple': 'Cold, Fire, Lightning, Poison, and Magic',
    'Moo Moo Farm': 'None',
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': 'Cold, Fire, Lightning, Poison, Physical, and Magic',
    'Outer Steppes and Plains of Despair': 'Cold, Fire, Lightning, and Poison',
    'River of Flame and City of the Damned': 'Cold, Fire, Lightning, and Poison',
    'Rocky Waste and Stony Tomb': 'Cold, Fire, Lightning, Poison, and Magic',
    'Sewers': 'Cold, Fire, Poison, and Magic',
    'Spider Forest and Spider Cavern': 'Cold, Fire, Lightning, and Poison',
    'Stony Field': 'Cold, Fire, Lightning, and Poison',
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': 'Cold, Fire, Lightning, Poison, and Magic',
    'The Forgotten Tower': 'Fire, Lightning, and Physical',
    'The Pit': 'Cold and Fire',
    'Travincal': 'Cold, Fire, Lightning, and Poison',
    'Tristram': 'Fire, Lightning, and Poison',
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': 'Cold, Fire, Lightning, Poison, Physical, and Magic'
}

scdict = {
    'Ancient\'s Way and Icy Cellar': '1',
    'Arcane Sanctuary': '9-12',
    'Arreat Plateau': 'None',
    'Blood Moor and Den of Evil': 'None',
    'Bloody Foothills': 'None',
    'Burial Grounds, The Crypt, and The Mausoleum': '2',
    'Cathedral and Catacombs': 'None',
    'Chaos Sanctuary': 'None',
    'Cold Plains and The Cave': '1',
    'Crystalline Passage and Frozen River': 'None',
    'Dark Wood': 'None',
    'Dry Hills and Halls of the Dead': 'None',
    'Durance of Hate': 'None',
    'Far Oasis': 'None',
    'Flayer Jungle and Flayer Dungeon': 'None',
    'Frigid Highlands': 'None',
    'Glacial Trail': 'None',
    'Jail': 'None',
    'Kurast Bazaar, Ruined Temple, and Disused Fane': 'None',
    'Kurast Sewers': '1',
    'Lost City, Valley of Snakes, and Claw Viper Temple': 'None',
    'Moo Moo Farm': 'None',
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': '1',
    'Outer Steppes and Plains of Despair': 'None',
    'River of Flame and City of the Damned': 'None',
    'Rocky Waste and Stony Tomb': '1',
    'Sewers': 'None',
    'Spider Forest and Spider Cavern': 'None',
    'Stony Field': 'None',
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': '6',
    'The Forgotten Tower': 'None',
    'The Pit': '1',
    'Travincal': 'None',
    'Tristram': 'None',
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': 'None'
}

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
        zone = tz_status.get("terrorZone").get("highestProbabilityZone").get("zone")
        pingid = tzdict.get(zone)
        bp = bpdict.get(zone)
        su = sudict.get(zone)
        im = imdict.get(zone)
        sc = scdict.get(zone)

        # build the message
        message = 'Current Terror Zone:\n'
        message += f'Zone: **{zone}** <@&{pingid}>\n'
        message += f'Boss Packs: **{bp}**\n'
        message += f'Super Uniques: **{su}**\n'
        message += f'Immunities: **{im}**\n'
        message += f'Sparkly Chests: **{sc}**\n'
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
        terror_zone = self.d2rw.terror_zone().get('terrorZone').get('highestProbabilityZone').get('zone')

        # if the terror zone changed since the last check, send a message to Discord
        if terror_zone and terror_zone != self.d2rw.current_terror_zone:
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
            terror_zone = self.d2rw.terror_zone().get('terrorZone').get('highestProbabilityZone').get('zone')
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
