# -*- coding: utf-8 -*-
# load Dependancies

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import sys
import os
import textwrap
import logging
import signal
import argparse


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
        '--url',
        help='A link to the website url',
        default='no')
    parser.add_argument(
        '--sentence',
        help='Argument to define number of sentence for the summary',
        default='no',
        type=int)
    parser.add_argument(
        '--language',
        help='Argument to define language of the summary',
        default='no')

    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
        # Configure logging
    logging.basicConfig(filename='applog.log',
                        filemode='w',
                        level=logging.INFO,
                        format='%(levelname)s:%(message)s')
    args = parse_args(argv)
    action = args.action
    url = args.url
    LANGUAGE = "english" if args.language is None else args.language
    SENTENCES_COUNT = 2 if args.sentence is None else args.sentence
    if action == 'summarize':
        # guide against errors
        try:
            parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
            # or for plain text files
            # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
            stemmer = Stemmer(LANGUAGE)

            summarizer = Summarizer(stemmer)
            summarizer.stop_words = get_stop_words(LANGUAGE)

            for sentence in summarizer(parser.document, SENTENCES_COUNT):
                print(sentence)
                sys.stdout.flush()

        except:
            print(
                '\n\n Invalid Entry!, please Ensure you enter a valid web link \n\n')
            sys.stdout.flush()
            return
        return
    else:
        print(
            '\nAction command is not supported\n for help: run python3 app.py -h'
        )
        sys.stdout.flush()
        return


if (__name__ == '__main__'):
    main()
