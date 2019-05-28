from discord_chat_interface import DiscordChatInterface
from cli_chat_interface import CliChatInterface

import sys

def main():
    args = sys.argv[1:]

    if (args and args[0] == "--cli"):
        client = CliChatInterface()
    else:
        client = DiscordChatInterface()
    
    client.add_message_receiver(lambda msg: 'hello' if msg == 'world' else None)
    client.add_message_receiver(lambda msg: 'world' if msg == 'hello' else None)
    
    if (args and args[0] == "--cli"):
        client.get_message()
    else:
        client.run('NTgyNzk1NjcxOTY3NDk4MjUx.XOzByQ.TWGoeHzh5i-LI4dVLWUFmrMmJ5w')


if __name__ == '__main__':
    main()