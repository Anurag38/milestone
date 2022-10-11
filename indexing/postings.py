from symbol import term


class Posting:
    """A Posting encapsulates a document ID associated with a search query component."""

    def __init__(self, doc_id: int):
        self.doc_id = doc_id
        self.term_pos_list = list()
        

    def addPosition(self, term_pos : int):
        self.term_pos_list.append(term_pos)

    def getPositions(self):
        return self.term_pos_list
