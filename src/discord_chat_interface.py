import unittest

import discord

class DiscordChatInterface(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


class TestDiscordChatInterface(unittest.TestCase):
    def test_failure(self):
        # Replace this with actual tests
        self.assertEqual(True, False)

if __name__ == "__main__":
    unittest.main()
