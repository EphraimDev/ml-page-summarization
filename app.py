# load Dependancies
import sys
import os
import threading
import queue
import time
import nltk
import textwrap
import logging
import signal
import argparse
from newspaper import Article


def parse_args(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            A command line utility for website summarization.
            -----------------------------------------------
            These are common commands for this app.'''))
    parser.add_argument(
        'action',
        help='This action should be summarize')
    parser.add_argument(
        '--website',
        help='A link to the website url')

    return parser.parse_args(argv[1:])

    # NLTK's punkt require to run Article Summary
    nltk.download('punkt')

# define input variable


def main(argv=sys.argv):
        # Configure logging
    logging.basicConfig(filename='applog.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(levelname)s:%(message)s')
    args = parse_args(argv)
    action = args.action
    website = args.website
    if action == 'summarize':
        # guide against errors
        try:
            article = Article(website)
            article.download()
            article.parse()
            article.nlp()
            # # print keywords
            # print('\n keywords; \n', article.keywords)
            # print page summary
            print('\n summary :\n\n', article.summary,'\n\n')
            sys.stdout.flush()
        except:
            print('\n\n Invalid Entry!, please Ensure you enter a valid web link \n\n')
            sys.stdout.flush()


if (__name__ == '__main__'):
    main()
