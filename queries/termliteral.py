from xmlrpc.client import boolean
from indexing.postings import Posting
from text.tokenprocessor import TokenProcessor
from .querycomponent import QueryComponent

class TermLiteral(QueryComponent):
    """
    A TermLiteral represents a single term in a subquery.
    """

    def __init__(self, term : str, isNegative : boolean):
        self.term = term
        self.IsNegative = isNegative

    def get_postings(self, index, processor : TokenProcessor) -> list[Posting]:
        return index.getPostings(processor.process_token(self.term)[0])
        

    def __str__(self) -> str:
        return self.term

    def isNegative(self):
        return self.IsNegative
    