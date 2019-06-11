from src.discord_chat_interface import DiscordChatInterface
from src.cli_chat_interface import CliChatInterface
from src.relevance_detector import RelevanceDetector
from src.database_connection import make_connection
from src.query_scanner import QueryScanner
from src.data_sustainer import DataSustainer
from src.scrapers.scrape_all import scrape_all
from src.test_queries import test_all_queries
from datetime import timedelta, datetime
from threading import Timer
import time

import sys

rd = RelevanceDetector()
qs = QueryScanner()


def answer_query(query, save=True):
    start_time = time.time()
    matched_question, matched_answer, score, vars = rd.most_relevant_query(query)

    if save:
        print("Matched question in", time.time() - start_time)
        print(matched_answer)
        print(score, vars, qs.find_within_brackets(matched_answer))

    start_time = time.time()

    if save:
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO user_query (query_text, matched_question)
                SELECT
                    %s AS query_text,
                    question.id AS matched_question
                FROM question 
                WHERE question.question_text = %s;""", (query, matched_question))
                connection.commit()
        finally:
            connection.close()
        print("Saved query in", time.time() - start_time)
    return qs.answer_question(query, matched_answer)


def get_feedback(query):
    feedback_query = "UPDATE user_query SET correct = %s ORDER BY time_asked DESC LIMIT 1;"
    query = query.lower().strip('.')
    if query == "yes" or query == "correct" or query == "right" or query == "good bot":
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(feedback_query, True)
                connection.commit()
        finally:
            connection.close()
        return "Thanks for the feedback."

    if query == "no" or query == "false" or query == "wrong" or query == "bad bot":
        connection = make_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(feedback_query, False)
                connection.commit()
        finally:
            connection.close()
        return "Ops. Sorry about that. I will try to do better in the future. Thanks for the feedback."


def start_periodic_scraping(scraping_function, wait_time):
    """ Reruns the scraper once a day """

    def to_run():
        scraping_function()
        start_periodic_scraping(scraping_function, wait_time)

    Timer(wait_time.total_seconds(), to_run).start()


def run_tests(verbose):
    test_all_queries(verbose)


def main():
    args = sys.argv[1:]

    if args and args[0] == "--cli":
        client = CliChatInterface()
    elif args and args[0] == "--test":
        run_tests(False)
        sys.exit(0)
    elif args and args[0] == "--test-verbose":
        run_tests(True)
        sys.exit(0)
    elif args and args[0] == "--init":
        DataSustainer.initialize_database()
        sys.exit(0)
    elif args and args[0] == "--scrape":
        scrape_all()
        sys.exit(0)
    else:
        client = DiscordChatInterface()

    client.add_message_receiver(get_feedback)
    client.add_message_receiver(answer_query)

    if args and args[0] == "--cli":
        client.get_message()
    else:
        client.run('NTgyNzk1NjcxOTY3NDk4MjUx.XOzByQ.TWGoeHzh5i-LI4dVLWUFmrMmJ5w')
        start_periodic_scraping(scrape_all, timedelta(days=1))


if __name__ == '__main__':
    main()
