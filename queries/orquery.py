from .querycomponent import QueryComponent
from text.tokenprocessor import TokenProcessor
from indexing import Index, Posting

from queries import querycomponent 

class OrQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        self.components = components

    def get_postings(self, index : Index, processor : TokenProcessor) -> list[Posting]:
        result = []
        # TODO: program the merge for an OrQuery, by gathering the postings of the composed QueryComponents and
		# merging the resulting postings.

        first_q = self.components[0]
        first_list = first_q.get_postings(index, processor)

        for i in range(1,len(self.components)):
            second_list = self.components[i].get_postings(index, processor)
            temp = []
            x=0
            y=0
            while (x < len(first_list) and y < len(second_list)):
                firstPosting = first_list[x]
                secondPosting = second_list[y]

                #adding the smaller doc_ids
                if (firstPosting.doc_id > secondPosting.doc_id):
                    temp.append(secondPosting)
                    y+=1
                    if (firstPosting.doc_id == secondPosting.doc_id):
                        x+=1

                else:
                    temp.append(firstPosting)
                    x+=1
                    if (firstPosting.doc_id == secondPosting.doc_id):
                        y+=1

            # adding the remaining doc_ids
            if (x == len(first_list)):
                while(y < len(second_list)):
                    temp.append(second_list[y])
                    y+=1

            elif (y == len(second_list)):
                while (x < len(first_list)):
                    temp.append(first_list[x])
                    x+=1

        result = temp

        return result

    def isNegative(self):
        return False

    def __str__(self):
        return "(" + " OR ".join(map(str, self.components)) + ")"