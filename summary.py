#load Dependancies
import sys, os
import threading
import queue
import time
from newspaper import Article
import nltk
import heapq
import re


#define input variable
def read_kbd_input(inputQueue):    
    
    print("\nType/Paste a valid web link below")
    while (True):
        input_str = input()
        inputQueue.put(input_str)
        
    #NLTK's punkt require to run Article Summary
    nltk.download('punkt')

#page Summary engine
def main():
    EXIT_COMMAND = "exit"
    inputQueue = queue.Queue() 
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()
    
    #start loop
    while (True):

        #loop condition
        if (inputQueue.qsize() > 0): 
            input_str = inputQueue.get()            
            print(input_str)
            
            #guide against errors
            try:
                article = Article(input_str)           
                article.download()
                article.parse() 
                article.nlp()
                
                # Removing Square Brackets and Extra Spaces
                article_text = re.sub(r'\[[0-9]*\]', ' ', article.text)  
                article_text = re.sub(r'\s+', ' ', article_text) 
                
                # Removing special characters and digits from the text
                formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)  
                formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
                
                #sentence tokenization
                sentence_list = nltk.sent_tokenize(article.text)
                
                #Weighted Frequency of Occurrence with ~formatted_article_text~
                stopwords = nltk.corpus.stopwords.words('english')
                word_frequencies = {}  
                for word in nltk.word_tokenize(formatted_article_text):  
                    if word not in stopwords:
                        if word not in word_frequencies.keys():
                            word_frequencies[word] = 1
                        else:
                            word_frequencies[word] += 1 
                            
                 #maximum frequncy of Occurrence           
                maximum_frequncy = max(word_frequencies.values())
                for word in word_frequencies.keys():  
                    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

                
                 #Calculating Sentence Scores           
                sentence_scores = {}  
                for sent in sentence_list:  
                    for word in nltk.word_tokenize(sent.lower()):
                        if word in word_frequencies.keys():
                            if len(sent.split(' ')) < 30:
                                if sent not in sentence_scores.keys():
                                    sentence_scores[sent] = word_frequencies[word]
                                else:
                                    sentence_scores[sent] += word_frequencies[word]
                                    
                 #Getting the Summary 
                summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)
                summary = ' '.join(summary_sentences)  
                
                
                #print keywords
                print('\n keywords; \n',article.keywords)
                #print page summary
                print('\n summary :\n',summary)
            except:
                print('\n\n Invalid Entry!, please Ensure you enter a valid web link \n\n')
                
                
             #close the loop
            if (input_str == EXIT_COMMAND):
                print("Oops! You Have exited the program")
                break   
                
            #restart again
            input_str = ' '
            print("\n\n Type/Paste a valid hotel web link below or 'exit\' to close \n  {}".format(input_str))
            
			        

        
        #auto end section
        time.sleep(0.1) 


if (__name__ == '__main__'): 
    main()
