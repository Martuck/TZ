#!/usr/bin/env python3
"""
A Discord Bot for tracking Diablo 2: Resurrected Terror Zones - https://github.com/Martuck/TZ
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
from asyncio import sleep
from os import environ, path
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
# Token and contact (email address) for d2runewizard.com API, get a token at https://d2runewizard.com/integration
TZ_D2RW_TOKEN = environ.get('TZ_D2RW_TOKEN')
TZ_D2RW_CONTACT = environ.get('TZ_D2RW_CONTACT')

# Emoji Mapping, currently uses default Discord Emoji.
# You can use custom emoji by using the emoji ID, e.g. :emoji_name:
emoji_map = {
    'Cold': ':snowflake:',
    'Fire': ':fire:',
    'Lightning': ':zap:',
    'Magic': ':magic_wand:',
    'Physical': ':axe:',
    'Poison': ':nauseated_face:',
}

########################
# End of configuration #
########################

##################
# Bot Dictionary #
##################
tzdict = {
    'Ancient Tunnels': {
        'boss_packs': '6-8',
        'immunities': ['Fire', 'Poison', 'Lightning', 'Magic'],
    },
    'Ancient\'s Way and Icy Cellar': {
        'boss_packs': '6-8',
        'super_uniques': 'Snapchip Shatter',
        'immunities': ['Cold', 'Lightning', 'Poison', 'Physical'],
        'sparkly_chests': '1',
    },
    'Arcane Sanctuary': {
        'boss_packs': '7-9',
        'super_uniques': 'The Summoner',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical'],
    },
    'Arreat Plateau and Pit of Acheron': {
        'boss_packs': '15-19',
        'super_uniques': 'Thresh Socket',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Black Marsh and The Hole': {
        'boss_packs': '15-20',
        'immunities': ['Fire', 'Cold', 'Lightning', 'Poison'],
        'sparkly_chests': '1',
    },
    'Blood Moor and Den of Evil': {
        'boss_packs': '7-9',
        'super_uniques': 'Corpsefire',
        'immunities': ['Cold', 'Fire'],
    },
    'Bloody Foothills, Frigid Highlands and Abaddon': {
        'boss_packs': '19-25',
        'super_uniques': 'Dac Farren, Shenk The Overseer, Eldritch the Rectifier, Sharptooth Slayer and Eyeback the Unleashed',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Burial Grounds, The Crypt, and The Mausoleum': {
        'boss_packs': '8-10',
        'super_uniques': 'Blood Raven and Bonebreaker',
        'immunities': ['Lightning'],
        'sparkly_chests': '2',
    },
    'Cathedral and Catacombs': {
        'boss_packs': '27-35',
        'super_uniques': 'Bone Ash and Andariel',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Physical'],
    },
    'Chaos Sanctuary': {
        'boss_packs': '6-7',
        'super_uniques': 'Grand Vizier of Chaos, Infector of Souls, Lord De Seis, and Diablo',
        'immunities': ['Cold', 'Fire', 'Lightning'],
    },
    'Cold Plains and The Cave': {
        'boss_packs': '13-16',
        'super_uniques': 'Bishibosh and Coldcrow',
        'immunities': ['Cold', 'Fire', 'Lightning'],
        'sparkly_chests': '1',
    },
    'Crystalline Passage and Frozen River': {
        'boss_packs': '13-17',
        'super_uniques': 'Frozenstein',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Dark Wood and Underground Passage': {
        'boss_packs': '16-22',
        'super_uniques': 'Treehead Woodfist',
        'immunities': ['Cold', 'Fire', 'Poison', 'Lightning'],
        'sparkly_chests': '1',
    },
    'Dry Hills and Halls of the Dead': {
        'boss_packs': '20-27',
        'super_uniques': 'Bloodwitch the Wild',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Durance of Hate': {
        'boss_packs': '15-21',
        'super_uniques': 'Wyand Voidbringer, Maffer Dragonhand, Bremm Sparkfist, and Mephisto',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Far Oasis': {
        'boss_packs': '7-9',
        'super_uniques': 'Beetleburst',
        'immunities': ['Lightning', 'Poison', 'Physical'],
    },
    'Flayer Jungle and Flayer Dungeon': {
        'boss_packs': '22-29',
        'super_uniques': 'Stormtree and Witch Doctor Endugu',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Glacial Trail and Drifter Cavern': {
        'boss_packs': '13-17',
        'super_uniques': 'Bonesaw Breaker',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical'],
    },
    'Great Marsh': {
        'boss_packs': '10-15',
        'immunities': ['Fire', 'Lightning', 'Cold'],
    },
    'Jail and Barracks': {
        'boss_packs': '24-32',
        'super_uniques': 'Pitspawn Fouldog and The Smith',
        'immunities': ['Cold', 'Fire', 'Poison', 'Physical'],
    },
    'Kurast Bazaar, Ruined Temple, and Disused Fane': {
        'boss_packs': '15-17',
        'super_uniques': 'Battlemaid Sarina',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Lost City, Valley of Snakes, and Claw Viper Temple': {
        'boss_packs': '21-28',
        'super_uniques': 'Dark Elder and Fangskin',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Magic'],
    },
    'Moo Moo Farm': {
        'boss_packs': '6-8',
        'super_uniques': 'The Cow King',
    },
    'Nihlathak\'s Temple, Halls of Anguish, Halls of Pain, and Halls of Vaught': {
        'boss_packs': '12-14',
        'super_uniques': 'Pindleskin and Nihlathak',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
    'Outer Steppes and Plains of Despair': {
        'boss_packs': '16-20',
        'super_uniques': 'Izual',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'River of Flame and City of the Damned': {
        'boss_packs': '14-17',
        'super_uniques': 'Hephasto The Armorer',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Rocky Waste and Stony Tomb': {
        'boss_packs': '17-23',
        'super_uniques': 'Creeping Feature',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Magic'],
        'sparkly_chests': '1',
    },
    'Sewers': {
        'boss_packs': '18-24',
        'super_uniques': 'Radament',
        'immunities': ['Cold', 'Fire', 'Poison', 'Magic'],
    },
    'Spider Forest and Spider Cavern': {
        'boss_packs': '14-20',
        'super_uniques': 'Sszark The Burning',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Stony Field': {
        'boss_packs': '7-9',
        'super_uniques': 'Rakanishu',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Tal Rasha\'s Tombs and Tal Rasha\'s Chamber': {
        'boss_packs': '49-63',
        'super_uniques': 'Ancient Kaa The Soulless and Duriel',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Magic'],
        'sparkly_chests': '6',
    },
    'The Forgotten Tower': {
        'boss_packs': '15-20',
        'super_uniques': 'The Countess',
        'immunities': ['Fire', 'Lightning', 'Physical'],
    },
    'The Pit': {
        'boss_packs': '8-11',
        'super_uniques': 'None',
        'immunities': ['Cold', 'Fire'],
        'sparkly_chests': '1',
    },
    'Travincal': {
        'boss_packs': '6-8',
        'super_uniques': 'Ismail Vilehand, Toorc Icefist, and Geleb Flamefinger',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison'],
    },
    'Tristram': {
        'boss_packs': '5-6',
        'super_uniques': 'Griswold',
        'immunities': ['Fire', 'Lightning', 'Poison'],
    },
    'Worldstone Keep, Throne of Destruction, and Worldstone Chamber': {
        'boss_packs': '22-29',
        'super_uniques': 'Colenzo The Annihilator, Achmel The Cursed, Bartuc The Bloody, Ventar The Unholy, Lister The Tormentor, and Baal',
        'immunities': ['Cold', 'Fire', 'Lightning', 'Poison', 'Physical', 'Magic'],
    },
}

#####################
# End of Dictionary #
#####################
__version__ = '0.1'

# TZ_DISCORD_TOKEN, TZ_DISCORD_CHANNEL_ID, TZ_D2RW_TOKEN, and TZ_D2RW_CONTACT are required
if not TZ_DISCORD_TOKEN or TZ_DISCORD_CHANNEL_ID == 0 or not TZ_D2RW_TOKEN or not TZ_D2RW_CONTACT:
    print('Please set TZ_DISCORD_TOKEN, TZ_DISCORD_CHANNEL_ID, TZ_D2RW_TOKEN, and TZ_D2RW_CONTACT in your environment.')
    exit(1)


class D2RuneWizardClient():
    """
    Interacts with the d2runewizard.com terror zone API and tracks the current terror zone.
    """
    def __init__(self):
        self.current_terror_zone = None  # tracks the current terror zone

    def load_config(self):
        """
        Loads customizations from config.py.
        """
        # pylint: disable=import-outside-toplevel
        # if config.py exists, import emoji and roles
        if path.exists('config.py'):
            print('Importing configuration from config.py...')

            # try to import custom emoji
            try:
                from config import emoji as custom_emoji

                # merge config.emoji into emoji_map
                for immunity, emoji in custom_emoji.items():
                    if immunity not in emoji_map:
                        print(f'[D2RW.load_config:emoji] Error: "{immunity}" is not a valid immunity.')
                        continue
                    if not emoji or not isinstance(emoji, str):
                        print(f'[D2RW.load_config:emoji] Error: "{emoji}" is not a valid emoji for "{immunity}".')
                        continue

                    # update the immunity emoji with the custom one
                    emoji_map[immunity] = emoji
                    print(f'[D2RW.load_config:emoji] Custom {immunity} immunity emoji is "{emoji}"')
            except Exception as ex:
                print(f'[D2RW.load_config:emoji] Error: Unable to import custom emoji. {ex}')

            # try to import roles to ping
            try:
                from config import roles as ping_roles

                # merge config.roles into tzdict as pingid
                for zone, role in ping_roles.items():
                    if zone not in tzdict:
                        print(f'[D2RW.load_config:roles] Error: "{zone}" is not a valid terror zone.')
                        continue
                    if not role or not role.isnumeric():
                        print(f'[D2RW.load_config:roles] Error: "{role}" is not a valid role ID for "{zone}".')
                        continue

                    # add the role id to tzdict as pingid
                    tzdict[zone]['pingid'] = role
                    print(f'[D2RW.load_config:roles] Role to ping for "{zone}" is "{role}"')
            except Exception as ex:
                print(f'[D2RW.load_config:roles] Error: Unable to import roles to ping. {ex}')
        else:
            print('No configuration file (config.py) found. Default emoji will be used and no roles will be pinged.')

    @staticmethod
    async def terror_zone():
        """
        Get the currently reported TZ status from the D2RW TZ API.
        API documentation: https://d2runewizard.com/integration#terror-zone-tracker
        """
        try:
            url = 'https://d2runewizard.com/api/terror-zone'
            params = {'token': TZ_D2RW_TOKEN}
            headers = {
                'D2R-Contact': TZ_D2RW_CONTACT,
                'D2R-Platform': 'Discord',
                'D2R-Repo': 'https://github.com/Martuck/TZ'
            }
            response = get(url, params=params, headers=headers, timeout=10)

            # handle api rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f'[D2RW.terror_zone] API Error: HTTP {response.status_code} {response.reason}; sleeping for {retry_after} seconds...')
                await sleep(retry_after)
                return {}

            response.raise_for_status()
            return response.json().get('terrorZone', {})
        except Exception as err:
            print(f'[D2RW.terror_zone] API Error: {err}')
            return {}

    @staticmethod
    def terror_zone_message(discord_client, tz_status):
        """
        Returns a formatted message of the current terror zone status.

        :param: discord_client: The discord client object
        :param: tz_status: The current TZ status

        :return: The formatted message for Discord
        """
        zone = tz_status.get('highestProbabilityZone', {}).get('zone')
        pingid = tzdict.get(zone, {}).get('pingid')
        boss_packs = tzdict.get(zone, {}).get('boss_packs', 'UNKNOWN')
        super_uniques = tzdict.get(zone, {}).get('super_uniques', 'UNKNOWN')
        immunities = tzdict.get(zone, {}).get('immunities')
        sparkly_chests = tzdict.get(zone, {}).get('sparkly_chests')

        # build the message
        message = f'Current Terror Zone: **{zone}**\n\n'
        if super_uniques and super_uniques != 'UNKNOWN':
            message += f'Super Uniques: {super_uniques}\n'
        message += f'Boss Packs: {boss_packs}\n'

        # Add emoji Immunities
        if immunities:
            immunities_emoji = ' '.join([emoji_map.get(i, i) for i in immunities])
            message += f'Immunities: {immunities_emoji}\n'

        # Add Sparkly Chests if they exist
        if sparkly_chests:
            message += f'Sparkly Chests: {sparkly_chests}\n'

        # ping a discord role only if it is defined in tzdict
        if pingid and pingid.isnumeric():
            # verify that the role exists for this server by getting the alert channel,
            # getting the guild (server) that channel belongs to, and then getting
            # the role from that guild.
            role = discord_client.get_channel(TZ_DISCORD_CHANNEL_ID).guild.get_role(int(pingid))
            if not role:
                print(f'[D2RW.terror_zone_message] Warning: Role {pingid} does not exist on this server.')
            else:
                message += f'<@&{pingid}>\n'

        message += '\n> Data courtesy of d2runewizard.com'

        return message


class DiscordClient(discord.Client):
    """
    Connects to Discord and watches for the `.tz` or `!tz` command to report the current Terror Zone status.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.d2rw = D2RuneWizardClient()
        self.d2rw.load_config()  # load customizations from config.py

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

    @tasks.loop(seconds=60)
    async def check_terror_zone(self):
        """
        Background task that checks the current terror zone via the d2runewizard.com API every 60 seconds.
        If the current status is different from the last known status, a message is sent to Discord.
        """
        # print('>> Checking Terror Zone status...')
        tz_status = await self.d2rw.terror_zone()
        terror_zone = tz_status.get('highestProbabilityZone', {}).get('zone')

        # if the terror zone changed since the last check, send a message to Discord
        if terror_zone and terror_zone != self.d2rw.current_terror_zone:
            print(f'Terror Zone changed from "{self.d2rw.current_terror_zone}" to "{terror_zone}"')
            tz_message = D2RuneWizardClient.terror_zone_message(self, tz_status)

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
            tz_status = await self.d2rw.terror_zone()
            terror_zone = tz_status.get('highestProbabilityZone', {}).get('zone')
        except Exception as err:
            print(f'Unable to set the current terror zone at startup: {err}')
            return

        # set the current terror zone
        # this prevents a duplicate message from being sent when the bot starts
        # comment this out if you want the bot to post the current terror zone when it starts
        self.d2rw.current_terror_zone = terror_zone
        print(f'Initial Terror Zone is "{terror_zone}"')
        await sleep(60)


if __name__ == '__main__':
    client = DiscordClient(intents=discord.Intents.default())
    client.run(TZ_DISCORD_TOKEN)
