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

#####################
# Bot Configuration #
#####################
# Setting environment variables is preferred, but you can also edit the variables below.

# Discord (Required)
TZ_DISCORD_TOKEN = environ.get('TZ_DISCORD_TOKEN')
TZ_DISCORD_CHANNEL_ID = int(environ.get('TZ_DISCORD_CHANNEL_ID', 0))

# D2RuneWizard API (Required)
TZ_D2RW_TOKEN = environ.get('TZ_D2RW_TOKEN')

# Emoji Mapping, currently uses default Discord Emoji.
# You can use custom emoji by using the emoji ID, e.g. :emoji_name:
emoji_map = {
    'Fire': ':fire:',
    'Cold': ':snowflake:',
    'Lightning': ':zap:',
    'Magic': ':magic_wand:',
    'Poison': ':nauseated_face:',
    'Physical': ':axe:',
    # 'None': ':white_check_mark:',
}

########################
# End of configuration #
########################

##################
# Bot Dictionary #
##################
tzdict = {
    'Ancient\'s Way and Icy Cellar': {
        'pingid': '1033401915377188935',
        'boss_packs': '6-8',
        'super_uniques': 'Snapchip Shatter',
        'immunities': ['Cold', 'Lightning', 'Poison', 'Physical'],
        'sparkly_chests': '1',
    },
    'Arcane Sanctuary': {
        'pingid': '1033400916650491915',
        'boss_packs': '7-9',
        'super_uniques': 'The Summoner',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical'],
    },
    'Arreat Plateau': {
        'pingid': '1033401910767669308',
        'boss_packs': '9-11',
        'super_uniques': 'Thresh Socket',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Blood Moor and Den of Evil': {
        'pingid': '1033399859039973457',
        'boss_packs': '7-9',
        'super_uniques': 'Corpsefire',
        'immunities': ['Cold', 'Fire'],
    },
    'Bloody Foothills': {
        'pingid': '1033401900269326396',
        'boss_packs': '4-6',
        'super_uniques': 'Dac Farren and Shenk The Overseer',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Burial Grounds, The Crypt, and The Mausoleum': {
        'pingid': '1033400209704755210',
        'boss_packs': '8-10',
        'super_uniques': 'Blood Raven and Bonebreaker',
        'immunities': ['Lightning'],
        'sparkly_chests': '2',
    },
    'Cathedral and Catacombs': {
        'pingid': '1033400591436754954',
        'boss_packs': '27-35',
        'super_uniques': 'Bone Ash and Andariel',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Physical'],
    },
    'Chaos Sanctuary': {
        'pingid': '1033401692491874334',
        'boss_packs': '6-7',
        'super_uniques': 'Grand Vizier of Chaos, Infector of Souls, Lord De Seis, and Diablo',
        'immunities': ['Cold', 'Fire', 'Lightning'],
    },
    'Cold Plains and The Cave': {
        'pingid': '1033400167900123226',
        'boss_packs': '13-16',
        'super_uniques': 'Bishibosh and Coldcrow',
        'immunities': ['Cold', 'Fire', 'Lightning'],
        'sparkly_chests': '1',
    },
    'Crystalline Passage and Frozen River': {
        'pingid': '1033401906736922624',
        'boss_packs': '13-17',
        'super_uniques': 'Frozenstein',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Dark Wood': {
        'pingid': '1033400366630441060',
        'boss_packs': '7-9',
        'super_uniques': 'Treehead Woodfist',
        'immunities': ['Cold', 'Fire', 'Poison'],
    },
    'Dry Hills and Halls of the Dead': {
        'pingid': '1033400910669426828',
        'boss_packs': '20-27',
        'super_uniques': 'Bloodwitch the Wild',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Durance of Hate': {
        'pingid': '1033401340682055680',
        'boss_packs': '15-21',
        'super_uniques': 'Wyand Voidbringer, Maffer Dragonhand, Bremm Sparkfist, and Mephisto',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Far Oasis': {
        'pingid': '1033400912795943003',
        'boss_packs': '7-9',
        'super_uniques': 'Beetleburst',
        'immunities': ['Lightning', 'Poison', 'Physical'],
    },
    'Flayer Jungle and Flayer Dungeon': {
        'pingid': '1033401331848859758',
        'boss_packs': '22-29',
        'super_uniques': 'Stormtree and Witch Doctor Endugu',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Frigid Highlands': {
        'pingid': '1033401902186119259',
        'boss_packs': '9-11',
        'super_uniques': 'Eldritch the Rectifier, Sharptooth Slayer, and Eyeback the Unleashed',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Glacial Trail': {
        'pingid': '1033401904371335168',
        'boss_packs': '7-9',
        'super_uniques': 'Bonesaw Breaker',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical'],
    },
    'Jail': {
        'pingid': '1033400502798516355',
        'boss_packs': '18-24',
        'super_uniques': 'Pitspawn Fouldog',
        'immunities': ['Cold', 'Fire', 'Poison', 'Physical'],
    },
    'Kurast Bazaar, Ruined Temple, and Disused Fane': {
        'pingid': '1033401333912436767',
        'boss_packs': '15-17',
        'super_uniques': 'Battlemaid Sarina',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Kurast Sewers': {
        'pingid': '1033401336399679498',
        'boss_packs': '12-14',
        'super_uniques': 'Icehawk Riftwing',
        'immunities': ['Cold', 'Lightning', 'Poison', 'Magic'],
        'sparkly_chests': '1',
    },
    'Lost City, Valley of Snakes, and Claw Viper Temple': {
        'pingid': '1033400914867933244',
        'boss_packs': '21-28',
        'super_uniques': 'Dark Elder and Fangskin',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Magic'],
    },
    'Moo Moo Farm': {
        'pingid': '1033400750656729088',
        'boss_packs': '6-8',
        'super_uniques': 'The Cow King',
    },
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': {
        'pingid': '1033401913309417583',
        'boss_packs': '12-14',
        'super_uniques': 'Pindleskin and Nihlathak',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Outer Steppes and Plains of Despair': {
        'pingid': '1033401688201101402',
        'boss_packs': '16-20',
        'super_uniques': 'Izual',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'River of Flame and City of the Damned': {
        'pingid': '1033401690436665425',
        'boss_packs': '14-17',
        'super_uniques': 'Hephasto The Armorer',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Rocky Waste and Stony Tomb': {
        'pingid': '1033400908308041870',
        'boss_packs': '17-23',
        'super_uniques': 'Creeping Feature',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Magic'],
        'sparkly_chests': '1',
    },
    'Sewers': {
        'pingid': '1033400906227654829',
        'boss_packs': '18-24',
        'super_uniques': 'Radament',
        'immunities': ['Cold', 'Fire', 'Poison', 'Magic'],
    },
    'Spider Forest and Spider Cavern': {
        'pingid': '1033401329814601748',
        'boss_packs': '14-20',
        'super_uniques': 'Sszark The Burning',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Stony Field': {
        'pingid': '1033400326205735014',
        'boss_packs': '7-9',
        'super_uniques': 'Rakanishu',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': {
        'pingid': '1033400918974152904',
        'boss_packs': '49-63',
        'super_uniques': 'Ancient Kaa The Soulless and Duriel',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Magic'],
        'sparkly_chests': '6',
    },
    'The Forgotten Tower': {
        'pingid': '1033400469634170922',
        'boss_packs': '15-20',
        'super_uniques': 'The Countess',
        'immunities': ['Fire', 'Lightning', 'Physical'],
    },
    'The Pit': {
        'pingid': '1033400658008735775',
        'boss_packs': '8-11',
        'super_uniques': 'None',
        'immunities': ['Cold', 'Fire'],
        'sparkly_chests': '1',
    },
    'Travincal': {
        'pingid': '1033401338425528383',
        'boss_packs': '6-8',
        'super_uniques': 'Ismail Vilehand, Toorc Icefist, and Geleb Flamefinger',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Tristram': {
        'pingid': '1033400671493423126',
        'boss_packs': '5-6',
        'super_uniques': 'Griswold',
        'immunities': ['Fire', 'Lightning', 'Poison'],
    },
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': {
        'pingid': '1033401917591781527',
        'boss_packs': '22-29',
        'super_uniques': 'Colenzo The Annihilator, Achmel The Cursed, Bartuc The Bloody, Ventar The Unholy, Lister The Tormentor, and Baal',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
}

