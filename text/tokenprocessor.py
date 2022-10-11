from abc import ABC, abstractmethod
from lib2to3.pgen2.tokenize import tokenize
from typing import Iterable
from porter2stemmer import Porter2Stemmer
import re

class TokenProcessor(ABC):
    """A TokenProcessor applies some rules of normalization to a token from a document,
     and returns a term for that token."""
  
    def process_token(self, token : str) -> Iterable[str]:
        """Normalizes a token into a term."""
        # initializing PorterStemmer
        stemmer = Porter2Stemmer()

        # to get only the alpha-numeric
        if (len(token) == 0 or len(token) == 1):
            return token
        
        # to remove the non-alphanumeric characters
        characters = list(token)
        startIndex = 0
        endIndex = len(characters) - 1

        startIndexB = False
        endIndexB = False

        while(True):
            if(characters[startIndex].isalpha() or characters[endIndex].isdigit()):
                if (not(startIndexB)):
                    startIndexB = True
                
            else:
                startIndex+=1

            if(characters[endIndex].isalpha() or characters[endIndex].isdigit()):
                if (not(endIndexB)):
                    endIndexB = True

            else:
                endIndex-=1

            if (startIndex >= endIndex):
                return token

            if (startIndexB and endIndexB):
                break

        token = token[startIndex:endIndex+1].lower()

        ch = ["\"", "'"]

        for c in ch:
            if c in token:
                token = token.replace(c, "")

        hyphen_tokens = []

        if '-' in token:
            tokenizer = token.split('-')
            final_string = ""
            token_n = 0
            while(token_n < len(tokenizer)):
                temp = tokenizer[token_n]
                token_n+=1
                final_string + temp
                hyphen_tokens.append(stemmer.stem(temp))

            hyphen_tokens.insert(0, final_string)
        
        else:
            hyphen_tokens.append(stemmer.stem(token))

        return hyphen_tokens

            
                
            

            



        