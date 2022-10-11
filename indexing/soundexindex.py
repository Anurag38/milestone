from typing import Iterable
from . import Posting
from .index import Index

class SoundexIndex(Index):
    """Implements soundex hashing on the given query"""

    def __init__(self):
        """Constructs an empty InvertedIndex using dictionary."""
        self.vocab = {}

    def add_term(self, term: str, documentId: int):
        """Records that the given term occurred in the given document ID."""
        if term not in self.vocab:
            self.vocab[term] = [Posting(documentId)]
        else:
            if self.vocab.get(term)[-1].doc_id != documentId:
                self.vocab[term].append(Posting(documentId))

    def getPostings(self, term: str) -> Iterable[Posting]:
        return self.vocab[term]