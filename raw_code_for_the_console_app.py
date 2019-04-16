#!/usr/bin/env python3
import sys, os
import csv
import pandas as pd
import argparse

#dependancies
import pandas as pd
from sumy.summarizers.lex_rank import LexRankSummarizer 
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer


def read_csv(csvfile):
    print('read_csv(): type(csvfile)) = {}'.format(csvfile))
    print('')

    data = pd.read_csv(csvfile)

    return data
    
def main():
    parser = argparse.ArgumentParser(description='Make barchart from csv.')
    parser.add_argument('-d', '--debug', help='Debugging output', action='store_true')
    parser.add_argument('csvfile', type=argparse.FileType('r'), help='Input csv file')
    args = parser.parse_args()

    print('main(): type(args.csvfile)) = {}'.format(args.csvfile))
    print('')

    ### This works 
    df = pd.read_csv(args.csvfile)

    summary_holder = []

    try:
        summarizer = LexRankSummarizer()
        for url in df.valid_website:   
            parser = HtmlParser.from_url(url, Tokenizer("english"))
            summary = summarizer(parser.document, 2)

            #saving the summary to a dataframe
            for sentence in summary:        
                summary_holder.append(sentence)
                df['summary'] = pd.DataFrame(summary_holder)

          #save dataframe as CSV           
        df.to_csv('summaried4', encoding='utf-8', index=False)   

    except:
        print('error message')
        
        
    return df[['valid_website','summary']]

if __name__ == '__main__':
    main()