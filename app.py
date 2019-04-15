# load Dependancies
import sys
import os
import time
import textwrap
import logging
import signal
import argparse
import numpy as np
import pandas as pd
import nltk
nltk.download('punkt') # one time execution
import re


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
            print('\n summary :\n\n', article.summary, '\n\n')
            sys.stdout.flush()
        except:
            print('\n\n Invalid Entry!, please Ensure you enter a valid web link \n\n')
            sys.stdout.flush()
    if action == 'train':
        # default path for the folder inside google drive
        default_path = "drive/Colab Notebooks/Model 2/"
        # path for training text (article)
        train_article_path = default_path + "sumdata/train/train.article.txt"
        # path for training text output (headline)
        train_title_path = default_path + "sumdata/train/train.title.txt"
        # path for validation text (article)
        valid_article_path = default_path + "sumdata/train/valid.article.filter.txt"
        # path for validation text output(headline)
        valid_title_path = default_path + "sumdata/train/valid.title.filter.txt"


if (__name__ == '__main__'):
    main()
