"""
implement only the second of the loop in the main of termdocumentindex
"""

from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus, Document
from indexing import Index, TermDocumentIndex 
from indexing.invertedindex import InvertedIndex
from indexing.positionalinvertedindex import PositionalInvertedIndex
from indexing.soundexindex import SoundexIndex
from queries.booleanqueryparser import BooleanQueryParser
from text import BasicTokenProcessor, englishtokenstream
from porter2stemmer import Porter2Stemmer
import os.path
import time

from text.tokenprocessor import TokenProcessor

def soundex_hashing(term : str) -> str:
    term = term.upper()
    soundex = term[0]

    dictionary = {"BFPV": "1", 
            "CGJKQSXZ": "2",
            "DT": "3",
            "L": "4", 
            "MN": "5", 
            "R": "6",
            "AEIOUHWY": "0"}
    count = {}
    for char in term[1:]:
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if key in count:
                    count[key]+=1
                else:
                    count[key] = 1
                # if code != '.':
                #     if code != soundex[-1]:
                if count[key] == 2:
                    count[key] = 0
                else:
                    soundex += code

    soundex = soundex.replace("0", "")
    if (len(soundex) < 4):
        soundex + "0" * (4-len(soundex))
    else:
        soundex = soundex[:4]

    return soundex


def soundex_indexing(corpus : DocumentCorpus) -> Index:

    si = SoundexIndex()
    for c in corpus:
        # print(c)
        stream = englishtokenstream.EnglishTokenStream(c.getContent())
        for s in stream:
             # send this to add_term
            # tokenList = token_processor.process_token(s)
            soundex = soundex_hashing(s)
            si.add_term(soundex, c.id)
        
          
    return si
    # token = token.upper()
    # soundex = token[0]

    # dictionary = {"BFPV": "1", 
    #               "CGJKQSXZ": "2",
    #               "DT": "3",
    #               "L": "4", 
    #               "MN": "5", 
    #               "R": "6",
    #               "AEIOUHWY": "0"}

    # for char in token[1:]:
    #     for key in dictionary.keys():
    #         if char in key:
    #             code = dictionary[key]
    #             if code != '0':
    #                 soundex += code
    # soundex = soundex[:4]
    # return soundex


def index_corpus(corpus : DocumentCorpus) -> Index:
    
    # token_processor = BasicTokenProcessor()
    token_processor = TokenProcessor()
    # vocabulary = {}
    # vocabulary = set()
    

    # for d in corpus:
    #     # print(f"Found document {d.title}")
    #     # TODO:
    #     print(type(d))
    #     stream = englishtokenstream.EnglishTokenStream(d.getContent())
    #     for s in stream:
    #         term = token_processor.process_token(s)
    #         vocabulary.add(term)

        #   Tokenize the document's content by creating an EnglishTokenStream around the document's .content()
        #   Iterate through the token stream, processing each with token_processor's process_token method.
        #   Add the processed token (a "term") to the vocabulary set.

    # TODO:
    # After the above, next:
    # Create a TermDocumentIndex object, with the vocabular you found, and the len() of the corpus.
    # Iterate through the documents in the corpus:
    #   Tokenize each document's content, again.
    #   Process each token.
    #   Add each processed term to the index with .add_term().
    # t1 = TermDocumentIndex(vocabulary, len(corpus))
    # for c in corpus:
    #     stream = englishtokenstream.EnglishTokenStream(c.get_content())
    #     for s in stream:
    #         term = token_processor.process_token(s)
    #         t1.add_term(term, c.id)

    # return t1

    # t2 = InvertedIndex(vocabulary, len(corpus))
    t2 = PositionalInvertedIndex()
    for c in corpus:
        # print(c)
        stream = englishtokenstream.EnglishTokenStream(c.getContent())
        position = 1
        for s in stream:
            tokenList = token_processor.process_token(s)
            for token in tokenList:
                t2.add_term(token, c.id, position)
                position+=1

    return t2

def load_docs():
    
    return 0