#####################
# End of Dictionary #
#####################

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
            return response.json().get('terrorZone', {})
        except Exception as err:
            print(f'[D2RW.terror_zone] API Error: {err}')
            return {}

    @staticmethod
    def terror_zone_message(discord_client):
        """
        Returns a formatted message of the current terror zone status.
        """
        # get the currently reported TZ status
        tz_status = D2RuneWizardClient.terror_zone()
        zone = tz_status.get('highestProbabilityZone', {}).get('zone')
        pingid = tzdict.get(zone).get('pingid')
        boss_packs = tzdict.get(zone).get('boss_packs')
        super_uniques = tzdict.get(zone).get('super_uniques')
        immunities = tzdict.get(zone).get('immunities')
        sparkly_chests = tzdict.get(zone).get('sparkly_chests')

        # build the message
        message = f'Current Terror Zone: **{zone}**\n\n'
        message += f'Super Uniques: {super_uniques}\n'
        message += f'Boss Packs: {boss_packs}\n'
        #message += f'Immunities: {immunities}\n'
        #message += f'Sparkly Chests: {sparkly_chests}\n'

        # Add emoji Immunities
        if immunities:
            immunities_emoji = ' '.join([emoji_map.get(i, i) for i in immunities])
            message += f'Immunities: {immunities_emoji}\n'
        
        # Add Sparkly Chests if they exist
        if sparkly_chests:
            message += f'Sparkly Chests: {sparkly_chests}\n'

        # ping a discord role only if it is defined in tzdict
        if pingid:
            # verify that the role exists for this server by getting the alert channel,
            # getting the guild (server) that channel belongs to, and then getting
            # the role from that guild.
            role = discord_client.get_channel(TZ_DISCORD_CHANNEL_ID).guild.get_role(int(pingid))
            if not role:
                print(f'[D2RW.terror_zone_message] Warning: Role {pingid} does not exist on this server.')
            else:
                message += f'<@&{pingid}>\n\n'

        message += '> Data courtesy of d2runewizard.com'

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
            current_status = D2RuneWizardClient.terror_zone_message(self)

            channel = self.get_channel(message.channel.id)
            await channel.send(current_status)

    @tasks.loop(seconds=60)
    async def check_terror_zone(self):
        """
        Background task that checks the current terror zone via the d2runewizard.com API every 60 seconds.
        If the current status is different from the last known status, a message is sent to Discord.
        """
        # print('>> Checking Terror Zone status...')
        terror_zone = self.d2rw.terror_zone().get('highestProbabilityZone', {}).get('zone')

        # if the terror zone changed since the last check, send a message to Discord
        if terror_zone and terror_zone != self.d2rw.current_terror_zone:
            print(f'Terror Zone changed from {self.d2rw.current_terror_zone} to {terror_zone}')
            tz_message = D2RuneWizardClient.terror_zone_message(self)

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
            terror_zone = self.d2rw.terror_zone().get('highestProbabilityZone', {}).get('zone')
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
