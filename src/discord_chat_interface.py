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
            print('ignored', message.content)
            return

        content = message.content[len(self.name) + 1:].strip()
        print("responding to *{}*".format(content))
        await message.channel.send(self._on_messsage_received(content))

    def get_message(self):
        text = input()
        if text[:len(self.name)] == self.name:
            responce = self._on_messsage_received(text[:len(self.name) + 1])
            self.send_message(responce)
    
    def _is_message_for_me(self, message):
        return message[:len(self.name)] == self.name
    
    def _on_messsage_received(self, message):
        print(len(self.on_message_callbacks))
        for callback in self.on_message_callbacks:
            res = callback(message)
            if res:
                return res
        return 'Sorry, I did not understand that.'
    
    def add_message_receiver(self, callback):
        self.on_message_callbacks.append(callback)
        print('addcallback', callback, len(self.on_message_callbacks))

class TestDiscordChatInterface(unittest.TestCase):
    def test_failure(self):
        # Replace this with actual tests
        self.assertEqual(True, False)

if __name__ == "__main__":
    unittest.main()