if __name__ == "__main__":

    # token_processor = BasicTokenProcessor()
    token_processor = TokenProcessor()
    queryParser = BooleanQueryParser()
    stemmer = Porter2Stemmer()
    corpus = None
    # corpus_path = Path(r"C:\Users\anura\Desktop\CSULB\Sem 1\CECS_529_SET\Homework\Homework 1\SearchFoundations_Python\all-nps-sites-extracted")
    corpus_path = input("Enter the path of the directory to be indexed: ")
    if os.path.isdir(corpus_path):
        for root, dirs, files in os.walk(corpus_path):#, "r+")
            if os.path.join(root, files[0]).split(".")[1] == "json":
                corpus = DirectoryCorpus.load_json_directory(corpus_path, ".json")

            elif os.path.join(root, files[0]).split(".")[1] == "txt":
                corpus = DirectoryCorpus.load_json_directory(corpus_path, ".txt")

    else:
        print("Directory not exists.")
    
    # corpus_path = "./all-nps-sites-extracted"

    # #COMMENTED THIS
    # corpus = DirectoryCorpus.load_json_directory(corpus_path, ".json")

    # Build the index over this directory.
    # print(type(d))

    # COMMENTED EVERYTHING AFTER THIS
    start = time.process_time()
    index = index_corpus(corpus)    
    print(time.process_time() - start)
    
    # index.add_term()

    # We aren't ready to use a full query parser;
    # for now, we'll only support single-term queries.
    # query = "whale" # hard-coded search for "whale"
    
    query = ""
    while True:
        postings = []
        query = input("Enter a query: ")
        # if query == "quit":
        #     break
        
        # special queries
        if (query[0] == ":"):
            q_token = query[1:].split(" ")

            if (q_token[0] == "stem"):
                # do stemming and then print
                print(stemmer.stem(q_token[1]))
                
            elif (q_token[0] == "index"):
                for root, dirs, files in os.walk(q_token[1]):#, "r+")
                    if os.path.join(root, files[0]).split(".")[1] == "json":
                        corpus = DirectoryCorpus.load_json_directory(q_token[1], ".json")

                    elif os.path.join(root, files[0]).split(".")[1] == "txt":
                        corpus = DirectoryCorpus.load_json_directory(q_token[1], ".txt")

                index = index_corpus(corpus)

            elif (q_token[0] == "q"):
                break

            elif (q_token[0] == "vocab"):
                print("First 1000 terms.")
                terms = list(index.vocab.keys())
                terms.sort()
                for i in range(1000):
                    print(terms[i])
                # print(terms[:1000], sep="\n")
                print("Total terms : ", len(terms))

            elif (q_token[0] == "author"):
                # s = SoundexIndex()
                d = DirectoryCorpus.load_json_directory("mlb-articles-4000", ".json")
                index = soundex_indexing(d)
                hashed_term = soundex_hashing(q_token[1])
                postings = index.getPostings(hashed_term)
                for p in postings:
                    print("Title: ", d.get_document(p.doc_id).getTitle, end=" ")
                    authors = d.get_document(p.doc_id).getAuthor()
                    for a in authors:
                        print("(Author: ", a, " )", end=" ")
                    # print(type(authors))
                    print("Doc ID: ", p.doc_id)

                print("Total Documents: ", len(postings))
                print("Do you want to view a document? y - Yes or n - No")
                inp = input("Enter you choice: ")
                if inp == "y":
                    doc = int(input("Enter the Doc ID of the document that you want to see: "))
                    for p in postings:
                        if p.doc_id == doc:
                            print("Content of file: ")
                            cont = d.get_document(p.doc_id).getContent()
                            for c in cont:
                                print(c, end=" ")

                   
                    # print("Title: ", d.get_document(p.doc_id).getTitle, " (Author: ", for i in d.get_document(p.doc_id).getAuthor(), " )")
                    # print()
                
        else:
            queryComp = queryParser.parse_query(query)
            postings = queryComp.get_postings(index, token_processor)

            for p in postings:
                # print("Doc ID - ", p.doc_id)
                print("Title: ", corpus.get_document(p.doc_id).getTitle, " (Doc ID : ", p.doc_id, " )")

            print("Total Documents - ", len(postings))
        
            print("Do you want to view a document? y - Yes or n - No")
            inp = input("Enter you choice: ")
            if inp == "y":
                doc = int(input("Enter the Doc ID of the document that you want to see: "))
                for p in postings:
                    if p.doc_id == doc:
                        print("Content of file: ",)
                        cont = corpus.get_document(p.doc_id).getContent()
                        for c in cont:
                            print(c, end=" ")
                        print()
            # print("Title: ", d.get_document(p.doc_id).getTitle, " (Author: ", for i in d.get_document(p.doc_id).getAuthor(), " )")
            # print()
        



        # #OLD MAIN CODE
        # # Processing the query as terms
        # query = token_processor.process_token(query)
        # # print(query)
        # print(type(query))
        # # print(f"The query '{query}' is found in  the following documents: ")
        # # for p in index.getPostings(query):
        # #     pList.append(d.get_document(p.doc_id).getTitle)

        # # if len(pList) == 0:
        # #     print("No documents found")
        
        # # else:
        # #     print(sorted(pList))
        # #     print(f"'{query}' is found in {len(pList)} documents")
        # # if type(query) == 'list':
        # print("The query ", end='')
        # for q in query:
        #     qList = []
        #     # print(f"The query '{q}' is found in  the following documents: ")
        #     for p in index.getPostingsWithPositions(q):    
        #         qList.append(corpus.get_document(p.doc_id).getTitle)

        #     if len(qList) == 0:
        #         # print("No documents found")
        #         continue
            
        #     else:
        #         # print(sorted(qList))
        #         pList = pList + qList
        #         # print(f"'{q}' is found in {len(pList)} documents")
        #     print(q, end=", ")
        # print("are found in the following documents: ")
        # print(sorted(pList), sep="\n")
        # print("Total documents: ", len(pList))



        # else:
        #     print(f"The query '{query}' is found in  the following documents: ")
        #     for p in index.getPostingsWithPositions(query):
        #         pList.append(d.get_document(p.doc_id).getTitle)

        #     if len(pList) == 0:
        #         print("No documents found")
        #     else:
        #         print(sorted(pList))
        #         print(f"Total documents: {len(pList)} documents")


    # query = input("Enter the term to search: ")
    # while (query != "quit"):
    #     for p in index.getPostings(query):
    #         # print()
    #         print(f"{d.get_document(p)}")
    #         # print(p)
    #     query = input("Enter the term to search: ")
    #     # TODO: fix this application so the user is asked for a term to search.