import unittest

class CliChatInterface:
    def __init__(self):
        self.name = 'StaCIA'
        self.on_message_callbacks = []

    def send_message(self, message):
        print(message)

    def get_message(self):
        message = input()
        if self._is_message_for_me(message):
            content = message[len(self.name) + 1:].strip()
            responce = self._on_messsage_received(content)
            self.send_message(responce)
        self.get_message()
    
    def _is_message_for_me(self, message):
        return message[:len(self.name)] == self.name
    
    def _on_messsage_received(self, message):
        print('*{}*'.format(message))
        print(len(self.on_message_callbacks), )
        for callback in self.on_message_callbacks:
            res = callback(message)
            if res:
                return res
        return 'Sorry, I did not understand that.'
    
    def add_message_receiver(self, callback):
        self.on_message_callbacks.append(callback)


class TestCliChatInterface(unittest.TestCase):
    def setUp(self):
        self.interface = CliChatInterface()
    
    def test_callbacks(self):
        call_count = {'calls': 0}
        def increment(msg):
            call_count['calls'] += 1
        self.interface.add_message_receiver(increment)
        self.assertEqual(call_count['calls'], 0)
        self.interface._on_messsage_received('msg')
        self.assertEqual(call_count['calls'], 1)
    
    def test_message_is_for_me(self):
        self.assertTrue(self.interface._is_message_for_me(self.interface.name + ':'))
        self.assertFalse(self.interface._is_message_for_me('time:'))
        self.assertFalse(self.interface._is_message_for_me(''))
        self.assertFalse(self.interface._is_message_for_me(':' + self.interface.name))

if __name__ == "__main__":
    unittest.main()
