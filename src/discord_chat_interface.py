import unittest

import discord


class DiscordChatInterface(discord.Client):
    def __init__(self):
        super().__init__()
        self.on_message_callbacks = []

    async def on_ready(self):
        print('Logged on as', self.user, self.user.name)
        self.name = self.user.name

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user or not self._is_message_for_me(message.content):
            return

        content = message.content[len(self.name) + 1:].strip()
        print("responding to *{}*".format(content))
        await message.channel.send(self._on_message_received(content))

    def _is_message_for_me(self, message):
        return message[:len(self.name)] == self.name

    def _on_message_received(self, message):
        for callback in self.on_message_callbacks:
            res = callback(message)
            if res:
                return res[:2000]
        return 'Sorry, I did not understand that.'

    def add_message_receiver(self, callback):
        self.on_message_callbacks.append(callback)


class TestDiscordChatInterface(unittest.TestCase):
    def test_failure(self):
        # Replace this with actual tests
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
