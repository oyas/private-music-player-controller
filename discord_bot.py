import discord
from discord.ext.commands import HelpCommand
from player import Player
import os
from dotenv import load_dotenv

class MyClient(discord.Client):
    def __init__(self, intents, player):
        super().__init__(intents=intents)
        self.player = player

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.reply('Hello!', mention_author=True)

        if message.content.startswith('<@' + str(self.user.id) + '>'):
            m = message.content.removeprefix('<@' + str(self.user.id) + '>').strip()
            print("removed=" + m)
            if m == "help" or m == "":
                await message.channel.send('<search string>\tAdd songs.\nskip\tSkip the current song.\nstop\tStop or start.\nhelp\tShow this message.')
                return
            if m == "skip":
                self.player.skip()
                return
            if m == "stop":
                self.player.stop()
                return
            self.player.queue(m)
            await message.channel.send('queued ' + m)

        print(message, message.content)

def main():
    load_dotenv()

    player = Player()

    intents = discord.Intents(messages=True)
    client = MyClient(intents=intents, player=player)
    client.run(os.getenv("DISCORD_TOKEN"))

    player.close()

if __name__ == '__main__':
    main()
