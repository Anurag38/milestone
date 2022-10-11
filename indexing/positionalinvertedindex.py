from typing import Iterable
from . import Posting
from .index import Index

    
class PositionalInvertedIndex(Index):
    """Implements an InvertedIndex using a hash-map or dictionary. Does not require anything prior to construction."""

    def __init__(self):
        """Constructs an empty InvertedIndex using dictionary."""
        self.vocab = {}

    def add_term(self, term: str, documentId: int, position: int,):
        """Records that the given term occurred in the given document ID."""
        # if term in self.vocab:
        #     self.vocab[term] = [Posting(doc_id, term_pos)] #inner list contains the positions of the "term" in "doc_id"
        # else:
        #     if self.vocab.get(term)[-1].doc_id != doc_id:
        #         self.vocab[term].append(Posting(doc_id, term_pos))

        # if the term already exists in the index
        if term in self.vocab:
            if (self.vocab.get(term)[-1].doc_id != documentId):
                self.vocab[term].append(Posting(documentId))
                self.vocab.get(term)[-1].addPosition(position)

            else:
                self.vocab.get(term)[-1].addPosition(position)

        # if the term is not in the index
        else:
            self.vocab[term] = [Posting(documentId)]
            self.vocab.get(term)[-1].addPosition(position)

    def getPostings(self, term: str) -> Iterable[Posting]:
        """Returns a list of Postings for all documents that contain the given term."""
        return self.vocab.get(term, [])

    def getPostingsWithPositions(self, term: str) -> Iterable[Posting]:
        """Retrieves a sequence of Postings of documents that contain the given term with its position."""
        postings = []
        if (term in self.vocab):
            postings = self.vocab[term]

        return postings
    
    def getVocabulary(self) -> Iterable[str]:
        return sorted(list(self.vocab.keys()))
