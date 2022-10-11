from lib2to3.pgen2.tokenize import TokenError
from indexing.index import Index
from indexing.postings import Posting
# from indexing.positionalinvertedindex import PositionalInvertedIndex
from .querycomponent import QueryComponent
from text import TokenProcessor

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    def __init__(self, terms : list[str], isNegative):
        self.terms = [s for s in terms]
        self.IsNegative = isNegative

    def get_postings(self, index : Index, processor : TokenProcessor) -> list[Posting]:

        firstList = index.getPostingsWithPositions(processor.process_token(self.terms[0])[0])
        # firstList = index.getPostingsWithPositions(self.terms[0])
        gap = 1
        for i in range(1, len(self.terms)):
            secondList = index.getPostingsWithPositions(processor.process_token(self.terms[i])[0])
            # secondList = index.getPostingsWithPositions(self.terms[i])
            temp = []
            firstListSize = len(firstList)
            secondListSize = len(secondList)
            firstListPtr = 0
            secondListPtr = 0

            while (firstListPtr < firstListSize and secondListPtr < secondListSize):

                firstPosting = firstList[firstListPtr]
                secondPosting = secondList[secondListPtr]

                if (secondPosting.doc_id == firstPosting.doc_id):
                    firstPos = firstPosting.getPositions()
                    secondPos = secondPosting.getPositions()
                    firstPosPtr = 0
                    secondPosPtr = 0

                    while (firstPosPtr < len(firstPos) and secondPosPtr < len(secondPos)):
                        firstPosValue = firstPos[firstPosPtr]
                        secondPosValue = secondPos[secondPosPtr]

                        # check if gap is 1
                        if (secondPosValue - firstPosValue == gap):
                            temp.append(firstPosting)
                            break

                        if (firstPosValue == secondPosValue):
                            firstPosPtr+=1
                            secondPosPtr+=1

                        elif (firstPosting.doc_id > secondPosting.doc_id):
                            secondListPtr+=1

                        else:
                            firstListPtr+=1

            firstList = temp
            gap+=1

        return firstList
        # TODO: program this method. Retrieve the postings for the individual terms in the phrase,
		# and positional merge them together.

    def isNegative(self):
        return self.IsNegative

    def __str__(self) -> str:
        return '"' + " ".join(self.terms) + '"'