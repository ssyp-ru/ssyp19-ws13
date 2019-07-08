from connect import PrologConnector


class Translator:

    def __init__(self):
        self.connector = PrologConnector()
        self.connector.consult_file('Prolog/axiomsTarski.pl')

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
    def feedback(self, cls):
        pass

    # @staticmethod
    # def connect_to_prolog(instructions: str, results=-1) -> [dict]:
    #     # pc.consult_file('Prolog/Something.pl')
    #     return pc.get_n_ans_new(instructions, maxresults=results)  # FIXME: may be unfinished(and broken)

    def make_request(self, req):
        return self.connector.get_n_ans_new(req)

    # TODO: doit write this class!