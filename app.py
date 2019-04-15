# load Dependancies
import sys
import os
import time
import nltk
import textwrap
import logging
import signal
import argparse
from newspaper import Article
import heapq
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

    # NLTK's punkt require to run Article Summary
    nltk.download('punkt')
    nltk.download("stopwords")
    return parser.parse_args(argv[1:])


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

            # Removing Square Brackets and Extra Spaces
            article_text = re.sub(r'\[[0-9]*\]', ' ', article.text)
            article_text = re.sub(r'\s+', ' ', article_text)

            # Removing special characters and digits from the text
            formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
            formatted_article_text = re.sub(
                r'\s+', ' ', formatted_article_text)

            # sentence tokenization
            sentence_list = nltk.sent_tokenize(article.text)

            # Weighted Frequency of Occurrence with ~formatted_article_text~
            stopwords = nltk.corpus.stopwords.words('english')
            word_frequencies = {}

            for word in nltk.word_tokenize(formatted_article_text):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1

                 # maximum frequncy of Occurrence
            maximum_frequncy = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = (
                    word_frequencies[word]/maximum_frequncy)

                # Calculating Sentence Scores
            sentence_scores = {}
            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]

                # Getting the Summary
            summary_sentences = heapq.nlargest(
                10, sentence_scores, key=sentence_scores.get)
            summary = ' '.join(summary_sentences)

            # # print keywords
            # print('\n keywords; \n', article.keywords)
            # print page summary
            print('\n summary :\n', summary)
            sys.stdout.flush()
            return
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
