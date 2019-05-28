import unittest

class CliChatInterface:
    def __init__(self):
        self.name = 'bob'
        self.on_message_callbacks = []

    def send_message(self, message):
        print(message)

    def get_message(self):
        text = input()
        if text[:len(self.name)] == self.name:
            self.__on_messsage_received(text[:len(self.name) + 1])
    
    def _is_message_for_me(self, message):
        return message[:len(self.name)] == self.name
    
    def _on_messsage_received(self, message):
        for callback in self.on_message_callbacks:
            callback(message)
    
    def add_message_callback(self, callback):
        self.on_message_callbacks.append(callback)


class TestCliChatInterface(unittest.TestCase):
    def setUp(self):
        self.interface = CliChatInterface()
    
    def test_callbacks(self):
        call_count = {'calls': 0}
        def increment(msg):
            call_count['calls'] += 1
        self.interface.add_message_callback(increment)
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
