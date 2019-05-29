from discord_chat_interface import DiscordChatInterface
from cli_chat_interface import CliChatInterface
from relevance_detector import RelevanceDetector
from database_connection import connection
import time

import sys

rd = RelevanceDetector()

def answer_query(query):
    start_time = time.time()
    matched_question, matched_answer = rd.most_relevant_query(query)
    print("Matched question in", time.time() - start_time)
    start_time = time.time()
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO user_query (query_text, matched_question)
    SELECT
        %s AS query_text,
        question.id AS matched_question
    FROM question 
    WHERE question.question_text = %s;""", (query, matched_question))
        connection.commit()
    print("Saved query in", time.time() - start_time)
    return matched_answer

def get_feedback(query):
    feeback_query = "UPDATE user_query SET correct = %s ORDER BY time_asked DESC LIMIT 1;"
    query = query.lower().strip('.')
    if query == "yes" or query == "correct" or query == "right" or query == "good bot":
        with connection.cursor() as cursor:
            cursor.execute(feeback_query, True)
            connection.commit()
        return "Thanks for the feedback."

    if query == "no" or query == "false" or query == "wrong" or query == "bad bot":
        with connection.cursor() as cursor:
            cursor.execute(feeback_query, False)
            connection.commit()
        return "Ops. Sorry about that. I will try to do better in the future. Thanks for the feedback."
    


def main():
    args = sys.argv[1:]

    relevance_detector = RelevanceDetector()

    if (args and args[0] == "--cli"):
        client = CliChatInterface()
    else:
        client = DiscordChatInterface()
    
    client.add_message_receiver(get_feedback)
    client.add_message_receiver(answer_query)
    
    if (args and args[0] == "--cli"):
        client.get_message()
    else:
        client.run('NTgyNzk1NjcxOTY3NDk4MjUx.XOzByQ.TWGoeHzh5i-LI4dVLWUFmrMmJ5w')


if __name__ == '__main__':
    main()