# TZ

A Discord bot for reporting Diablo 2: Resurrected [Terror Zone](https://d2runewizard.com/terror-zone-tracker) changes. By default it will report the terror zone, super uniques, boss packs, immunities, and super chests every hour when the Terror Zone changes.

You can also get the current terror zone by typing `.tz` or `!tz` in chat.

## Usage

Requires Python 3.8+, tested on Ubuntu 22.04.

### Installation

```
git clone https://github.com/Martuck/TZ.git
cd TZ
pip3 install -r requirements.txt
```

### Configuration

Configuration is done via environment variables, or you can edit the variables near the top of the script.

**Required**
 - `TZ_DISCORD_CHANNEL_ID`: The [channel id](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) to send messages to.
 - `TZ_DISCORD_TOKEN`: Token for connecting to Discord, create a bot account with the instructions [here](https://discordpy.readthedocs.io/en/stable/discord.html). Only the `Send Messages` permission is required.
 - `TZ_D2RW_TOKEN`: Token for querying the d2runewizard.com Terror Zone API. Get one by clicking `Request token` [here](https://d2runewizard.com/integration#terror-zone-tracker).
 - `TZ_D2RW_CONTACT`: The email address for your d2runewizard.com account.

**Optional**
 - Modify the `pingid` for each zone in `tzdict` if you'd like to ping a Discord role when the current zone changes. The `pingid` should be a string containing the id of the Discord role. In the future we'll support a configuration file to make this easier.

### Running

Start the bot with `python3 terror_zones.py`.

## Disclaimer

Data courtesy of [d2runewizard.com](https://d2runewizard.com/terror-zone-tracker).
