from connect import PrologConnector


# Review: I guess you know what to do here. Do it.

class HashableSegment:
    
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __hash__(self):
        return hash(self.start) ^ hash(self.end)

    def __str__(self):
        return f"({self.start}, {self.end})"


class Translator:

    def __init__(self):
        self.connector = PrologConnector()
        self.connector.consult_file('Prolog/axiomsTarski.pl')
        self.connector.consult_file('Prolog/definitions.pl')

    def eat(self, something):
        # TODO: Parse ↑↑↑(maybe)
        instructions: str = self.parse_food(something)
        out = self.connect_to._prolog(instructions)
        self.feedback(...)
        return out

    # TODO: Write me
    def parse_food(self, food):
        pass

    # TODO: Write me
    # Review: Is this a Human Centipede reference?
    def feedback(self, cls):
        pass

    def make_request(self, req, **kwargs):
        return self.connector.get_n_ans_new(req, **kwargs)

    # TODO: doit write this class(may be)!
