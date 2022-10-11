from text.tokenprocessor import TokenProcessor
from .querycomponent import QueryComponent
from indexing import Index, Posting
from text import TokenProcessor

from queries import querycomponent 

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index, processor : TokenProcessor) -> list[Posting]:
        result = []
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.

        first_q = self.components[0]
        second_q = self.components[1]



        first_q_posting = first_q.get_postings(index, processor)
        second_q_posting = second_q.get_postings(index, processor)

        #check if any of the list is empty
        if len(first_q_posting) == 0 or len(second_q_posting) == 0:
            return result

        # AND NOT
        if (first_q.isNegative() or second_q.isNegative()):
            positivePostings = list()
            negativePostings = list()

            #determining which query is negative
            if (first_q.isNegative()):
                positivePostings = second_q_posting
                negativePostings = first_q_posting
            else:
                positivePostings = first_q_posting
                negativePostings = second_q_posting

            pos = 0
            neg = 0
            currentPosID = 0
            currentNegId = 0

            while (True):
                currentPosID = positivePostings[pos].doc_id
                currentNegId = negativePostings[neg].doc_id

                #if both the ids are same
                if (currentPosID == currentNegId):
                    pos+=1
                    neg+=1

                    #if all neg postings are done
                    if (neg == len(negativePostings)): #not wala khatam
                        for i in range(pos, len(positivePostings)):
                            result.append(positivePostings[i]) #baki ke pos wale andar
                            pos+=1
                        break

                    elif (pos == len(positivePostings)): #pos khatam to break
                        break
                
                # if posid>negid
                elif(currentPosID > currentNegId):
                    neg+=1
                    if (neg == len(negativePostings)):
                        for i in range(pos, len(positivePostings)):
                            result.append(positivePostings[i]) #baki ke pos wale andar
                            pos+=1
                        break

                # if posid<negid
                else:
                    result.append(positivePostings[pos])
                    pos+=1

                    if (pos == len(positivePostings)):
                        break
                    

        # AND
        else:
            first_pos = 0
            second_pos = 0

            currentFirstDoc = 0
            currentSecondDoc = 0

            while(True):
                currentFirstDoc = first_q_posting[first_pos].doc_id
                currentSecondDoc = second_q_posting[second_pos].doc_id

                if (currentFirstDoc == currentSecondDoc):
                    result.append(first_q_posting[first_pos])
                    first_pos+=1
                    second_pos+=1

                elif (currentFirstDoc < currentSecondDoc):
                    first_pos+=1
                
                else:
                    second_pos+=1

                # check break condition
                if (first_pos == len(first_q_posting) or second_pos == len(second_q_posting)):
                    break

        return result

    def isNegative(self):
        return False

    def __str__(self):
        return " AND ".join(map(str, self.components))