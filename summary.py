#load Dependancies
import sys, os
import threading
import queue
import time
from newspaper import Article
import nltk


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
                #print keywords
                print('\n keywords; \n',article.keywords)
                #print page summary
                print('\n summary :\n',article.summary)
            except:
                print('\n\n Invalid Entry!, please Ensure you enter a valid web link \n\n')
                
            #restart again
            input_str = ' '
            print("\n\n Type/Paste a valid hotel web link below or 'exit\' to close \n  {}".format(input_str))
            
			#close the loop
            if (input_str == EXIT_COMMAND):
                print("Exiting serial terminal.")
                break           

        
        #auto end section
        time.sleep(0.1) 
    print("End.")

if (__name__ == '__main__'): 
    main()