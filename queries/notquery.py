from .querycomponent import QueryComponent
from text.tokenprocessor import TokenProcessor
from indexing import Index, Posting
from queries import querycomponent 

class NotQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index, processor : TokenProcessor) -> list[Posting]:
        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.

        literal = self.components
        result = literal.get_postings(index, processor)
        return result

    def isNegative(self):
        return True

    # def __str__(self):
    #     return "(" + " OR ".join(map(str, self.components)) + ")"