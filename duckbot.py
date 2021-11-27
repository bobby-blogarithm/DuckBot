import discord.ext.commands as disc_cmds
import yaml

from cmd_manager import CommandManager
from listen_manager import ListenerManager

CONFIG_FILE = 'config.yml'

class DuckBot(disc_cmds.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load bot config file
        with open(CONFIG_FILE) as config_file:
            self.config = yaml.safe_load(config_file)
        self.token = self.config['token']

        # Attach cogs to bot
        self.add_cog(CommandManager(self))
        self.add_cog(ListenerManager(self))

def main():
    # Create client for bot
    client = DuckBot(command_prefix='?')

    # Connect client to discord
    client.run(client.token)
    
if __name__ == '__main__':
    main()