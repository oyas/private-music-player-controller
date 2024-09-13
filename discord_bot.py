import discord
from discord.ext.commands import HelpCommand
import player

class MyClient(discord.Client):
    def __init__(self, intents, driver):
        super().__init__(intents=intents)
        self.driver = driver

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
                player.skip(self.driver)
                return
            if m == "stop":
                player.stop(self.driver)
                return
            player.queue(self.driver, m)
            await message.channel.send('queued ' + m)

        print(message, message.content)

def main():
    driver = player.openYouTubeMusic()

    intents = discord.Intents(messages=True)
    client = MyClient(intents=intents, driver=driver)
    client.run()

    player.closeYouTubeMusic(driver)

if __name__ == '__main__':
    main()
